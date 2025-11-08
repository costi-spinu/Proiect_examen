from datetime import datetime
from typing import Dict, Any


class Masina:
    """Clasă pentru gestionarea datelor unei mașini."""

    contor_ID = 0  # contor global pentru ID-uri mașini

    def __init__(
        self,
        fabricatie: str = "",
        anul: int = 0,
        model: str = "",
        pret_cost: float = 0.0,
        potential_pret_vanzare: float = 0.0,
        nr_inmatriculare: str = "",
    ):
        Masina.contor_ID += 1
        self.ID = f"CAR-{Masina.contor_ID:03d}"
        self.fabricatie = fabricatie
        self.anul = anul
        self.model = model
        self.pret_cost = pret_cost
        self.potential_pret_vanzare = potential_pret_vanzare
        self.nr_inmatriculare = nr_inmatriculare

    def creare_dictionar(self) -> Dict[str, Any]:
        """Creează un dicționar cu datele mașinii."""
        return {
            "id": self.ID,
            "fabricatie": self.fabricatie,
            "anul": self.anul,
            "model": self.model,
            "pret_cost": self.pret_cost,
            "potential_pret_vanzare": self.potential_pret_vanzare,
            "nr_inmatriculare": self.nr_inmatriculare,
        }

    def introducere_date(self):
        """Introduce datele mașinii (ID se generează automat)."""
        print("\n=== INTRODUCERE DATE MAȘINĂ ===")
        campuri = {
            "fabricatie": "Producător (ex: Dacia, Toyota)",
            "anul": "An fabricație",
            "model": "Model",
            "pret_cost": "Preț de achiziție (€)",
            "potential_pret_vanzare": "Preț potențial de vânzare (€)",
            "nr_inmatriculare": "Numar de inmatriculare",
        }

        for atribut, mesaj in campuri.items():
            valoare = ""
            while not valoare:
                valoare = input(f"{mesaj}: ").strip()
                if not valoare:
                    print(" Câmp obligatoriu!")

            # Validări simple:
            if atribut == "anul":
                try:
                    valoare = int(valoare)
                    an_curent = datetime.now().year
                    if valoare < 1900 or valoare > an_curent + 1:
                        print("An invalid! Reintroduceți.")
                        return self.introducere_date()
                except ValueError:
                    print(" Trebuie să fie un număr.")
                    return self.introducere_date()
            elif atribut in ["pret_cost", "potential_pret_vanzare"]:
                try:
                    valoare = float(valoare)
                except ValueError:
                    print(" Trebuie să fie o valoare numerică (ex: 25000.00).")
                    return self.introducere_date()

            setattr(self, atribut, valoare)

        print(f"ID generat automat: {self.ID}")

    def __str__(self):
        return (
            f"{self.ID} | {self.fabricatie} {self.model} ({self.anul}) | "
            f"Achiziție: {self.pret_cost:.2f} € | "
            f"Vânzare potențială: {self.potential_pret_vanzare:.2f} €"
        )
