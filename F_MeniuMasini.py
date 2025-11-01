import os
from E_GestionareMasini import GestionareMasini


class MeniuMasini:

    @staticmethod
    def alege_fisier() -> str:
        """Permite utilizatorului să încarce sau să creeze un fișier nou."""
        print("=== GESTIONARE DATE MAȘINI ===\n")
        while True:
            print("1. Încarcă un fișier existent")
            print("2. Creează un fișier nou")
            opt = input("Alege o opțiune (1/2): ").strip()

            if opt == "1":
                nume = input("Introdu numele fișierului (ex: masini.json): ").strip()
                if os.path.exists(nume):
                    print(f"Fișierul '{nume}' va fi folosit.")
                    return nume
                else:
                    print("Fișierul nu există. Încearcă din nou.")
            elif opt == "2":
                nume = input(
                    "Introdu numele noului fișier (ex: listaNouaMasini.json): "
                ).strip()
                if not nume.endswith(".json"):
                    nume += ".json"
                with open(nume, "w", encoding="utf-8") as f:
                    f.write("[]")
                print(f"Fișierul '{nume}' a fost creat.")
                return nume
            else:
                print("Opțiune invalidă. Reîncearcă!")

    # -------------------------------
    # Meniul principal
    # -------------------------------
    def meniu(self):
        fisier_selectat = self.alege_fisier()
        manager = GestionareMasini(fisier_selectat)
        manager.incarca_din_fisier()

        print(f"\nFișierul '{fisier_selectat}' a fost încărcat cu succes.")

        while True:
            print("\n" + "=" * 40)
            print("MENIU PRINCIPAL - GESTIONARE MAȘINI ")
            print("=" * 40)
            print("1. Adaugă mașină")
            print("2. Afișează toate mașinile")
            print("3. Caută mașină (după ID, model, producător sau nr. înmatriculare)")
            print("4. Modifică datele unei mașini (după ID sau nr. înmatriculare)")
            print("5. Șterge o mașină (după ID sau nr. înmatriculare)")
            print("6. Salvează și ieși")

            opt = input("Alege o opțiune: ").strip()

            if opt == "1":
                manager.adauga_masina()
                manager.salvare_in_fisier()

            elif opt == "2":
                manager.afiseaza_masini()

            elif opt == "3":
                termen = input("Introdu termenul de căutare: ").strip()
                manager.cauta_masina(termen)

            elif opt == "4":
                criteriu = input("Introdu ID-ul sau nr. de înmatriculare: ").strip()
                manager.modifica_masina(criteriu)
                manager.salvare_in_fisier()

            elif opt == "5":
                criteriu = input("Introdu ID-ul sau nr. de înmatriculare: ").strip()
                manager.sterge_masina(criteriu)
                manager.salvare_in_fisier()

            elif opt == "6":
                manager.salvare_in_fisier()
                print("Datele au fost salvate. La revedere! 👋")
                break

            else:
                print("Opțiune invalidă. Reîncearcă!")


# -------------------------------
# Punct de pornire
# -------------------------------
if __name__ == "__main__":
    app = MeniuMasini()
    app.meniu()
