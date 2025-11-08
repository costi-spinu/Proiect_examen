import json
from typing import List, Optional
from datetime import datetime
from G_Vanzari import Vanzari
from D_Masini import Masina
from A_angajati import ListaAngajati


def print_vanzare(v: dict) -> None:
    """Afișează o vânzare pe un singur rând."""
    print(
        f"Data: {v['data']} | "
        f"Angajat: {v['angajat_nume']} ({v['angajat_id']}) | "
        f"Mașină: {v['masina_model']} ({v['masina_id']}) | "
        f"Profit: {v['profit']:.2f} €"
    )


class GestionareVanzari:
    """Clasă pentru gestionarea colecției de vânzări."""

    def __init__(self, fisier: str = "vanzari.json"):
        self.vanzari = Vanzari()
        self.fisier = fisier

    # === Adăugare ===
    def adauga_vanzare(self):
        print("\n=== Adăugare vânzare ===")
        angajat = ListaAngajati(
            input("Nume: "),
            input("Prenume: "),
            input("Ocupație: "),
            input("Telefon: "),
            input("Email: "),
            input("Adresă: "),
        )

        masina = Masina(
            input("Producător: "),
            int(input("An fabricație: ")),
            input("Model: "),
            float(input("Preț achiziție (€): ")),
            float(input("Preț vânzare (€): ")),
            input("Număr înmatriculare: "),
        )

        profit = float(input("Profit obținut (€): "))
        data = input("Data vânzării (YYYY-MM-DD): ").strip() or datetime.now().strftime("%Y-%m-%d")

        self.vanzari.adauga_vanzare(angajat, masina, profit, data)
        print("✅ Vânzare adăugată cu succes!")

    # === Afișare ===
    def afiseaza_vanzari(self):
        if not self.vanzari.lista_vanzari:
            print("⚠️ Nu există vânzări înregistrate.")
            return
        print("\n=== LISTA VÂNZĂRILOR ===")
        for v in self.vanzari.lista_vanzari:
            print_vanzare(v)

    # === Căutare ===
    def cauta_vanzare(self, termen: str):
        rezultate = [
            v
            for v in self.vanzari.lista_vanzari
            if termen.lower() in v["angajat_nume"].lower()
            or termen.lower() in v["masina_model"].lower()
            or termen.lower() in v["masina_id"].lower()
        ]
        if rezultate:
            print("\n=== REZULTATE CĂUTARE ===")
            for v in rezultate:
                print_vanzare(v)
        else:
            print(f"Nicio vânzare găsită pentru: '{termen}'.")

    # === Modificare ===
    def modifica_vanzare(self):
        criteriu = input("Introdu ID-ul mașinii sau al angajatului: ").strip()
        for v in self.vanzari.lista_vanzari:
            if criteriu.lower() in (v["masina_id"].lower(), v["angajat_id"].lower()):
                print_vanzare(v)
                print("\nCe dorești să modifici?")
                print("1. Profit")
                print("2. Angajat")
                print("3. Mașină")
                opt = input("Alege o opțiune (1-3): ").strip()

                if opt == "1":
                    v["profit"] = float(input("Noul profit (€): "))
                    print("Profit actualizat.")
                elif opt == "2":
                    ang = ListaAngajati(
                        input("Nume: "),
                        input("Prenume: "),
                        input("Ocupație: "),
                        input("Telefon: "),
                        input("Email: "),
                        input("Adresă: "),
                    )
                    v["angajat_id"] = ang.ID
                    v["angajat_nume"] = f"{ang.nume} {ang.prenume}"
                    print("Angajat actualizat.")
                elif opt == "3":
                    masina = Masina(
                        input("Producător: "),
                        int(input("An fabricație: ")),
                        input("Model: "),
                        float(input("Preț achiziție (€): ")),
                        float(input("Preț vânzare (€): ")),
                        input("Număr înmatriculare: "),
                    )
                    v["masina_id"] = masina.ID
                    v["masina_model"] = f"{masina.fabricatie} {masina.model}"
                    print("Modelul mașinii actualizat.")
                else:
                    print("Opțiune invalidă.")
                return
        print("⚠️ Vânzare negăsită.")

    # === Ștergere ===
    def sterge_vanzare(self):
        criteriu = input("Introdu ID-ul mașinii sau al angajatului: ").strip()
        for v in self.vanzari.lista_vanzari:
            if criteriu.lower() in (v["masina_id"].lower(), v["angajat_id"].lower()):
                print_vanzare(v)
                confirm = input("Ești sigur că vrei să ștergi această vânzare? (da/nu): ").lower()
                if confirm in ["da", "d"]:
                    self.vanzari.lista_vanzari.remove(v)
                    print("🗑️ Vânzarea a fost ștearsă.")
                else:
                    print("Ștergerea anulată.")
                return
        print("⚠️ Nicio vânzare găsită.")

    # === Salvare / Încărcare ===
    def salvare_in_fisier(self, fisier: Optional[str] = None):
        if fisier is None:
            fisier = self.fisier
        with open(fisier, "w", encoding="utf-8") as f:
            json.dump(self.vanzari.lista_vanzari, f, indent=4, ensure_ascii=False)
        print(f"💾 Datele au fost salvate în '{fisier}'.")

    def incarca_din_fisier(self, fisier: Optional[str] = None):
        if fisier is None:
            fisier = self.fisier
        try:
            with open(fisier, "r", encoding="utf-8") as f:
                self.vanzari.lista_vanzari = json.load(f)
            print(f"📂 {len(self.vanzari.lista_vanzari)} vânzări încărcate din '{fisier}'.")
        except FileNotFoundError:
            print(f"⚠️ Fișierul '{fisier}' nu există încă.")
