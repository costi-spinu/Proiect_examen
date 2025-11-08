# J_MeniuPrincipal.py
import os
from C_MeniuAngajati import MeniuAngajati
from F_MeniuMasini import MeniuMasini
from I_MeniuVanzari import MeniuVanzari
from J_autentificare import login, change_password


class MeniuPrincipal:
    """Meniu principal cu autentificare și roluri."""

    def __init__(self):
        self.meniu_angajati = MeniuAngajati()
        self.meniu_masini = MeniuMasini()
        self.meniu_vanzari = MeniuVanzari()
        self.user = None  # va stoca utilizatorul curent (dict)

    def afiseaza_meniu(self):
        # login la pornire
        self.user = login()
        role = self.user["role"]

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("\n" + "=" * 60)
            print(f"🚗 SISTEM GESTIONARE AUTO - ({role.upper()})")

            print("1. Gestionare angajați")
            print("2. Gestionare mașini")
            print("3. Gestionare vânzări")
            print("4. Schimbă parola")
            print("5. Ieșire")

            opt = input("Alege o opțiune (1-5): ").strip()

            if opt == "1":
                if role == "admin":
                    self.meniu_angajati.meniu()
                else:
                    print("Acces restricționat. Doar adminul poate modifica angajații.")
                    input("Apasă Enter pentru a continua...")

            elif opt == "2":
                self.meniu_masini.meniu()

            elif opt == "3":
                self.meniu_vanzari.meniu()

            elif opt == "4":
                change_password(self.user["username"])

            elif opt == "5":
                print("\n💾 Se salvează toate datele...")
                print("✅ Datele au fost salvate. 👋 La revedere!")
                break

            else:
                print("⚠️ Opțiune invalidă. Reîncearcă!")
                input("Apasă Enter pentru a continua...")


# -------------------------------
# Punct de pornire
# -------------------------------
if __name__ == "__main__":
    app = MeniuPrincipal()
    app.afiseaza_meniu()
