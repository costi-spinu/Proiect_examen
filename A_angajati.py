from typing import Dict


class ListaAngajati:
    """Clasa pentru gestionarea datelor unui angajat."""

    counter_ID = 0  # contor global pentru ID-uri

    def __init__(
        self,
        nume: str = "",
        prenume: str = "",
        ocupatie: str = "",
        nrTelefon: str = "",
        email: str = "",
        adresa: str = "",
    ):
        ListaAngajati.counter_ID += 1
        self.ID = f"ID-{ListaAngajati.counter_ID:02d}"
        self.nume = nume
        self.prenume = prenume
        self.ocupatie = ocupatie
        self.nrTelefon = nrTelefon
        self.email = email
        self.adresa = adresa

    def creare_dictionar(self) -> Dict:
        """Creare dicționar cu datele introduse"""
        return {
            "id": self.ID,
            "nume": self.nume,
            "prenume": self.prenume,
            "ocupatie": self.ocupatie,
            "telefon": self.nrTelefon,
            "email": self.email,
            "adresa": self.adresa,
        }

    def introducere_date(self):
        """Introducere date angajat (ID se generează automat)"""
        campuri = {
            "nume": "Nume",
            "prenume": "Prenume",
            "ocupatie": "Ocupatie",
            "nrTelefon": "Număr Telefon",
            "email": "E-mail",
            "adresa": "Adresa",
        }
        for atribut, mesaj in campuri.items():
            valoare = ""
            while not valoare:
                valoare = input(f"{mesaj}: ").strip()
                if not valoare:
                    print(" Camp obligatoriu!")
            setattr(self, atribut, valoare)

        print(f" ID generat automat: {self.ID}")

    def __str__(self):
        return (
            f"{self.ID} | {self.nume} {self.prenume} | {self.ocupatie} | "
            f"{self.nrTelefon} | {self.email} | {self.adresa}"
        )



    

   