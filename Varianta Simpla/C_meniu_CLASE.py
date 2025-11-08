from A_angajati_masini_vanzari import ListaAngajati, Masina, Vanzare
from B_manager_CLASE import SalvareJson, ManagerAngajati, ManagerMasini, ManagerVanzari
import os


def cere_input(mesaj: str, optional=False):
    """Ajutor simplu pentru a cere valori de la utilizator."""
    val = input(f"{mesaj}: ").strip()
    if not val and not optional:
        print("  Câmp obligatoriu!")
        return cere_input(mesaj, optional)
    return val


# ============================================================
# MENIU ANGAJATI
# ============================================================


class MeniuAngajati:

    def __init__(self):
        self.manager = ManagerAngajati("angajati.json")

    # ---------------------------------------------------
    # 1. Adăugare
    # ---------------------------------------------------
    def adauga(self):
        print("\n=== ADAUGĂ ANGAJAT ===")
        try:
            ang = self.manager.adauga_angajat(
                nume=cere_input("Nume"),
                prenume=cere_input("Prenume"),
                ocupatie=cere_input("Ocupatie"),
                telefon=cere_input("Telefon"),
                email=cere_input("Email"),
                adresa=cere_input("Adresă"),
            )
            print(f"Angajat adăugat: {ang.ID} {ang.nume} {ang.prenume}")
        except Exception as e:
            print("Eroare:", e)

    # ---------------------------------------------------
    # 2. Afișare
    # ---------------------------------------------------
    def afiseaza(self):
        print("\n=== LISTA ANGAJAȚILOR ===")
        angajati = self.manager.afiseaza_toti()
        if not angajati:
            print("Nu există angajați.")
            return

        for a in angajati:
            print(
                f"{a['ID']} | {a['nume']} {a['prenume']} | "
                f"{a['ocupatie']} | {a['nrTelefon']} | {a['email']} | {a['adresa']}"
            )

    # ---------------------------------------------------
    # 3. Căutare
    # ---------------------------------------------------
    def cauta(self):
        termen = cere_input("Introdu termenul căutat")
        rezultate = self.manager.cauta(termen)

        if not rezultate:
            print("Niciun angajat găsit.")
            return

        print("\n=== Rezultate căutare ===")
        for a in rezultate:
            print(
                f"{a['ID']} | {a['nume']} {a['prenume']} | "
                f"{a['ocupatie']} | {a['nrTelefon']} | {a['email']} | {a['adresa']}"
            )

    # ---------------------------------------------------
    # 4. Modificare (după telefon)
    # ---------------------------------------------------
    def modifica(self):
        tel = cere_input("Telefonul angajatului de modificat")
        print("Lasă câmpul gol dacă nu vrei să modifici un câmp.")

        campuri = {
            "nume": cere_input("Nume (opțional)", optional=True),
            "prenume": cere_input("Prenume (opțional)", optional=True),
            "ocupatie": cere_input("Ocupatie (opțional)", optional=True),
            "nrTelefon": cere_input("Telefon nou (opțional)", optional=True),
            "email": cere_input("Email (opțional)", optional=True),
            "adresa": cere_input("Adresă (opțional)", optional=True),
        }

        if self.manager.modifica_dupa_telefon(tel, **campuri):
            print("Angajat modificat.")
        else:
            print("Angajatul nu a fost găsit după telefon.")

    # ---------------------------------------------------
    # 5. Ștergere (după telefon)
    # ---------------------------------------------------
    def sterge(self):
        tel = cere_input("Telefonul angajatului de șters")
        conf = input("Sigur vrei să ștergi? (da/nu): ").strip().lower()
        if conf not in ("da", "d"):
            print("Anulat.")
            return

        if self.manager.sterge_dupa_telefon(tel):
            print("Angajat șters.")
        else:
            print("Angajatul nu a fost găsit după telefon.")

    def meniu(self):
        while True:
            print("\n=== MENIU ANGAJAȚI ===")
            print("1. Adaugă angajat")
            print("2. Afișează toți angajații")
            print("3. Caută angajat")
            print("4. Modifică angajat (după număr de telefon)")
            print("5. Șterge angajat (după număr de telefon)")
            print("6. Înapoi la meniu principal")

            opt = input("Alege o opțiune (1-6): ").strip()

            if opt == "1":
                self.adauga()
            elif opt == "2":
                self.afiseaza()
            elif opt == "3":
                self.cauta()
            elif opt == "4":
                self.modifica()
            elif opt == "5":
                self.sterge()
            elif opt == "6":
                print("Revenire la meniu principal...")
                break
            else:
                print("Opțiune invalidă!")


