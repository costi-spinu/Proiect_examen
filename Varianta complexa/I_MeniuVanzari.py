import os
from B_ManagerAngajati import ManagerAngajati
from E_GestionareMasini import GestionareMasini
from H_GestionareVanzari import GestionareVanzari


class MeniuVanzari:
    """Meniu principal unitar pentru gestionarea angajaților, mașinilor și vânzărilor."""

    def __init__(self):
        # Fisierele implicite folosite pentru stocare
        self.fisier_angajati = "angajati.json"
        self.fisier_masini = "masini.json"
        self.fisier_vanzari = "vanzari.json"

        # Inițializare manageri
        self.manager_angajati = ManagerAngajati(self.fisier_angajati)
        self.manager_masini = GestionareMasini(self.fisier_masini)
        self.manager_vanzari = GestionareVanzari(self.fisier_vanzari)

        # Încarcă datele la pornire
        self.manager_angajati.incarca_din_fisier()
        self.manager_masini.incarca_din_fisier()
        self.manager_vanzari.incarca_din_fisier()

    # -------------------------------
    # Meniu principal
    # -------------------------------
    def meniu(self):
        while True:
            print("\n" + "=" * 60)
            print("🚗 SISTEM GESTIONARE AUTO - MENIU PRINCIPAL")
            print("=" * 60)
            print("1. Gestionare angajați")
            print("2. Gestionare mașini")
            print("3. Gestionare vânzări")
            print("4. Salvare manuală a tuturor datelor")
            print("5. Ieșire din program")
            print("=" * 60)

            opt = input("Alege o opțiune (1-5): ").strip()

            # === ANGAJAȚI ===
            if opt == "1":
                self.meniu_angajati()

            # === MAȘINI ===
            elif opt == "2":
                self.meniu_masini()

            # === VÂNZĂRI ===
            elif opt == "3":
                self.meniu_vanzari()

            # === SALVARE MANUALĂ ===
            elif opt == "4":
                self.salveaza_toate()
                print("💾 Toate fișierele au fost salvate cu succes!")

            # === IEȘIRE ===
            elif opt == "5":
                self.salveaza_toate()
                print("\n✅ Toate modificările au fost salvate.")
                print("👋 La revedere și o zi bună!")
                break

            else:
                print("⚠️ Opțiune invalidă. Reîncearcă!")

    # -------------------------------
    # Submeniuri (angajați, mașini, vânzări)
    # -------------------------------
    def meniu_angajati(self):
        """Apelează funcțiile din ManagerAngajati."""
        manager = self.manager_angajati
        while True:
            print("\n=== MENIU ANGAJAȚI ===")
            print("1. Adaugă angajat")
            print("2. Afișează toți angajații")
            print("3. Caută angajat (după ID, nume, prenume, telefon)")
            print("4. Modifică angajat")
            print("5. Șterge angajat")
            print("6. Înapoi la meniul principal")

            opt = input("Alege o opțiune (1-6): ").strip()

            if opt == "1":
                manager.adauga_angajat()
            elif opt == "2":
                manager.afiseaza_toti()
            elif opt == "3":
                termen = input("Introdu termenul de căutare: ").strip()
                manager.cauta_angajati(termen)
            elif opt == "4":
                id_angajat = input("Introdu ID-ul sau numele: ").strip()
                manager.modifica_angajat_dupa_nume(id_angajat)
            elif opt == "5":
                id_angajat = input("Introdu ID-ul sau numele: ").strip()
                manager.sterge_angajat_dupa_nume(id_angajat)
            elif opt == "6":
                manager.salveaza_in_fisier()
                print("🔙 Revenire la meniul principal.")
                break
            else:
                print("⚠️ Opțiune invalidă.")

    def meniu_masini(self):
        """Apelează funcțiile din GestionareMasini."""
        manager = self.manager_masini
        while True:
            print("\n=== MENIU MAȘINI ===")
            print("1. Adaugă mașină")
            print("2. Afișează toate mașinile")
            print("3. Caută mașină (după ID, model, producător sau nr. înmatriculare)")
            print("4. Modifică datele unei mașini")
            print("5. Șterge mașină")
            print("6. Înapoi la meniul principal")

            opt = input("Alege o opțiune (1-6): ").strip()

            if opt == "1":
                manager.adauga_masina()
            elif opt == "2":
                manager.afiseaza_masini()
            elif opt == "3":
                termen = input("Introdu termenul de căutare: ").strip()
                manager.cauta_masina(termen)
            elif opt == "4":
                criteriu = input("Introdu ID-ul sau nr. înmatriculare: ").strip()
                manager.modifica_masina(criteriu)
            elif opt == "5":
                criteriu = input("Introdu ID-ul sau nr. înmatriculare: ").strip()
                manager.sterge_masina(criteriu)
            elif opt == "6":
                manager.salvare_in_fisier()
                print("🔙 Revenire la meniul principal.")
                break
            else:
                print("⚠️ Opțiune invalidă.")

    def meniu_vanzari(self):
        """Apelează funcțiile din GestionareVanzari."""
        manager = self.manager_vanzari
        while True:
            print("\n=== MENIU VÂNZĂRI ===")
            print("1. Adaugă vânzare")
            print("2. Afișează toate vânzările")
            print("3. Caută vânzare")
            print("4. Modifică vânzare")
            print("5. Șterge vânzare")
            print("6. Cea mai vândută mașină într-o perioadă")
            print("7. Cel mai bun vânzător într-o perioadă")
            print("8. Profit total într-o perioadă")
            print("9. Înapoi la meniul principal")

            opt = input("Alege o opțiune (1-9): ").strip()

            if opt == "1":
                manager.adauga_vanzare()
            elif opt == "2":
                manager.afiseaza_vanzari()
            elif opt == "3":
                termen = input("Introdu termenul de căutare: ").strip()
                manager.cauta_vanzare(termen)
            elif opt == "4":
                manager.modifica_vanzare()
            elif opt == "5":
                manager.sterge_vanzare()
            elif opt == "6":
                start = input("Data de început (YYYY-MM-DD): ").strip()
                end = input("Data de sfârșit (YYYY-MM-DD): ").strip()
                print(manager.vanzari.cea_mai_vanduta_masina(start, end))
            elif opt == "7":
                start = input("Data de început (YYYY-MM-DD): ").strip()
                end = input("Data de sfârșit (YYYY-MM-DD): ").strip()
                print(manager.vanzari.cel_mai_bun_vanzator(start, end))
            elif opt == "8":
                start = input("Data de început (YYYY-MM-DD): ").strip()
                end = input("Data de sfârșit (YYYY-MM-DD): ").strip()
                total = manager.vanzari.profit_total_perioada(start, end)
                print(f"💰 Profit total în perioada {start} - {end}: {total:.2f} €")
            elif opt == "9":
                manager.salvare_in_fisier()
                print("🔙 Revenire la meniul principal.")
                break
            else:
                print("⚠️ Opțiune invalidă.")

    # -------------------------------
    # Salvare globală
    # -------------------------------
    def salveaza_toate(self):
        """Salvează toate fișierele într-un singur pas."""
        self.manager_angajati.salveaza_in_fisier()
        self.manager_masini.salvare_in_fisier()
        self.manager_vanzari.salvare_in_fisier()


# -------------------------------
# Punct de pornire
# -------------------------------
if __name__ == "__main__":
    app = MeniuVanzari()
    app.meniu()
