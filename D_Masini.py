from typing import Dict
from datetime import datetime


class Car:
    """Clasa pentru gestionarea datelor unei masini."""

    counter_ID = 0  # contor global pentru ID-uri masini

    def __init__(
        self,
        manufacturer: str = "",
        year: int = 0,
        model: str = "",
        cost_price: float = 0.0,
        potential_sale_price: float = 0.0,
    ):
        Car.counter_ID += 1
        self.ID = f"CAR-{Car.counter_ID:03d}"
        self.manufacturer = manufacturer
        self.year = year
        self.model = model
        self.cost_price = cost_price
        self.potential_sale_price = potential_sale_price

    def creare_dictionar(self) -> Dict:
        """Creeaza un dictionar cu datele masinii."""
        return {
            "id": self.ID,
            "manufacturer": self.manufacturer,
            "year": self.year,
            "model": self.model,
            "cost_price": self.cost_price,
            "potential_sale_price": self.potential_sale_price,
        }

    def introducere_date(self):
        """Introduce datele masinii (ID se genereaza automat)."""
        print("\n=== INTRODUCERE DATE MASINA ===")
        campuri = {
            "manufacturer": "Producator",
            "year": "An fabricatie",
            "model": "Model",
            "cost_price": "Pret de achizitie (€)",
            "potential_sale_price": "Pret potential de vanzare (€)",
        }

        for atribut, mesaj in campuri.items():
            valoare = ""
            while not valoare:
                valoare = input(f"{mesaj}: ").strip()
                if not valoare:
                    print(" Camp obligatoriu!")

            # Validari simple:
            if atribut == "year":
                try:
                    valoare = int(valoare)
                    current_year = datetime.now().year
                    if valoare < 1900 or valoare > current_year + 1:
                        print(" An invalid! Reintroduceti.")
                        return self.introducere_date()
                except ValueError:
                    print(" Trebuie sa fie un numar.")
                    return self.introducere_date()
            elif atribut in ["cost_price", "potential_sale_price"]:
                try:
                    valoare = float(valoare)
                except ValueError:
                    print(" Trebuie sa fie o valoare numerica (ex: 25000.00).")
                    return self.introducere_date()

            setattr(self, atribut, valoare)

        print(f" ID generat automat: {self.ID}")

    def __str__(self):
        return (
            f"{self.ID} | {self.manufacturer} {self.model} ({self.year}) | "
            f"Achizitie: {self.cost_price:.2f} € | "
            f"Vanzare potentiala: {self.potential_sale_price:.2f} €"
        )
