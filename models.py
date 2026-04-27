from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ROLE_CLIENTE = "cliente"
ROLE_ADMIN = "admin"
VALID_ROLES = (ROLE_CLIENTE, ROLE_ADMIN)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(
        db.Enum(*VALID_ROLES, name="usuarios_rol_enum", native_enum=True),
        nullable=False,
        default=ROLE_CLIENTE,
        server_default=ROLE_CLIENTE,
        index=True,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
