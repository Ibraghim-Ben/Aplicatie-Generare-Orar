from modele.orar import Orar, InregistrareOrar
from servicii.validator_constrangeri import ValidatorConstrangeri
from algoritmi.lectie_de_plasat import LectieDePlasat
from utilitare.constante import ZILE_LUCRATOARE
import time


class SlotDisponibil:
    def __init__(self, zi, numar_interval, sala):
        self.zi = zi
        self.numar_interval = numar_interval
        self.sala = sala
    
    def __str__(self):
        return f"{self.zi} - Interval {self.numar_interval} - {self.sala.nume}"


class PlanificatorHungarian:
    
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
    
    def genereaza_sloturi(self, sali):
        sloturi = []
        
        for zi in ZILE_LUCRATOARE:
            for numar_interval in range(1, 8):
                for sala in sali:
                    slot = SlotDisponibil(zi, numar_interval, sala)
                    sloturi.append(slot)
        
        return sloturi
    
    def genereaza_orar(self, profesori, materii, grupe, sali):
        if not materii or len(materii) == 0:
            return None
        
        if not sali or len(sali) == 0:
            return None
        
        timp_start = time.time()
        
        lectii = self.pregateste_lectii(materii)
        
        if len(lectii) == 0:
            return None
        
        sloturi = self.genereaza_sloturi(sali)
        
        orar_temporar = Orar()
        
        n = len(lectii)
        m = len(sloturi)
        dimensiune = max(n, m)
        
        matrice_cost = self.construieste_matrice_cost_patrata(lectii, sloturi, dimensiune, orar_temporar)
        
        alocari = self.algoritm_hungarian(matrice_cost, n, m)
        
        orar = self.aplica_alocari(lectii, sloturi, alocari)
        
        timp_final = time.time()
        orar.timp_generare = timp_final - timp_start
        orar.algoritm_folosit = "Hungarian"
        orar.conflicte = self.validator.numara_conflicte(orar)
        orar.scor_calitate = self.calculeaza_calitate(orar)
        
        return orar
    
    def construieste_matrice_cost_patrata(self, lectii, sloturi, dimensiune, orar_temporar):
        matrice = []
        
        for i in range(dimensiune):
            rand = []
            for j in range(dimensiune):
                if i < len(lectii) and j < len(sloturi):
                    cost = self.calculeaza_cost_alocare(lectii[i], sloturi[j], orar_temporar)
                else:
                    cost = 0
                rand.append(cost)
            matrice.append(rand)
        
        return matrice
    
    def calculeaza_cost_alocare(self, lectie, slot, orar_temporar):
        cost = 0
        
        if not self.validator.verifica_profesor_disponibil(lectie.profesor, slot.zi):
            return 10000
        
        valid, _ = self.validator.verifica_plasare_valida(
            orar_temporar, lectie.profesor, lectie.grupa, slot.sala, slot.zi, slot.numar_interval
        )
        
        if not valid:
            return 10000
        
        if slot.numar_interval >= 6:
            cost += 10
        elif slot.numar_interval <= 2:
            cost -= 5
        
        return cost
    
    def algoritm_hungarian(self, matrice_cost, n_lectii, m_sloturi):
        dimensiune = len(matrice_cost)
        matrice = [rand[:] for rand in matrice_cost]
        
        for i in range(dimensiune):
            min_val = min(matrice[i])
            for j in range(dimensiune):
                matrice[i][j] -= min_val
        
        for j in range(dimensiune):
            min_val = min(matrice[i][j] for i in range(dimensiune))
            for i in range(dimensiune):
                matrice[i][j] -= min_val
        
        max_iteratii = dimensiune * 2
        for iteratie in range(max_iteratii):
            linii_marcate = [False] * dimensiune
            coloane_marcate = [False] * dimensiune
            
            asignari_rand = [-1] * dimensiune
            asignari_coloana = [-1] * dimensiune
            
            for i in range(dimensiune):
                for j in range(dimensiune):
                    if matrice[i][j] == 0 and asignari_rand[i] == -1 and asignari_coloana[j] == -1:
                        asignari_rand[i] = j
                        asignari_coloana[j] = i
            
            numar_asignari = sum(1 for x in asignari_rand if x != -1)
            
            if numar_asignari >= dimensiune:
                break
            
            for i in range(dimensiune):
                if asignari_rand[i] == -1:
                    linii_marcate[i] = True
            
            schimbat = True
            while schimbat:
                schimbat = False
                for i in range(dimensiune):
                    if linii_marcate[i]:
                        for j in range(dimensiune):
                            if matrice[i][j] == 0 and not coloane_marcate[j]:
                                coloane_marcate[j] = True
                                schimbat = True
                
                for j in range(dimensiune):
                    if coloane_marcate[j]:
                        for i in range(dimensiune):
                            if asignari_rand[i] == j and not linii_marcate[i]:
                                linii_marcate[i] = True
                                schimbat = True
            
            min_nemarcate = float('inf')
            for i in range(dimensiune):
                if not linii_marcate[i]:
                    for j in range(dimensiune):
                        if not coloane_marcate[j]:
                            if matrice[i][j] < min_nemarcate:
                                min_nemarcate = matrice[i][j]
            
            if min_nemarcate == float('inf'):
                break
            
            for i in range(dimensiune):
                for j in range(dimensiune):
                    if not linii_marcate[i] and not coloane_marcate[j]:
                        matrice[i][j] -= min_nemarcate
                    elif linii_marcate[i] and coloane_marcate[j]:
                        matrice[i][j] += min_nemarcate
        
        alocari = [-1] * n_lectii
        for i in range(n_lectii):
            if asignari_rand[i] != -1 and asignari_rand[i] < m_sloturi:
                if matrice_cost[i][asignari_rand[i]] < 5000:
                    alocari[i] = asignari_rand[i]
        
        return alocari
    
    def aplica_alocari(self, lectii, sloturi, alocari):
        orar = Orar()
        
        for i, index_slot in enumerate(alocari):
            if index_slot != -1 and index_slot < len(sloturi):
                lectie = lectii[i]
                slot = sloturi[index_slot]
                
                inregistrare = InregistrareOrar(
                    lectie.materie,
                    lectie.profesor,
                    lectie.grupa,
                    slot.sala,
                    slot.numar_interval,
                    slot.zi
                )
                inregistrare.tip_lectie = lectie.tip_lectie
                
                orar.adauga_inregistrare(inregistrare)
        
        return orar
    
    def calculeaza_calitate(self, orar):
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
    
    def numara_ferestre_grupe(self, orar):
        ferestre = 0
        grupe_unice = set()
        
        for inreg in orar.inregistrari:
            grupe_unice.add(inreg.grupa.id)
        
        for id_grupa in grupe_unice:
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