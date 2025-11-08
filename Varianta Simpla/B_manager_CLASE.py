import json
from typing import List, Dict, Callable
from datetime import datetime
from A_angajati_masini_vanzari import ListaAngajati, Masina, Vanzare


# ============================================================
# SALVARE DATE
# ============================================================


class SalvareJson:
    def __init__(self, fisier: str):
        self.fisier = fisier
        self.data: List[Dict] = []
        self.incarca()

    def incarca(self):
        try:
            with open(self.fisier, "r", encoding="utf-8") as f:
                content = f.read().strip()
                self.data = json.loads(content) if content else []
        except FileNotFoundError:
            self.data = []
            self.salveaza()

    def salveaza(self):
        with open(self.fisier, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def adauga(self, item: Dict):
        self.data.append(item)
        self.salveaza()

    def sterge(self, predicate: Callable[[Dict], bool]) -> bool:
        for i, d in enumerate(self.data):
            if predicate(d):
                del self.data[i]
                self.salveaza()
                return True
        return False

    def cauta(self, predicate: Callable[[Dict], bool]) -> List[Dict]:
        return [d for d in self.data if predicate(d)]

    def actualizeaza(
        self, predicate: Callable[[Dict], bool], update: Callable[[Dict], None]
    ) -> bool:
        for d in self.data:
            if predicate(d):
                update(d)
                self.salveaza()
                return True
        return False


# ============================================================
# MANAGER ANGAJAȚI
# ============================================================


class ManagerAngajati:
    def __init__(self, fisier="angajati.json"):
        self.repo = SalvareJson(fisier)
        self.counter = self._init_counter()

    def _init_counter(self) -> int:
        max_id = 0
        for e in self.repo.data:
            try:
                nr = int(e["id"].split("-")[1])
                max_id = max(max_id, nr)
            except:
                pass
        return max_id

    def _genereaza_id(self) -> str:
        self.counter += 1
        return f"ID-{self.counter:02d}"

    # -------------------------------------------------------
    # ADĂUGARE
    # -------------------------------------------------------
    def adauga_angajat(self, nume, prenume, ocupatie, telefon, email, adresa):
        for e in self.repo.data:
            if e["telefon"] == telefon:
                raise ValueError(f"Telefonul {telefon} există deja (ID: {e['id']}).")
            if e["email"].lower() == email.lower():
                raise ValueError(f"Emailul {email} există deja (ID: {e['id']}).")

        ang = ListaAngajati(
            ID=self._genereaza_id(),
            nume=nume,
            prenume=prenume,
            ocupatie=ocupatie,
            nrTelefon=telefon,
            email=email,
            adresa=adresa,
        )
        self.repo.adauga(ang.creare_dictionar())
        return ang

    # -------------------------------------------------------
    # AFIȘARE
    # -------------------------------------------------------
    def afiseaza_toti(self) -> List[Dict]:
        return self.repo.data

    # -------------------------------------------------------
    # CĂUTARE
    # -------------------------------------------------------
    def cauta(self, termen: str) -> List[Dict]:
        t = termen.lower()
        return self.repo.cauta(
            lambda e: t in e["id"].lower()
            or t in e["nume"].lower()
            or t in e["prenume"].lower()
            or t in e["telefon"].lower()
            or t in e["email"].lower()
        )

    # ȘTERGERE după telefon
    # -------------------------------------------------------
    def sterge_dupa_telefon(self, telefon: str) -> bool:
        return self.repo.sterge(lambda e: e["telefon"] == telefon)

    # -------------------------------------------------------
    # MODIFICARE după telefon
    # -------------------------------------------------------
    def modifica_dupa_telefon(self, telefon: str, **campuri) -> bool:

        def update(e: Dict):
            for k, v in campuri.items():
                if v not in ("", None, False):
                    e[k] = v

        return self.repo.actualizeaza(lambda e: e["telefon"] == telefon, update)


# ============================================================
# MANAGER MAȘINI
# ============================================================
class ManagerMasini:

    def __init__(self, fisier="masini.json"):
        self.repo = SalvareJson(fisier)
        self._counter = self._init_counter()

    def _init_counter(self) -> int:

        max_id = 0
        for m in self.repo.data:
            try:
                nr = int(m["id"].split("-")[1])
                max_id = max(max_id, nr)
            except:
                pass
        return max_id

    def _genereaza_id(self) -> str:
        self._counter += 1
        return f"CAR-{self._counter:03d}"

    # --------------------------------------------------------
    # 1. Adăugare mașină
    # --------------------------------------------------------
    def adauga_masina(
        self,
        fabricatie,
        anul,
        model,
        pret_cost,
        potential_pret_vanzare,
        nr_inmatriculare,
    ):
        anul = int(anul)
        pret_cost = float(pret_cost)
        potential_pret_vanzare = float(potential_pret_vanzare)
        nr_inmatriculare = nr_inmatriculare.upper()

        # verificare an
        an_curent = datetime.now().year
        if anul < 1900 or anul > an_curent + 1:
            raise ValueError("An fabricație invalid.")

        masina = Masina(
            ID=self._genereaza_id(),
            fabricatie=fabricatie,
            anul=anul,
            model=model,
            pret_cost=pret_cost,
            potential_pret_vanzare=potential_pret_vanzare,
            nr_inmatriculare=nr_inmatriculare,
        )

        self.repo.adauga(masina.creare_dictionar())
        return masina

    # --------------------------------------------------------
    # 2. Afișare mașini
    # --------------------------------------------------------
    def toate(self) -> List[Dict]:
        return self.repo.data

    # --------------------------------------------------------
    # 3. Căutare DOAR după nr. de înmatriculare
    # --------------------------------------------------------
    def cauta(self, nr_inmatriculare: str) -> List[Dict]:
        nr = nr_inmatriculare.upper()
        return self.repo.cauta(lambda m: m["nr_inmatriculare"].upper() == nr)

    # --------------------------------------------------------
    # 4. Modificare DOAR după nr. de înmatriculare
    # --------------------------------------------------------
    def modifica(self, nr_inmatriculare: str, **campuri) -> bool:
        nr = nr_inmatriculare.upper()

        def update(m: Dict):
            for k, v in campuri.items():
                if v in ("", None):
                    continue
                if k in ("pret_cost", "potential_pret_vanzare"):
                    v = float(v)
                if k == "anul":
                    v = int(v)
                if k == "nr_inmatriculare":
                    v = v.upper()
                m[k] = v

        return self.repo.actualizeaza(
            lambda m: m["nr_inmatriculare"].upper() == nr, update
        )

    # --------------------------------------------------------
    # 5. Ștergere DOAR după nr. de înmatriculare
    # --------------------------------------------------------
    def sterge(self, nr_inmatriculare: str) -> bool:
        nr = nr_inmatriculare.upper()
        return self.repo.sterge(lambda m: m["nr_inmatriculare"].upper() == nr)


# ============================================================
# MANAGER VANZARI
# ============================================================


class ManagerVanzari:

    def __init__(self, fisier="vanzari.json"):
        # ✅ JsonRepoVanzari nu exista → folosim SalvareJson
        self.repo = SalvareJson(fisier)

    # ----------------------------
    # 1. Adăugare vânzare
    # ----------------------------
    def adauga_vanzare(
        self,
        data: str,
        angajat_id: str,
        angajat_nume: str,
        masina_id: str,
        masina_model: str,
        profit: float,
    ) -> Vanzare:

        data = self._valideaza_data(data)
        profit = float(profit)

        vanzare = Vanzare(
            data=data,
            angajat_id=angajat_id,
            angajat_nume=angajat_nume,
            masina_id=masina_id,
            masina_model=masina_model,
            profit=profit,
        )

        self.repo.adauga(vanzare.creare_dictionar())
        return vanzare

    # ----------------------------
    # 2. Afișare toate
    # ----------------------------
    def toate(self) -> List[Dict]:
        return self.repo.data

    # ----------------------------
    # 3. Căutare (după angajat, model, ID mașină)
    # ----------------------------
    def cauta(self, termen: str) -> List[Dict]:
        t = termen.lower()
        return self.repo.cauta(
            lambda v: t in v["angajat_nume"].lower()
            or t in v["masina_model"].lower()
            or t in v["masina_id"].lower()
        )

    # ----------------------------
    # 4. Analitice
    # ----------------------------
    def _valideaza_data(self, s: str) -> str:
        """Acceptă formate multiple: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY."""
        s = s.strip()
        if not s:
            return datetime.now().strftime("%Y-%m-%d")

        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
            except ValueError:
                pass

        raise ValueError("Format dată invalid. Exemplu corect: 2025-11-08")

    def _in_interval(self, data: str, start: str, end: str) -> bool:
        d = datetime.strptime(data, "%Y-%m-%d")
        s = datetime.strptime(self._valideaza_data(start), "%Y-%m-%d")
        e = datetime.strptime(self._valideaza_data(end), "%Y-%m-%d")
        return s <= d <= e

    def filtrare_perioada(self, start: str, end: str) -> List[Dict]:
        return self.repo.cauta(lambda v: self._in_interval(v["data"], start, end))

    def cea_mai_vanduta_masina(self, start: str, end: str) -> str:
        vlist = self.filtrare_perioada(start, end)
        if not vlist:
            return "Nu există vânzări în perioada selectată."

        counter = {}
        for v in vlist:
            counter[v["masina_model"]] = counter.get(v["masina_model"], 0) + 1

        model, cnt = max(counter.items(), key=lambda t: t[1])
        return f"Cea mai vândută mașină: {model} ({cnt} vânzări)"

    def cel_mai_bun_vanzator(self, start: str, end: str) -> str:
        vlist = self.filtrare_perioada(start, end)
        if not vlist:
            return "Nu există vânzări în perioada selectată."

        profituri = {}
        nume = {}

        for v in vlist:
            profituri[v["angajat_id"]] = profituri.get(v["angajat_id"], 0) + v["profit"]
            nume[v["angajat_id"]] = v["angajat_nume"]

        winner = max(profituri, key=profituri.get)
        return (
            f"Cel mai bun vânzător: {nume[winner]} "
            f"({winner}) | Profit total: {profituri[winner]:.2f} €"
        )

    def profit_total(self, start: str, end: str) -> float:
        return sum(v["profit"] for v in self.filtrare_perioada(start, end))
