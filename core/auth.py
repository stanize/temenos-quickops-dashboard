from dataclasses import dataclass

@dataclass
class AuthResult:
    ok: bool
    message: str = ""

def dummy_validate(username: str, password: str) -> AuthResult:
    u = (username or "").strip()
    p = password or ""

    if not u:
        return AuthResult(False, "Username is required.")
    if p != "demo123":
        return AuthResult(False, "Invalid password (hint: demo123).")

    return AuthResult(True, "Login OK (dummy).")

