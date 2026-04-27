from flask import redirect, request, session, url_for

from models import ROLE_ADMIN, ROLE_CLIENTE

ROLE_TO_ENDPOINT = {
    ROLE_CLIENTE: "cliente",
    ROLE_ADMIN: "admin",
}

PROTECTED_ENDPOINT_ROLES = {
    "cliente": ROLE_CLIENTE,
    "admin": ROLE_ADMIN,
}

SKIPPED_ENDPOINTS = {"ia_chat", "create_admin"}
PUBLIC_AUTH_ENDPOINTS = {"login", "registro"}


def resolve_home_endpoint_by_role(role):
    return ROLE_TO_ENDPOINT.get(role, "login")


def register_role_middleware(app):
    @app.before_request
    def role_redirect_middleware():
        endpoint = request.endpoint
        if endpoint is None:
            return None

        if endpoint.startswith("static") or endpoint in SKIPPED_ENDPOINTS:
            return None

        role = session.get("user_role")

        if endpoint in PUBLIC_AUTH_ENDPOINTS and role in ROLE_TO_ENDPOINT:
            return redirect(url_for(resolve_home_endpoint_by_role(role)))

        required_role = PROTECTED_ENDPOINT_ROLES.get(endpoint)
        if required_role is None:
            return None

        if role is None:
            return redirect(url_for("login"))

        if role != required_role:
            return redirect(url_for(resolve_home_endpoint_by_role(role)))

        return None
