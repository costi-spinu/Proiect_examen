from D_Masini import Masina
import json
from typing import List, Optional


def print_masina(masina: Masina) -> None:
    """Afișează o mașină pe un singur rând."""
    print(
        f"ID: {masina.ID} | "
        f"{masina.fabricatie} {masina.model} ({masina.anul}) | "
        f"Cost: {masina.pret_cost:.2f} € | "
        f"Vânzare: {masina.potential_pret_vanzare:.2f} € | "
        f"Numar Inmatriculare: {masina.nr_inmatriculare} "
    )


class GestionareMasini:
    """Clasă pentru gestionarea unei colecții de mașini."""

    def __init__(self, fisier: str = "masini.json"):
        self.masini: List[Masina] = []
        self.fisier = fisier

    # === Adăugare ===
    def adauga_masina(self, masina: Optional[Masina] = None):
        if masina is None:
            masina = Masina()
            masina.introducere_date()
        self.masini.append(masina)
        print(
            f"Mașina {masina.ID} ({masina.nr_inmatriculare}) a fost adăugată cu succes."
        )

    # === Afișare ===
    def afiseaza_masini(self):
        if not self.masini:
            print("Nu există mașini înregistrate.")
            return
        print("\n=== LISTA MAȘINILOR ===")
        for m in self.masini:
            print_masina(m)

    # === Căutare ===
    def cauta_masina(self, criteriu: str):
        """Caută mașini după număr de înmatriculare, ID, model sau fabricatie."""
        rezultate = [
            m
            for m in self.masini
            if criteriu.lower() in m.nr_inmatriculare.lower()
            or criteriu.lower() in m.ID.lower()
            or criteriu.lower() in m.model.lower()
            or criteriu.lower() in m.fabricatie.lower()
        ]
        if rezultate:
            print("\n=== REZULTATE CĂUTARE ===")
            for m in rezultate:
                print_masina(m)
        else:
            print(f"Nicio mașină găsită pentru: '{criteriu}'.")

    # === Ștergere ===
    def sterge_masina(self, nr_masina: str):
        """Șterge o mașină după numărul de înmatriculare sau ID."""
        for m in self.masini:
            if (
                m.nr_inmatriculare.lower() == nr_masina.lower()
                or m.ID.lower() == nr_masina.lower()
            ):
                print_masina(m)
                confirm = (
                    input("Ești sigur că vrei să ștergi această mașină? (da/nu): ")
                    .strip()
                    .lower()
                )
                if confirm in ["da", "d"]:
                    self.masini.remove(m)
                    print(f"Mașina {m.nr_inmatriculare} a fost ștearsă.")
                else:
                    print("Ștergerea a fost anulată.")
                return
        print("Nu s-a găsit nicio mașină cu acest număr de înmatriculare sau ID.")

    # === Modificare ===
    def modifica_masina(self, criteriu: str):
        """Permite modificarea unui câmp ales de utilizator (după ID sau nr. înmatriculare)."""
        for m in self.masini:
            if (
                m.nr_inmatriculare.lower() == criteriu.lower()
                or m.ID.lower() == criteriu.lower()
            ):
                print("\n--- Modificare date mașină ---")
                print(
                    f"Selectată: {m.fabricatie} {m.model} ({m.anul}) | {m.nr_inmatriculare}"
                )

                while True:
                    print("\nCe dorești să modifici?")
                    print("1. Producător")
                    print("2. Model")
                    print("3. An fabricație")
                    print("4. Preț achiziție")
                    print("5. Preț potențial vânzare")
                    print("6. Număr înmatriculare")
                    print("7. Termină modificarea")
                    opt = input("Alege o opțiune (1-7): ").strip()

                    if opt == "1":
                        m.fabricatie = input("Nou producător: ").strip()
                        print("Producător actualizat.")
                    elif opt == "2":
                        m.model = input("Nou model: ").strip()
                        print("Model actualizat.")
                    elif opt == "3":
                        try:
                            m.anul = int(input("Nou an fabricație: ").strip())
                            print("An actualizat.")
                        except ValueError:
                            print("Valoare invalidă. Introdu un număr întreg.")
                    elif opt == "4":
                        try:
                            m.pret_cost = float(
                                input("Noul preț de achiziție (€): ").strip()
                            )
                            print("Preț de achiziție actualizat.")
                        except ValueError:
                            print("Valoare invalidă.")
                    elif opt == "5":
                        try:
                            m.potential_pret_vanzare = float(
                                input("Noul preț de vânzare (€): ").strip()
                            )
                            print("Preț de vânzare actualizat.")
                        except ValueError:
                            print("Valoare invalidă.")
                    elif opt == "6":
                        m.nr_inmatriculare = (
                            input("Noul număr de înmatriculare: ").strip().upper()
                        )
                        print("Număr de înmatriculare actualizat.")
                    elif opt == "7":
                        print("Modificarea a fost încheiată.")
                        return
                    else:
                        print("Opțiune invalidă. Reîncearcă!")

                return
        print("Nicio mașină găsită cu acest ID sau număr de înmatriculare.")

    # === Salvare/Încărcare ===
    def salvare_in_fisier(self, fisier: Optional[str] = None):
        """Salvează lista de mașini într-un fișier JSON."""
        if fisier is None:
            fisier = self.fisier
        with open(fisier, "w", encoding="utf-8") as f:
            json.dump(
                [m.creare_dictionar() for m in self.masini],
                f,
                indent=4,
                ensure_ascii=False,
            )
        print(f"Datele au fost salvate în '{fisier}'.")

    def incarca_din_fisier(self, fisier: Optional[str] = None):
        """Încarcă lista de mașini dintr-un fișier JSON."""
        if fisier is None:
            fisier = self.fisier
        try:
            with open(fisier, "r", encoding="utf-8") as f:
                date = json.load(f)
                self.masini = [
                    Masina(
                        fabricatie=e["fabricatie"],
                        anul=e["anul"],
                        model=e["model"],
                        pret_cost=e["pret_cost"],
                        potential_pret_vanzare=e["potential_pret_vanzare"],
                        nr_inmatriculare=e.get("nr_inmatriculare", ""),
                    )
                    for e in date
                ]
            print(f"{len(self.masini)} mașini încărcate din '{fisier}'.")
        except FileNotFoundError:
            print(f"Fișierul '{fisier}' nu există încă.")
