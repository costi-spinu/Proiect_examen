from typing import Dict, Any, List
from datetime import datetime
from D_Masini import Masina
from A_angajati import ListaAngajati


class Vanzari:
    """Gestionarea datelor despre vânzări."""

    def __init__(self):
        self.lista_vanzari: List[Dict[str, Any]] = []

    def adauga_vanzare(
        self,
        angajat: ListaAngajati,
        masina: Masina,
        profit: float,
        data_vanzare: str = None,
    ):
        """Adaugă o vânzare completă."""
        if data_vanzare is None:
            data_vanzare = datetime.now().strftime("%Y-%m-%d")

        vanzare = {
            "angajat_id": angajat.ID,
            "angajat_nume": f"{angajat.nume} {angajat.prenume}",
            "masina_id": masina.ID,
            "masina_model": f"{masina.fabricatie} {masina.model}",
            "profit": profit,
            "data": data_vanzare,
        }
        self.lista_vanzari.append(vanzare)

    def creare_dictionar(self) -> List[Dict[str, Any]]:
        """Returnează lista vânzărilor."""
        return self.lista_vanzari

    def filtreaza_dupa_perioada(
        self, data_start: str, data_end: str
    ) -> List[Dict[str, Any]]:
        """Returnează vânzările dintr-o perioadă."""
        start = datetime.strptime(data_start, "%Y-%m-%d")
        end = datetime.strptime(data_end, "%Y-%m-%d")
        return [
            v
            for v in self.lista_vanzari
            if start <= datetime.strptime(v["data"], "%Y-%m-%d") <= end
        ]

    def cea_mai_vanduta_masina(self, data_start: str, data_end: str) -> str:
        vanzari_perioada = self.filtreaza_dupa_perioada(data_start, data_end)
        if not vanzari_perioada:
            return "Nu există vânzări în această perioadă."

        frecventa: Dict[str, int] = {}
        for v in vanzari_perioada:
            model = v["masina_model"]
            frecventa[model] = frecventa.get(model, 0) + 1

        model_castigator = max(frecventa, key=frecventa.get)
        return f"Cea mai vândută mașină: {model_castigator} ({frecventa[model_castigator]} vânzări)"

    def cel_mai_bun_vanzator(self, data_start: str, data_end: str) -> str:
        vanzari_perioada = self.filtreaza_dupa_perioada(data_start, data_end)
        if not vanzari_perioada:
            return "Nu există vânzări în această perioadă."

        profituri: Dict[str, float] = {}
        for v in vanzari_perioada:
            id_angajat = v["angajat_id"]
            profituri[id_angajat] = profituri.get(id_angajat, 0) + v["profit"]

        id_castigator = max(profituri, key=profituri.get)
        nume_castigator = next(
            (
                v["angajat_nume"]
                for v in vanzari_perioada
                if v["angajat_id"] == id_castigator
            ),
            "Necunoscut",
        )
        profit_total = profituri[id_castigator]

        return f"Cel mai bun vânzător: {nume_castigator} ({id_castigator})  Profit total: {profit_total:.2f} €"

    def profit_total_perioada(self, data_start: str, data_end: str) -> float:
        vanzari_perioada = self.filtreaza_dupa_perioada(data_start, data_end)
        return sum(v["profit"] for v in vanzari_perioada)
