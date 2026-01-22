from modele.orar import Orar, InregistrareOrar
from servicii.validator_constrangeri import ValidatorConstrangeri
from algoritmi.lectie_de_plasat import LectieDePlasat
from utilitare.constante import ZILE_LUCRATOARE
import time


class PlanificatorBacktracking:
    
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
        orar = Orar()
        
        if not materii or len(materii) == 0:
            return None
        
        if not sali or len(sali) == 0:
            return None
        
        timp_start = time.time()
        
        lectii = self.pregateste_lectii(materii)
        
        if len(lectii) == 0:
            return None
        
        succes = self.backtrack(0, lectii, orar, sali)
        
        timp_final = time.time()
        orar.timp_generare = timp_final - timp_start
        orar.algoritm_folosit = "Backtracking"
        
        if succes:
            orar.conflicte = self.validator.numara_conflicte(orar)
            orar.scor_calitate = self.calculeaza_calitate(orar)
            return orar
        else:
            return None
    
    def backtrack(self, index, lectii, orar, sali):
        if index >= len(lectii):
            return True
        
        lectie = lectii[index]
        
        for zi in ZILE_LUCRATOARE:
            if not self.validator.verifica_profesor_disponibil(lectie.profesor, zi):
                continue
            
            for numar_interval in range(1, 8):
                for sala in sali:
                    valid, _ = self.validator.verifica_plasare_valida(
                        orar, lectie.profesor, lectie.grupa, sala, zi, numar_interval
                    )
                    
                    if valid:
                        inregistrare = InregistrareOrar(
                            lectie.materie,
                            lectie.profesor,
                            lectie.grupa,
                            sala,
                            numar_interval,
                            zi
                        )
                        inregistrare.tip_lectie = lectie.tip_lectie
                        
                        orar.adauga_inregistrare(inregistrare)
                        
                        if self.backtrack(index + 1, lectii, orar, sali):
                            return True
                        
                        orar.inregistrari.pop()
        
        return False
    
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
        from modele.grupa import Grupa
        
        ferestre = 0
        grupe_unice = set()
        
        for inreg in orar.inregistrari:
            grupe_unice.add(inreg.grupa.id)
        
        for id_grupa in grupe_unice:
            grupa_temp = None
            for inreg in orar.inregistrari:
                if inreg.grupa.id == id_grupa:
                    grupa_temp = inreg.grupa
                    break
            
            if grupa_temp:
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