import os
import platform

from C_meniu_CLASE import MeniuAngajati, MeniuMasini, MeniuVanzari


def clear_screen():
    """Șterge ecranul în funcție de sistemul de operare."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class MeniuPrincipal:
    """Meniul principal al aplicației."""

    def __init__(self):
        self.meniu_angajati = MeniuAngajati()
        self.meniu_masini = MeniuMasini()
        self.meniu_vanzari = MeniuVanzari()

    def ruleaza(self):
        while True:
            clear_screen()
            print("\n==============================")
            print("     MENIUL PRINCIPAL")
            print("==============================")
            print("1. Gestionare angajați")
            print("2. Gestionare mașini")
            print("3. Gestionare vânzări")
            print("4. Ieșire")
            print("==============================")

            opt = input("Alege o opțiune (1-4): ").strip()

            if opt == "1":
                clear_screen()
                self.meniu_angajati.meniu()

            elif opt == "2":
                clear_screen()
                self.meniu_masini.meniu()

            elif opt == "3":
                clear_screen()
                self.meniu_vanzari.meniu()

            elif opt == "4":
                print("La revedere! 👋")
                break

            else:
                print("Opțiune invalidă! Încearcă din nou.")
                input("Apasă Enter pentru a continua...")


# ------------------------
# PUNCT DE PORNIRE
# ------------------------
if __name__ == "__main__":
    app = MeniuPrincipal()
    app.ruleaza()
