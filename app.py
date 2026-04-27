import os

import click
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from gpt4all import GPT4All
from werkzeug.security import check_password_hash, generate_password_hash

from middleware import register_role_middleware, resolve_home_endpoint_by_role
from models import ROLE_ADMIN, ROLE_CLIENTE, Usuario, db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "reservify-dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost/reservify",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)

SYSTEM_PROMPT = (
    "Eres un asistente virtual de la plataforma educativa Edunexo. "
    "Solo respondes en espanol, de forma breve (maximo 2 o 3 oraciones). "
    "No saludes ni te presentes al inicio. Simplemente responde la pregunta del usuario "
    "sin generar preguntas adicionales ni ejemplos de conversacion."
)
_model = None


def normalize_email(value):
    return (value or "").strip().lower()


def get_model():
    global _model
    if _model is None:
        _model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    return _model


def generate_response(message, max_tokens=256):
    model = get_model()
    with model.chat_session(system_prompt=SYSTEM_PROMPT):
        response = model.generate(message, max_tokens=max_tokens)
    return response


register_role_middleware(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/ia")
def ia():
    return render_template("IA.html")


@app.route("/cliente")
def cliente():
    return render_template("cliente.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = (request.form.get("nombre") or "").strip()
        email = normalize_email(request.form.get("email"))
        password = request.form.get("password") or ""

        if not nombre or not email or not password:
            return render_template(
                "registro.html",
                message="Completa todos los campos para registrarte.",
                message_type="error",
            )

        user_exists = Usuario.query.filter_by(email=email).first()
        if user_exists:
            return render_template(
                "registro.html",
                message="Ese correo ya esta registrado.",
                message_type="error",
            )

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
            rol=ROLE_CLIENTE,
        )
        db.session.add(usuario)
        db.session.commit()
        return render_template(
            "registro.html",
            message="Cuenta creada correctamente.",
            message_type="success",
        )

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = normalize_email(request.form.get("email"))
        password = request.form.get("password") or ""

        if not email or not password:
            return render_template(
                "login.html",
                message="Ingresa correo y contrasena.",
                message_type="error",
            )

        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not check_password_hash(usuario.password_hash, password):
            return render_template(
                "login.html",
                message="Credenciales invalidas.",
                message_type="error",
            )

        session["user_id"] = usuario.id
        session["user_role"] = usuario.rol
        session["user_name"] = usuario.nombre
        return redirect(url_for(resolve_home_endpoint_by_role(usuario.rol)))

    return render_template("login.html")


@app.cli.command("create-admin")
@click.option("--creator-email", required=True, help="Correo del admin que autoriza.")
@click.option("--creator-password", required=True, help="Contrasena del admin que autoriza.")
@click.option("--nombre", required=True, help="Nombre del nuevo admin.")
@click.option("--email", required=True, help="Correo del nuevo admin.")
@click.option("--password", required=True, help="Contrasena del nuevo admin.")
def create_admin(creator_email, creator_password, nombre, email, password):
    creator_email = normalize_email(creator_email)
    email = normalize_email(email)

    creator = Usuario.query.filter_by(email=creator_email).first()
    if not creator or creator.rol != ROLE_ADMIN:
        raise click.ClickException("Solo un admin existente puede crear otro admin.")

    if not check_password_hash(creator.password_hash, creator_password):
        raise click.ClickException("Credenciales del admin creador invalidas.")

    if Usuario.query.filter_by(email=email).first():
        raise click.ClickException("El correo del nuevo admin ya existe.")

    nuevo_admin = Usuario(
        nombre=nombre.strip(),
        email=email,
        password_hash=generate_password_hash(password),
        rol=ROLE_ADMIN,
    )
    db.session.add(nuevo_admin)
    db.session.commit()
    click.echo(f"Admin creado correctamente: {email}")


@app.post("/api/ia/chat")
def ia_chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Debes enviar un mensaje."}), 400

    try:
        response = generate_response(message)
    except Exception as exc:
        return jsonify({"error": f"Error usando GPT4All: {exc}"}), 500

    return jsonify({"reply": response.strip()})


if __name__ == "__main__":
    app.run(debug=True)
