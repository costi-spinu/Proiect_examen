import os
from B_ManagerAngajati import ManagerAngajati


class MeniuAngajati:
    """Clasă care gestionează meniul interactiv pentru managerul de angajați"""

    @staticmethod
    def alege_fisier() -> str:
        """Permite utilizatorului să încarce sau să creeze un fișier nou"""
        print("=== GESTIONARE ANGAJAȚI ===\n")
        while True:
            print("1. Încarcă un fișier existent")
            print("2. Creează un fișier nou")
            opt = input("Alege o opțiune (1/2): ").strip()

            if opt == "1":
                nume = input("Introdu numele fișierului (ex: angajati.json): ").strip()
                if os.path.exists(nume):
                    print(f"Fișierul '{nume}' va fi folosit.")
                    return nume
                else:
                    print("Fișierul nu există. Încearcă din nou.")
            elif opt == "2":
                nume = input(
                    "Introdu numele noului fișier (ex: angajati_nou.json): "
                ).strip()
                if not nume.endswith(".json"):
                    nume += ".json"
                with open(nume, "w", encoding="utf-8") as f:
                    f.write("[]")
                print(f"✅ Fișierul '{nume}' a fost creat.")
                return nume
            else:
                print("Opțiune invalidă. Reîncearcă!")

    # -------------------------------
    # Meniul principal
    # -------------------------------
    def meniu(self):
        fisier_selectat = self.alege_fisier()
        manager = ManagerAngajati(fisier_selectat)

        while True:
            print("\n=== MENIU ANGAJAȚI ===")
            print("1. Adaugă angajat")
            print("2. Afișează toți angajații")
            print("3. Caută angajat (după nume, prenume, telefon sau ID)")
            print("4. Modifică datele unui angajat")
            print("5. Șterge angajat")
            print("6. Ieșire")

            opt = input("Alege o opțiune: ").strip()

            if opt == "1":
                manager.adauga_angajat()

            elif opt == "2":
                manager.afiseaza_toti()

            elif opt == "3":
                termen = input("Introdu termenul de căutare: ").strip()
                manager.cauta_angajati(termen)

            elif opt == "4":
                print("\nAlege metoda de modificare:")
                print("1. După ID(exemplu: ID-01)")
                print("2. După număr de telefon")
                print("3. După nume/prenume")
                selectie = input("Opțiune: ").strip()

                if selectie == "1":
                    id_angajat = input("Introdu ID-ul angajatului: ").strip()
                    manager.modifica_angajat_ID(id_angajat)
                elif selectie == "2":
                    nr_tel = input("Introdu numărul de telefon: ").strip()
                    manager.modifica_angajat_nr(nr_tel)
                elif selectie == "3":
                    nume = input("Introdu numele sau prenumele: ").strip()
                    manager.modifica_angajat_dupa_nume(nume)
                else:
                    print("Opțiune invalidă.")

            elif opt == "5":
                print("\nAlege metoda de ștergere:")
                print("1. După ID")
                print("2. După număr de telefon")
                print("3. După nume/prenume")
                selectie = input("Opțiune: ").strip()

                if selectie == "1":
                    id_angajat = input("Introdu ID-ul angajatului: ").strip()
                    manager.sterge_angajat_ID(id_angajat)
                elif selectie == "2":
                    nr_tel = input("Introdu numărul de telefon: ").strip()
                    manager.sterge_angajat_nr(nr_tel)
                elif selectie == "3":
                    nume = input("Introdu numele sau prenumele: ").strip()
                    manager.sterge_angajat_dupa_nume(nume)
                else:
                    print("Opțiune invalidă.")

            elif opt == "6":
                print("Fisierul se salveaza...")
                print("Fisierul a fost salvat...")
                print("La revedere!")
                break

            else:
                print("Opțiune invalidă!")


# -------------------------------
# Punct de pornire
# -------------------------------
if __name__ == "__main__":
    app = MeniuAngajati()
    app.meniu()
