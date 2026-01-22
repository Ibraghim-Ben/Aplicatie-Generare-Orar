from modele.orar import Orar, InregistrareOrar
from servicii.validator_constrangeri import ValidatorConstrangeri
from algoritmi.lectie_de_plasat import LectieDePlasat
from utilitare.constante import ZILE_LUCRATOARE
import heapq
import time


class StareOrar:
    def __init__(self, orar, index_lectie, lectii_ramase, cost_g):
        self.orar = orar
        self.index_lectie = index_lectie
        self.lectii_ramase = lectii_ramase
        self.cost_g = cost_g
    
    def __lt__(self, other):
        return self.cost_g < other.cost_g


class PlanificatorAStar:
    
    def __init__(self):
        self.validator = ValidatorConstrangeri()
    
    def pregateste_lectii(self, materii):
        lectii = []
        
        for materie in materii:
            for grupa in materie.grupe_alocate:
                if materie.ore_curs > 0 and materie.profesor_curs:
                    for _ in range(materie.ore_curs):
                        lectie = LectieDePlasat(materie, materie.profesor_curs, grupa)
                        lectie.tip_lectie = 'Curs'
                        lectii.append(lectie)
                
                if materie.ore_seminar > 0 and materie.profesor_seminar:
                    for _ in range(materie.ore_seminar):
                        lectie = LectieDePlasat(materie, materie.profesor_seminar, grupa)
                        lectie.tip_lectie = 'Seminar'
                        lectii.append(lectie)
                
                if materie.ore_laborator > 0 and materie.profesor_laborator:
                    for _ in range(materie.ore_laborator):
                        lectie = LectieDePlasat(materie, materie.profesor_laborator, grupa)
                        lectie.tip_lectie = 'Laborator'
                        lectii.append(lectie)
        
        return lectii
    
    def genereaza_orar(self, profesori, materii, grupe, sali):
        if not materii or len(materii) == 0:
            return None
        
        if not sali or len(sali) == 0:
            return None
        
        timp_start = time.time()
        
        lectii = self.pregateste_lectii(materii)
        
        if len(lectii) == 0:
            return None
        
        orar_initial = Orar()
        stare_initiala = StareOrar(orar_initial, 0, lectii, 0)
        
        coada_prioritati = []
        heapq.heappush(coada_prioritati, (self.calculeaza_prioritate(stare_initiala), 0, stare_initiala))
        
        numar_iteratii = 0
        max_iteratii = 10000
        
        while coada_prioritati and numar_iteratii < max_iteratii:
            numar_iteratii += 1
            
            _, _, stare_curenta = heapq.heappop(coada_prioritati)
            
            if stare_curenta.index_lectie >= len(lectii):
                timp_final = time.time()
                stare_curenta.orar.timp_generare = timp_final - timp_start
                stare_curenta.orar.algoritm_folosit = "A*"
                stare_curenta.orar.conflicte = self.validator.numara_conflicte(stare_curenta.orar)
                stare_curenta.orar.scor_calitate = self.calculeaza_calitate_finala(stare_curenta.orar)
                return stare_curenta.orar
            
            stari_noi = self.extinde_stare(stare_curenta, lectii, sali)
            
            for stare_noua in stari_noi:
                prioritate = self.calculeaza_prioritate(stare_noua)
                heapq.heappush(coada_prioritati, (prioritate, numar_iteratii, stare_noua))
        
        return None
    
    def extinde_stare(self, stare, lectii, sali):
        stari_noi = []
        
        if stare.index_lectie >= len(lectii):
            return stari_noi
        
        lectie = lectii[stare.index_lectie]
        
        for zi in ZILE_LUCRATOARE:
            if not self.validator.verifica_profesor_disponibil(lectie.profesor, zi):
                continue
            
            for numar_interval in range(1, 8):
                for sala in sali:
                    valid, _ = self.validator.verifica_plasare_valida(
                        stare.orar, lectie.profesor, lectie.grupa, sala, zi, numar_interval
                    )
                    
                    if valid:
                        orar_nou = Orar()
                        orar_nou.inregistrari = stare.orar.inregistrari.copy()
                        
                        inregistrare = InregistrareOrar(
                            lectie.materie,
                            lectie.profesor,
                            lectie.grupa,
                            sala,
                            numar_interval,
                            zi
                        )
                        inregistrare.tip_lectie = lectie.tip_lectie
                        
                        orar_nou.adauga_inregistrare(inregistrare)
                        
                        cost_plasare = self.calculeaza_cost_plasare(orar_nou, inregistrare)
                        cost_g_nou = stare.cost_g + cost_plasare
                        
                        stare_noua = StareOrar(orar_nou, stare.index_lectie + 1, lectii, cost_g_nou)
                        stari_noi.append(stare_noua)
        
        return stari_noi
    
    def calculeaza_cost_plasare(self, orar, inregistrare):
        cost = 0
        
        if inregistrare.numar_interval >= 6:
            cost += 5
        
        ferestre = self.numara_ferestre_pentru_grupa(orar, inregistrare.grupa.id)
        cost += ferestre * 10
        
        return cost
    
    def calculeaza_prioritate(self, stare):
        g = stare.cost_g
        h = self.euristica(stare.orar, len(stare.lectii_ramase) - stare.index_lectie)
        return g + h
    
    def euristica(self, orar, lectii_ramase):
        if lectii_ramase == 0:
            return 0
        
        scor = lectii_ramase * 10
        
        ferestre = self.numara_ferestre_grupe(orar)
        scor += ferestre * 5
        
        distributie = self.verifica_distributie_uniforma(orar)
        scor -= distributie * 2
        
        return scor
    
    def numara_ferestre_pentru_grupa(self, orar, id_grupa):
        ferestre = 0
        
        for zi in ZILE_LUCRATOARE:
            intervale_ocupate = []
            for inreg in orar.inregistrari:
                if inreg.grupa.id == id_grupa and inreg.zi == zi:
                    intervale_ocupate.append(inreg.numar_interval)
            
            if len(intervale_ocupate) > 1:
                intervale_ocupate.sort()
                for i in range(len(intervale_ocupate) - 1):
                    diferenta = intervale_ocupate[i + 1] - intervale_ocupate[i]
                    if diferenta > 1:
                        ferestre += (diferenta - 1)
        
        return ferestre
    
    def numara_ferestre_grupe(self, orar):
        ferestre = 0
        grupe_unice = set()
        
        for inreg in orar.inregistrari:
            grupe_unice.add(inreg.grupa.id)
        
        for id_grupa in grupe_unice:
            ferestre += self.numara_ferestre_pentru_grupa(orar, id_grupa)
        
        return ferestre
    
    def verifica_distributie_uniforma(self, orar):
        if len(orar.inregistrari) == 0:
            return 0.0
        
        distributie_zile = {}
        for zi in ZILE_LUCRATOARE:
            distributie_zile[zi] = 0
        
        for inreg in orar.inregistrari:
            distributie_zile[inreg.zi] += 1
        
        valori = list(distributie_zile.values())
        if len(valori) == 0:
            return 0.0
        
        medie = sum(valori) / len(valori)
        
        if medie == 0:
            return 0.0
        
        deviatii = sum(abs(v - medie) for v in valori)
        uniformitate = max(0.0, 1.0 - (deviatii / (medie * len(valori))))
        
        return uniformitate * 10
    
    def calculeaza_calitate_finala(self, orar):
        if len(orar.inregistrari) == 0:
            return 0.0
        
        scor = 100.0
        
        ferestre_total = self.numara_ferestre_grupe(orar)
        scor -= ferestre_total * 2
        
        distributie = self.verifica_distributie_uniforma(orar)
        scor += distributie * 5
        
        if orar.conflicte > 0:
            scor -= orar.conflicte * 20
        
        return max(0.0, min(100.0, scor))