# ============================================================
# MENIU MASINI
# ============================================================


class MeniuMasini:
    """Meniu pentru gestionarea mașinilor (versiunea finală)."""

    def __init__(self):
        self.manager = ManagerMasini("masini.json")

    # ---------------------------------------------------
    # 1. Adaugă
    # ---------------------------------------------------
    def adauga(self):
        print("\n=== ADAUGĂ MAȘINĂ ===")
        try:
            masina = self.manager.adauga_masina(
                fabricatie=cere_input("Producător"),
                anul=cere_input("An fabricație"),
                model=cere_input("Model"),
                pret_cost=cere_input("Preț achiziție (€)"),
                potential_pret_vanzare=cere_input("Preț potențial vânzare (€)"),
                nr_inmatriculare=cere_input("Număr de înmatriculare"),
            )
            print(f" Mașină adăugată: {masina.ID} {masina.fabricatie} {masina.model}")
        except Exception as e:
            print("", e)

    # ---------------------------------------------------
    # 2. Afișare
    # ---------------------------------------------------
    def afiseaza(self):
        print("\n=== LISTA MAȘINILOR ===")
        masini = self.manager.toate()

        if not masini:
            print("Nu există mașini.")
            return

        for m in masini:
            print(
                f"{m['id']} | {m['fabricatie']} {m['model']} ({m['anul']}) | "
                f"Cost: {m['pret_cost']} € | "
                f"Vânzare: {m['potential_pret_vanzare']} € | "
                f"Nr. înmatriculare: {m['nr_inmatriculare']}"
            )

    # ---------------------------------------------------
    # 3. Căutare (NUMAI după nr. înmatriculare)
    # ---------------------------------------------------
    def cauta(self):
        nr = cere_input("Numărul de înmatriculare")
        rezultate = self.manager.cauta(nr)

        if not rezultate:
            print("Nicio mașină găsită.")
            return

        print("\n=== Rezultate căutare ===")
        for m in rezultate:
            print(
                f"{m['id']} | {m['fabricatie']} {m['model']} | Nr: {m['nr_inmatriculare']}"
            )

    # ---------------------------------------------------
    # 4. Modificare (NUMAI după nr. înmatriculare)
    # ---------------------------------------------------
    def modifica(self):
        nr = cere_input("Numărul de înmatriculare al mașinii de modificat")
        print("Lasă câmpul gol dacă nu vrei să modifici un câmp.")
        campuri = {
            "fabricatie": cere_input("Producător (opțional)", optional=True),
            "anul": cere_input("An fabricație (opțional)", optional=True),
            "model": cere_input("Model (opțional)", optional=True),
            "pret_cost": cere_input("Preț achiziție (opțional)", optional=True),
            "potential_pret_vanzare": cere_input(
                "Preț vânzare (opțional)", optional=True
            ),
            "nr_inmatriculare_nou": cere_input(
                "Nr. înmatriculare NOU (opțional)", optional=True
            ),
        }

        if self.manager.modifica(nr, **campuri):
            print("Mașină modificată.")
        else:
            print("Mașina nu a fost găsită după numărul de înmatriculare.")

    # ---------------------------------------------------
    # 5. Ștergere (NUMAI după nr. înmatriculare)
    # ---------------------------------------------------
    def sterge(self):
        nr = cere_input("Numărul de înmatriculare al mașinii de șters")
        confirm = input("Sigur vrei să ștergi? (da/nu): ").strip().lower()

        if confirm not in ("da", "d"):
            print("Anulat.")
            return

        if self.manager.sterge(nr):
            print("Mașină ștearsă.")
        else:
            print("Mașina nu a fost găsită după numărul de înmatriculare.")

    def meniu(self):
        while True:
            print("\n=== MENIU MAȘINI ===")
            print("1. Adaugă mașină")
            print("2. Afișează toate mașinile")
            print("3. Caută mașină (după nr. înmatriculare)")
            print("4. Modifică mașină (după nr. înmatriculare)")
            print("5. Șterge mașină (după nr. înmatriculare)")
            print("6. Înapoi la meniul principal")

            opt = input("Alege o opțiune (1-6): ").strip()

            if opt == "1":
                self.adauga()
            elif opt == "2":
                self.afiseaza()
            elif opt == "3":
                self.cauta()
            elif opt == "4":
                self.modifica()
            elif opt == "5":
                self.sterge()
            elif opt == "6":
                print("Revenire la meniul principal...")
                break
            else:
                print("Opțiune invalidă!")


