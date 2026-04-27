from flask import Flask, jsonify, render_template, request
from gpt4all import GPT4All

app = Flask(__name__)
SYSTEM_PROMPT = (
    "Eres un asistente virtual de la plataforma educativa Edunexo. "
    "Solo respondes en espanol, de forma breve (maximo 2 o 3 oraciones). "
    "No saludes ni te presentes al inicio. Simplemente responde la pregunta del usuario "
    "sin generar preguntas adicionales ni ejemplos de conversacion."
)
_model = None


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


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/ia")
def ia():
    return render_template("IA.html")


@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/login")
def login():
    return render_template("login.html")


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
