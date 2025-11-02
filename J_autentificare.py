# K_auth.py
import json
import os
import hashlib
import secrets
from getpass import getpass

AUTH_FILE = "auth.json"


# ------------------------------
# Funcții interne
# ------------------------------
def _hash_password(password: str, salt: str) -> str:
    """Generează un hash SHA256 pentru o parolă + salt."""
    h = hashlib.sha256()
    h.update((salt + password).encode("utf-8"))
    return h.hexdigest()


def _load_auth_data() -> dict:
    if not os.path.exists(AUTH_FILE):
        return {"users": []}
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users": []}


def _save_auth_data(data: dict):
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ------------------------------
# Creare conturi
# ------------------------------
def create_user(role: str):
    """Creează un cont de utilizator nou (admin sau user)."""
    data = _load_auth_data()

    print(f"\n=== Creare cont {role.upper()} ===")
    username = input(f"Nume utilizator ({role}): ").strip().lower()
    while True:
        p1 = getpass("Introdu parola: ")
        p2 = getpass("Confirmă parola: ")
        if p1 != p2:
            print("⚠️ Parolele nu coincid.")
        elif len(p1) < 6:
            print("⚠️ Parola trebuie să aibă cel puțin 6 caractere.")
        else:
            break

    salt = secrets.token_hex(16)
    password_hash = _hash_password(p1, salt)

    # verifică duplicate
    for u in data["users"]:
        if u["username"] == username:
            print("❌ Utilizatorul există deja.")
            return

    data["users"].append({
        "username": username,
        "role": role,
        "salt": salt,
        "password_hash": password_hash
    })

    _save_auth_data(data)
    print(f"✅ Contul {role} '{username}' a fost creat cu succes!")


def setup_default_users():
    """Creează conturile inițiale dacă nu există."""
    data = _load_auth_data()
    if not data["users"]:
        print("⚙️ Nu există utilizatori. Vom crea conturile inițiale.")
        create_user("admin")
        create_user("user")
    else:
        print("✔️ Utilizatorii există deja.")


# ------------------------------
# Autentificare
# ------------------------------
def login() -> dict:
    """Autentificare și returnare informații utilizator."""
    setup_default_users()
    data = _load_auth_data()

    print("\n=== Autentificare ===")
    for attempt in range(3):
        username = input("Nume utilizator: ").strip().lower()
        password = getpass("Parola: ").strip()

        for u in data["users"]:
            if u["username"] == username:
                calc_hash = _hash_password(password, u["salt"])
                if calc_hash == u["password_hash"]:
                    print(f"✅ Autentificare reușită! Bine ai venit, {username} ({u['role']}).")
                    return u
        print("❌ Nume sau parolă incorectă.\n")

    print("⛔ Prea multe încercări eșuate. Acces refuzat.")
    exit()


# ------------------------------
# Schimbare parolă
# ------------------------------
def change_password(username: str):
    """Schimbă parola unui utilizator existent."""
    data = _load_auth_data()
    user = next((u for u in data["users"] if u["username"] == username), None)
    if not user:
        print("❌ Utilizator inexistent.")
        return

    print("\n=== Schimbare parolă ===")
    old_pass = getpass("Parola actuală: ").strip()
    if _hash_password(old_pass, user["salt"]) != user["password_hash"]:
        print("❌ Parola actuală este incorectă.")
        return

    while True:
        p1 = getpass("Noua parolă: ")
        p2 = getpass("Confirmă noua parolă: ")
        if p1 != p2:
            print("⚠️ Parolele nu coincid.")
        elif len(p1) < 6:
            print("⚠️ Parola trebuie să aibă cel puțin 6 caractere.")
        else:
            break

    new_salt = secrets.token_hex(16)
    user["salt"] = new_salt
    user["password_hash"] = _hash_password(p1, new_salt)
    _save_auth_data(data)
    print("✅ Parola a fost schimbată cu succes.")