# ============================================================
# MENIU VANZARI
# ============================================================


class MeniuVanzari:
    """Meniu pentru gestionarea vânzărilor (versiunea finală)."""

    def __init__(self):
        self.manager = ManagerVanzari("vanzari.json")

    # ---------------------------------------------------
    # 1. Adăugare vânzare
    # ---------------------------------------------------
    def adauga(self):
        print("\n=== ÎNREGISTREAZĂ VÂNZARE ===")
        try:
            vanzare = self.manager.adauga_vanzare(
                data=cere_input(
                    "Data vânzării (YYYY-MM-DD / DD.MM.YYYY / DD/MM/YYYY)",
                    optional=True,
                ),
                angajat_id=cere_input("ID angajat"),
                angajat_nume=cere_input("Nume angajat"),
                masina_id=cere_input("ID mașină"),
                masina_model=cere_input("Model mașină"),
                profit=cere_input("Profit (€)"),
            )
            print(
                f"Vânzare înregistrată: {vanzare.masina_model} | Profit: {vanzare.profit} €"
            )
        except Exception as e:
            print(" Eroare:", e)

    # ---------------------------------------------------
    # 2. Afișare vânzări
    # ---------------------------------------------------
    def afiseaza(self):
        print("\n=== TOATE VÂNZĂRILE ===")
        lst = self.manager.toate()

        if not lst:
            print("Nu există vânzări înregistrate.")
            return

        for v in lst:
            print(
                f"{v['data']} | {v['angajat_nume']} ({v['angajat_id']}) | "
                f"{v['masina_model']} [{v['masina_id']}] | Profit: {v['profit']} €"
            )

    # ---------------------------------------------------
    # 3. Căutare
    # ---------------------------------------------------
    def cauta(self):
        termen = cere_input("Termen de căutare")
        rezultate = self.manager.cauta(termen)

        if not rezultate:
            print("Nicio vânzare găsită.")
            return

        print("\n=== Rezultate căutare ===")
        for v in rezultate:
            print(
                f"{v['data']} | {v['angajat_nume']} | "
                f"{v['masina_model']} | Profit: {v['profit']} €"
            )

    # ---------------------------------------------------
    # 4. Analitice
    # ---------------------------------------------------
    def analitice(self):
        print("\n=== ANALITICE VANZARI ===")

        start = cere_input("Perioada începe la (data)", optional=True)
        end = cere_input("Perioada se termină la (data)", optional=True)

        if not start:
            start = "1900-01-01"
        if not end:
            end = "9999-12-31"

        print("\n--- REZULTATE ---")

        try:
            print(self.manager.cea_mai_vanduta_masina(start, end))
            print(self.manager.cel_mai_bun_vanzator(start, end))
            print(f"Profit total: {self.manager.profit_total(start, end):.2f} €")
        except Exception as e:
            print("Eroare:", e)

    def meniu(self):
        while True:
            print("\n=== MENIU VANZARI ===")
            print("1. Înregistrează vânzare")
            print("2. Afișează toate vânzările")
            print("3. Caută vânzare")
            print("4. Analitice vânzări")
            print("5. Înapoi la meniul principal")

            opt = input("Alege o opțiune (1-5): ").strip()

            if opt == "1":
                self.adauga()
            elif opt == "2":
                self.afiseaza()
            elif opt == "3":
                self.cauta()
            elif opt == "4":
                self.analitice()
            elif opt == "5":
                print("Revenire la meniul principal...")
                break
            else:
                print("Opțiune invalidă!")
