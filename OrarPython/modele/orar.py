class InregistrareOrar:
    def __init__(self, materie, profesor, grupa, sala, numar_interval, zi):
        self.materie = materie
        self.profesor = profesor
        self.grupa = grupa
        self.sala = sala
        self.numar_interval = numar_interval
        self.zi = zi
    
    def obtine_interval_text(self):
        from utilitare.constante import INTERVALE_ORARE
        if self.numar_interval in INTERVALE_ORARE:
            interval = INTERVALE_ORARE[self.numar_interval]
            return f"{interval[0]}-{interval[1]}"
        return ""
    
    def __str__(self):
        return f"{self.materie.nume} | {self.grupa.nume} | {self.sala.nume} | {self.zi} {self.obtine_interval_text()}"
    
    def __repr__(self):
        return self.__str__()


class Orar:
    def __init__(self):
        self.inregistrari = []
        self.conflicte = 0
        self.scor_calitate = 0.0
        self.timp_generare = 0.0
        self.algoritm_folosit = ""
    
    def adauga_inregistrare(self, inregistrare):
        if inregistrare:
            self.inregistrari.append(inregistrare)
    
    def obtine_inregistrari_pentru_grupa(self, grupa):
        return [inreg for inreg in self.inregistrari if inreg.grupa.id == grupa.id]
    
    def obtine_inregistrari_pentru_profesor(self, profesor):
        return [inreg for inreg in self.inregistrari if inreg.profesor.id == profesor.id]
    
    def obtine_inregistrari_pentru_sala(self, sala):
        return [inreg for inreg in self.inregistrari if inreg.sala.id == sala.id]
    
    def obtine_inregistrare(self, zi, numar_interval, grupa=None, profesor=None, sala=None):
        for inreg in self.inregistrari:
            if inreg.zi == zi and inreg.numar_interval == numar_interval:
                if grupa and inreg.grupa.id == grupa.id:
                    return inreg
                if profesor and inreg.profesor.id == profesor.id:
                    return inreg
                if sala and inreg.sala.id == sala.id:
                    return inreg
        return None
    
    def verifica_conflict_profesor(self, profesor, zi, numar_interval):
        for inreg in self.inregistrari:
            if (inreg.profesor.id == profesor.id and 
                inreg.zi == zi and 
                inreg.numar_interval == numar_interval):
                return True
        return False
    
    def verifica_conflict_grupa(self, grupa, zi, numar_interval):
        for inreg in self.inregistrari:
            if (inreg.grupa.id == grupa.id and 
                inreg.zi == zi and 
                inreg.numar_interval == numar_interval):
                return True
        return False
    
    def verifica_conflict_sala(self, sala, zi, numar_interval):
        for inreg in self.inregistrari:
            if (inreg.sala.id == sala.id and 
                inreg.zi == zi and 
                inreg.numar_interval == numar_interval):
                return True
        return False
    
    def goleste(self):
        self.inregistrari = []
        self.conflicte = 0
        self.scor_calitate = 0.0
    
    def __len__(self):
        return len(self.inregistrari)
    
    def __str__(self):
        return f"Orar: {len(self.inregistrari)} lecții, {self.conflicte} conflicte, Calitate: {self.scor_calitate:.1f}%"