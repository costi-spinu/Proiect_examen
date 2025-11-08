from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class ListaAngajati:

    ID: str
    nume: str
    prenume: str
    ocupatie: str
    nrTelefon: str
    email: str
    adresa: str

    def creare_dictionar(self):
        return asdict(self)

    @staticmethod
    def din_dict(d: dict):

        return ListaAngajati(
            ID=d["id"] if "id" in d else d["ID"],
            nume=d["nume"],
            prenume=d["prenume"],
            ocupatie=d["ocupatie"],
            nrTelefon=d["telefon"] if "telefon" in d else d["nrTelefon"],
            email=d["email"],
            adresa=d["adresa"],
        )


@dataclass
class Masina:

    ID: str
    fabricatie: str
    anul: int
    model: str
    pret_cost: float
    potential_pret_vanzare: float
    nr_inmatriculare: str

    def creare_dictionar(self) -> Dict:

        return {
            "id": self.ID,
            "fabricatie": self.fabricatie,
            "anul": self.anul,
            "model": self.model,
            "pret_cost": self.pret_cost,
            "potential_pret_vanzare": self.potential_pret_vanzare,
            "nr_inmatriculare": self.nr_inmatriculare,
        }

    @staticmethod
    def din_dict(d: Dict) -> "Masina":
        return Masina(
            ID=d["id"],
            fabricatie=d["fabricatie"],
            anul=d["anul"],
            model=d["model"],
            pret_cost=d["pret_cost"],
            potential_pret_vanzare=d["potential_pret_vanzare"],
            nr_inmatriculare=d.get("nr_inmatriculare", "").upper(),
        )


@dataclass
class Vanzare:

    data: str
    angajat_id: str
    angajat_nume: str
    masina_id: str
    masina_model: str
    profit: float

    def creare_dictionar(self) -> Dict:

        return {
            "data": self.data,
            "angajat_id": self.angajat_id,
            "angajat_nume": self.angajat_nume,
            "masina_id": self.masina_id,
            "masina_model": self.masina_model,
            "profit": self.profit,
        }

    @staticmethod
    def din_dict(d: Dict) -> "Vanzare":

        return Vanzare(
            data=d["data"],
            angajat_id=d["angajat_id"],
            angajat_nume=d["angajat_nume"],
            masina_id=d["masina_id"],
            masina_model=d["masina_model"],
            profit=d["profit"],
        )
