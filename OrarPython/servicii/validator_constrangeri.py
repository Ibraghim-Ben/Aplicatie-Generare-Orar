class ValidatorConstrangeri:
    
    @staticmethod
    def verifica_profesor_disponibil(profesor, zi):
        if not profesor or not zi:
            return False
        return zi in profesor.zile_disponibile
    
    @staticmethod
    def verifica_profesor_liber(orar, profesor, zi, numar_interval):
        if not profesor or not zi or not numar_interval:
            return False
        return not orar.verifica_conflict_profesor(profesor, zi, numar_interval)
    
    @staticmethod
    def verifica_grupa_libera(orar, grupa, zi, numar_interval):
        if not grupa or not zi or not numar_interval:
            return False
        return not orar.verifica_conflict_grupa(grupa, zi, numar_interval)
    
    @staticmethod
    def verifica_sala_libera(orar, sala, zi, numar_interval):
        if not sala or not zi or not numar_interval:
            return False
        return not orar.verifica_conflict_sala(sala, zi, numar_interval)
    
    @staticmethod
    def verifica_plasare_valida(orar, profesor, grupa, sala, zi, numar_interval):
        if not ValidatorConstrangeri.verifica_profesor_disponibil(profesor, zi):
            return False, "Profesorul nu este disponibil în această zi"
        
        if not ValidatorConstrangeri.verifica_profesor_liber(orar, profesor, zi, numar_interval):
            return False, f"Profesorul {profesor.nume} este ocupat la {zi} interval {numar_interval}"
        
        if not ValidatorConstrangeri.verifica_grupa_libera(orar, grupa, zi, numar_interval):
            return False, f"Grupa {grupa.nume} are deja o lecție la {zi} interval {numar_interval}"
        
        if not ValidatorConstrangeri.verifica_sala_libera(orar, sala, zi, numar_interval):
            return False, f"Sala {sala.nume} este ocupată la {zi} interval {numar_interval}"
        
        return True, "OK"
    
    @staticmethod
    def numara_conflicte(orar):
        conflicte = 0
        verificate = set()
        
        for i, inreg1 in enumerate(orar.inregistrari):
            for j, inreg2 in enumerate(orar.inregistrari):
                if i >= j:
                    continue
                
                pereche = (min(i, j), max(i, j))
                if pereche in verificate:
                    continue
                verificate.add(pereche)
                
                if inreg1.zi == inreg2.zi and inreg1.numar_interval == inreg2.numar_interval:
                    if inreg1.profesor.id == inreg2.profesor.id:
                        conflicte += 1
                    if inreg1.grupa.id == inreg2.grupa.id:
                        conflicte += 1
                    if inreg1.sala.id == inreg2.sala.id:
                        conflicte += 1
        
        return conflicte
    
    @staticmethod
    def obtine_lista_conflicte(orar):
        conflicte = []
        verificate = set()
        
        for i, inreg1 in enumerate(orar.inregistrari):
            for j, inreg2 in enumerate(orar.inregistrari):
                if i >= j:
                    continue
                
                pereche = (min(i, j), max(i, j))
                if pereche in verificate:
                    continue
                verificate.add(pereche)
                
                if inreg1.zi == inreg2.zi and inreg1.numar_interval == inreg2.numar_interval:
                    if inreg1.profesor.id == inreg2.profesor.id:
                        conflicte.append(f"Profesor {inreg1.profesor.nume} - {inreg1.zi} interval {inreg1.numar_interval}")
                    if inreg1.grupa.id == inreg2.grupa.id:
                        conflicte.append(f"Grupa {inreg1.grupa.nume} - {inreg1.zi} interval {inreg1.numar_interval}")
                    if inreg1.sala.id == inreg2.sala.id:
                        conflicte.append(f"Sala {inreg1.sala.nume} - {inreg1.zi} interval {inreg1.numar_interval}")
        
        return conflicte