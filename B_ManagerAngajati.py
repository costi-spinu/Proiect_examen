import json
import os
from typing import Dict, List
from A_angajati import ListaAngajati


# ======================
# Funcții ajutătoare afisare si scriere numar de telefon
# ======================


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
    """
    Curăță și validează numărul de telefon:
    - Elimină spații, cratime, paranteze.
    - Verifică dacă conține doar cifre.
    - Verifică lungimea (9-13 cifre).
    """
    curatat = (
        telefon.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    )

    if not curatat.isdigit():
        raise ValueError("Numărul de telefon trebuie să conțină doar cifre!")

    if len(curatat) < 9 or len(curatat) > 13:
        raise ValueError("❌ Numărul de telefon pare incorect (lungime invalidă)!")

    return curatat


# ======================
# Clasa principală
# ======================


class ManagerAngajati:
    def __init__(self, fisier="angajati.json"):
        self.fisier = fisier
        self.angajati: List[Dict] = self.incarca_din_fisier()

        # actualizare counter pentru ID-uri existente
        if self.angajati:
            ListaAngajati.counter_ID = len(self.angajati)

    # -------------------
    # Operații fișier
    # -------------------

    def salveaza_in_fisier(self):
        with open(self.fisier, "w", encoding="utf-8") as f:
            json.dump(self.angajati, f, indent=4, ensure_ascii=False)

    def incarca_din_fisier(self) -> List[Dict]:
        try:
            with open(self.fisier, "r", encoding="utf-8") as f:
                print(f"Fișierul '{self.fisier}' a fost încărcat cu succes.")
                return json.load(f)
        except FileNotFoundError:
            print(f"Fișierul '{self.fisier}' nu există. Va fi creat unul nou.")
            self.salveaza_in_fisier()
            return []

    # -------------------
    # Adăugare angajat
    # -------------------

    def adauga_angajat(self):
        """Adaugă un angajat nou, cu validare și verificare de duplicate"""
        ang = ListaAngajati()
        ang.introducere_date()

        # Curățare și validare telefon
        try:
            ang.nrTelefon = curata_telefon(ang.nrTelefon)
        except ValueError as err:
            print(err)
            return

        # Validare email simplă
        if "@" not in ang.email or "." not in ang.email:
            print("Adresa de email este invalidă.")
            return

        # Verificare duplicate (telefon / email)
        for e in self.angajati:
            if curata_telefon(e["telefon"]) == ang.nrTelefon:
                print(
                    f"Numărul de telefon {ang.nrTelefon} există deja (ID: {e['id']})."
                )
                return
            if e["email"].lower() == ang.email.lower():
                print(f"E-mailul {ang.email} există deja (ID: {e['id']}).")
                return

        self.angajati.append(ang.creare_dictionar())
        self.salveaza_in_fisier()
        print("Angajat adăugat cu succes!")

    # -------------------
    # Afișare / Căutare
    # -------------------

    def afiseaza_toti(self):
        if not self.angajati:
            print("Nu există angajați înregistrați.")
            return
        print("\n=== LISTA ANGAJAȚI ===")
        for e in self.angajati:
            print_employee(e)

    def cauta_angajati(self, termen: str) -> List[Dict]:
        """Caută angajați după ID, nume, prenume sau telefon"""
        gasiti = [
            e
            for e in self.angajati
            if termen.lower() in e["id"].lower()
            or termen.lower() in e["nume"].lower()
            or termen.lower() in e["prenume"].lower()
            or termen.lower() in e["telefon"].lower()
        ]
        if gasiti:
            print(f"\n Rezultate pentru '{termen}':")
            for e in gasiti:
                print_employee(e)
        else:
            print(" Niciun angajat găsit.")
        return gasiti

    # -------------------
    # Ștergere angajat
    # -------------------

    def sterge_angajat_ID(self, id_angajat: str):
        """Șterge un angajat după ID, doar după confirmare"""
        for e in self.angajati:
            if e["id"].lower() == id_angajat.lower().strip():
                print("\n=== ANGAJAT GĂSIT ===")
                print_employee(e)
                print(
                    "\nATENȚIE: ID-ul este unic și odată șters, nu va mai putea fi refolosit!"
                )
                confirm = (
                    input("Ești sigur că vrei să ștergi acest angajat? (da/nu): ")
                    .strip()
                    .lower()
                )
                if confirm in ["da", "d"]:
                    self.angajati.remove(e)
                    self.salveaza_in_fisier()
                    print(f"Angajatul cu ID {id_angajat} a fost șters definitiv.")
                else:
                    print("Ștergerea a fost anulată.")
                return
        print("ID-ul nu a fost găsit.")

    def sterge_angajat_nr(self, telefon: str):
        """Șterge un angajat după număr de telefon, cu confirmare"""
        for e in self.angajati:
            if e["telefon"].lower().strip() == telefon.lower().strip():
                print("\n=== ANGAJAT GĂSIT ===")
                print_employee(e)
                print(
                    "\nATENȚIE: ID-ul este unic și nu va mai fi refolosit după ștergere!"
                )
                confirm = (
                    input("Ești sigur că vrei să ștergi acest angajat? (da/nu): ")
                    .strip()
                    .lower()
                )
                if confirm in ["da", "d"]:
                    self.angajati.remove(e)
                    self.salveaza_in_fisier()
                    print(f"Angajatul cu telefonul {telefon} a fost șters definitiv.")
                else:
                    print("Ștergerea a fost anulată.")
                return
        print(f"Niciun angajat cu numărul {telefon} nu a fost găsit.")

    def sterge_angajat_dupa_nume(self, nume_sau_prenume: str):
        """Șterge un angajat după nume sau prenume, cu confirmare"""
        gasiti = [
            e
            for e in self.angajati
            if nume_sau_prenume.lower() in e["nume"].lower()
            or nume_sau_prenume.lower() in e["prenume"].lower()
        ]
        if not gasiti:
            print("Nu s-a găsit niciun angajat cu acest nume.")
            return

        if len(gasiti) > 1:
            print("Mai mulți angajați găsiți:")
            for e in gasiti:
                print_employee(e)
            id_selectat = input("Introdu ID-ul celui de șters: ").strip()
            for e in gasiti:
                if e["id"].lower() == id_selectat.lower():
                    print("\n=== ANGAJAT SELECTAT ===")
                    print_employee(e)
                    print(
                        "\nATENȚIE: ID-ul este unic și nu va mai fi refolosit după ștergere!"
                    )
                    confirm = (
                        input("Ești sigur că vrei să ștergi acest angajat? (da/nu): ")
                        .strip()
                        .lower()
                    )
                    if confirm in ["da", "d"]:
                        self.angajati.remove(e)
                        self.salveaza_in_fisier()
                        print(f"Angajatul {id_selectat} a fost șters definitiv.")
                    else:
                        print("Ștergerea a fost anulată.")
                    return
            print("ID invalid.")
        else:
            e = gasiti[0]
            print("\n=== ANGAJAT GĂSIT ===")
            print_employee(e)
            print("\nATENȚIE: ID-ul este unic și nu va mai fi refolosit după ștergere!")
            confirm = (
                input("Ești sigur că vrei să ștergi acest angajat? (da/nu): ")
                .strip()
                .lower()
            )
            if confirm in ["da", "d"]:
                self.angajati.remove(e)
                self.salveaza_in_fisier()
                print(f"Angajatul {e['nume']} {e['prenume']} a fost șters definitiv.")
            else:
                print("Ștergerea a fost anulată.")

    # -------------------
    # Modificare angajat
    # -------------------

    def modifica_angajat_ID(self, id_angajat: str):
        for e in self.angajati:
            if e["id"].lower() == id_angajat.lower():
                self._modifica_date_angajat(e)
                return
        print("ID-ul introdus nu există.")

    def modifica_angajat_nr(self, telefon: str):
        try:
            telefon_curat = curata_telefon(telefon)
        except ValueError as err:
            print(err)
            return

        for e in self.angajati:
            if curata_telefon(e["telefon"]) == telefon_curat:
                self._modifica_date_angajat(e)
                return
        print("Numărul de telefon introdus nu există.")

    def modifica_angajat_dupa_nume(self, nume_sau_prenume: str):
        gasiti = [
            e
            for e in self.angajati
            if nume_sau_prenume.lower() in e["nume"].lower()
            or nume_sau_prenume.lower() in e["prenume"].lower()
        ]
        if not gasiti:
            print("Nu s-a găsit niciun angajat cu acest nume sau prenume.")
            return

        if len(gasiti) > 1:
            print("Mai mulți angajați găsiți:")
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

    # -------------------
    # Funcție internă (modificare date)
    # -------------------

    def _modifica_date_angajat(self, e: Dict):
        """Funcție internă folosită pentru modificarea câmpurilor unui angajat"""
        print("\n=== MODIFICARE ANGAJAT ===")
        print_employee(e)

        campuri = {
            "nume": "Nume",
            "prenume": "Prenume",
            "ocupatie": "Ocupatie",
            "telefon": "Telefon",
            "email": "E-mail",
            "adresa": "Adresa",
        }

        for atribut, mesaj in campuri.items():
            val_noua = input(f"{mesaj} ({e[atribut]}): ").strip()
            if val_noua:
                if atribut == "telefon":
                    try:
                        val_noua = curata_telefon(val_noua)
                    except ValueError as err:
                        print(err)
                        continue
                e[atribut] = val_noua

        self.salveaza_in_fisier()
        print("Datele au fost actualizate cu succes!")
