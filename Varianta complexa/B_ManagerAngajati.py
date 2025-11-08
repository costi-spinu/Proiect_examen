import json
from typing import List, Dict
from A_angajati import ListaAngajati


def print_employee(e: Dict) -> None:
    """Afișează un angajat pe un singur rând"""
    print(
        f"ID: {e.get('id')}\t"
        f"Nume: {e.get('nume')} {e.get('prenume')}\t"
        f"Ocupatie: {e.get('ocupatie')}\t"
        f"Telefon: {e.get('telefon')}\t"
        f"E-mail: {e.get('email')}\t"
        f"Adresa: {e.get('adresa')}"
    )


def curata_telefon(telefon: str) -> str:
    """Curăță și validează numărul de telefon."""
    curatat = (
        telefon.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    )
    if not curatat.isdigit():
        raise ValueError("Numărul de telefon trebuie să conțină doar cifre!")
    if len(curatat) < 9 or len(curatat) > 13:
        raise ValueError("Număr de telefon invalid (lungime incorectă).")
    return curatat


class ManagerAngajati:
    """Gestionează adăugarea, modificarea și ștergerea angajaților."""

    def __init__(self, fisier: str = "angajati.json"):
        self.fisier = fisier
        self.angajati: List[Dict] = self.incarca_din_fisier()

        # actualizează contorul de ID-uri
        if self.angajati:
            ListaAngajati.counter_ID = len(self.angajati)

    # -------------------------
    # Operații cu fișierul JSON
    # -------------------------

    def salveaza_in_fisier(self):
        """Salvează lista de angajați în fișier JSON."""
        with open(self.fisier, "w", encoding="utf-8") as f:
            json.dump(self.angajati, f, indent=4, ensure_ascii=False)

    def incarca_din_fisier(self) -> List[Dict]:
        """Încarcă angajații din fișier, tratând fișiere goale sau corupte."""
        try:
            with open(self.fisier, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    print(
                        f"⚠️ Fișierul '{self.fisier}' este gol. Se va inițializa o listă nouă."
                    )
                    return []
                return json.loads(content)
        except FileNotFoundError:
            print(f"📄 Fișierul '{self.fisier}' nu există. Se va crea unul nou.")
            self.salveaza_in_fisier()
            return []
        except json.JSONDecodeError:
            print(f"⚠️ Fișierul '{self.fisier}' este corupt. A fost resetat.")
            self.salveaza_in_fisier()
            return []

    # -------------------------
    # Operații CRUD
    # -------------------------

    def adauga_angajat(self):
        """Adaugă un angajat nou."""
        ang = ListaAngajati()
        ang.introducere_date()

        # Validare telefon
        try:
            ang.nrTelefon = curata_telefon(ang.nrTelefon)
        except ValueError as err:
            print(err)
            return

        # Validare email
        if "@" not in ang.email or "." not in ang.email:
            print("Adresa de email este invalidă.")
            return

        # Verifică duplicate
        for e in self.angajati:
            if curata_telefon(e["telefon"]) == ang.nrTelefon:
                print(
                    f"⚠️ Numărul de telefon {ang.nrTelefon} există deja (ID: {e['id']})."
                )
                return
            if e["email"].lower() == ang.email.lower():
                print(f"⚠️ Emailul {ang.email} există deja (ID: {e['id']}).")
                return

        self.angajati.append(ang.creare_dictionar())
        self.salveaza_in_fisier()
        print("✅ Angajat adăugat cu succes!")

    def afiseaza_toti(self):
        """Afișează toți angajații existenți."""
        if not self.angajati:
            print("⚠️ Nu există angajați înregistrați.")
            return
        print("\n=== LISTA ANGAJAȚI ===")
        for e in self.angajati:
            print_employee(e)

    def cauta_angajati(self, termen: str) -> List[Dict]:
        """Caută angajați după ID, nume, prenume sau telefon."""
        gasiti = [
            e
            for e in self.angajati
            if termen.lower() in e["id"].lower()
            or termen.lower() in e["nume"].lower()
            or termen.lower() in e["prenume"].lower()
            or termen.lower() in e["telefon"].lower()
        ]
        if gasiti:
            print(f"\n🔍 Rezultate pentru '{termen}':")
            for e in gasiti:
                print_employee(e)
        else:
            print("❌ Niciun angajat găsit.")
        return gasiti

    def sterge_angajat_dupa_nume(self, nume_sau_prenume: str):
        """Șterge un angajat după nume sau prenume."""
        gasiti = [
            e
            for e in self.angajati
            if nume_sau_prenume.lower() in e["nume"].lower()
            or nume_sau_prenume.lower() in e["prenume"].lower()
        ]
        if not gasiti:
            print("❌ Nu s-a găsit niciun angajat cu acest nume.")
            return

        if len(gasiti) > 1:
            print("⚠️ Mai mulți angajați găsiți:")
            for e in gasiti:
                print_employee(e)
            id_selectat = input("Introdu ID-ul celui de șters: ").strip()
            for e in gasiti:
                if e["id"].lower() == id_selectat.lower():
                    confirm = (
                        input("Ești sigur că vrei să ștergi acest angajat? (da/nu): ")
                        .strip()
                        .lower()
                    )
                    if confirm in ["da", "d"]:
                        self.angajati.remove(e)
                        self.salveaza_in_fisier()
                        print(f"🗑️ Angajatul {e['nume']} {e['prenume']} a fost șters.")
                    else:
                        print("Operațiunea a fost anulată.")
                    return
        else:
            e = gasiti[0]
            confirm = (
                input(
                    f"Ești sigur că vrei să ștergi {e['nume']} {e['prenume']}? (da/nu): "
                )
                .strip()
                .lower()
            )
            if confirm in ["da", "d"]:
                self.angajati.remove(e)
                self.salveaza_in_fisier()
                print(f"🗑️ Angajatul {e['nume']} {e['prenume']} a fost șters.")
            else:
                print("Operațiunea a fost anulată.")

    def modifica_angajat_dupa_nume(self, nume_sau_prenume: str):
        """Modifică datele unui angajat existent."""
        gasiti = [
            e
            for e in self.angajati
            if nume_sau_prenume.lower() in e["nume"].lower()
            or nume_sau_prenume.lower() in e["prenume"].lower()
        ]
        if not gasiti:
            print("❌ Nu s-a găsit niciun angajat cu acest nume.")
            return

        if len(gasiti) > 1:
            print("⚠️ Mai mulți angajați găsiți:")
            for e in gasiti:
                print_employee(e)
            id_selectat = input("Introdu ID-ul celui de modificat: ").strip()
            for e in gasiti:
                if e["id"].lower() == id_selectat.lower():
                    self._modifica_date_angajat(e)
                    return
            print("ID invalid.")
        else:
            self._modifica_date_angajat(gasiti[0])

    def _modifica_date_angajat(self, e: Dict):
        """Permite modificarea câmpurilor unui angajat."""
        print("\n=== MODIFICARE ANGAJAT ===")
        print_employee(e)

        campuri = {
            "nume": "Nume",
            "prenume": "Prenume",
            "ocupatie": "Ocupație",
            "telefon": "Telefon",
            "email": "E-mail",
            "adresa": "Adresă",
        }

        for atribut, mesaj in campuri.items():
            noua_valoare = input(f"{mesaj} ({e[atribut]}): ").strip()
            if noua_valoare:
                if atribut == "telefon":
                    try:
                        noua_valoare = curata_telefon(noua_valoare)
                    except ValueError as err:
                        print(err)
                        continue
                e[atribut] = noua_valoare

        self.salveaza_in_fisier()
        print("✅ Datele au fost actualizate cu succes!")
