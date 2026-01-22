class Materie:
    def __init__(self, id_materie, nume, ore_pe_saptamana, grupe_alocate, 
                 profesor_curs=None, ore_curs=0,
                 profesor_seminar=None, ore_seminar=0,
                 profesor_laborator=None, ore_laborator=0):
        self.id = id_materie
        self.nume = nume
        self.ore_pe_saptamana = ore_pe_saptamana
        self.grupe_alocate = grupe_alocate if grupe_alocate else []
        
        self.profesor_curs = profesor_curs
        self.ore_curs = ore_curs
        
        self.profesor_seminar = profesor_seminar
        self.ore_seminar = ore_seminar
        
        self.profesor_laborator = profesor_laborator
        self.ore_laborator = ore_laborator
    
    def obtine_numar_total_lectii(self):
        total_ore = self.ore_curs + self.ore_seminar + self.ore_laborator
        return total_ore * len(self.grupe_alocate)
    
    def obtine_componente_active(self):
        componente = []
        if self.ore_curs > 0 and self.profesor_curs:
            componente.append(('Curs', self.profesor_curs, self.ore_curs))
        if self.ore_seminar > 0 and self.profesor_seminar:
            componente.append(('Seminar', self.profesor_seminar, self.ore_seminar))
        if self.ore_laborator > 0 and self.profesor_laborator:
            componente.append(('Laborator', self.profesor_laborator, self.ore_laborator))
        return componente
    
    def __str__(self):
        componente = []
        if self.ore_curs > 0:
            prof_curs = self.profesor_curs.nume if self.profesor_curs else "Fără profesor"
            componente.append(f"Curs: {prof_curs} ({self.ore_curs}h)")
        if self.ore_seminar > 0:
            prof_seminar = self.profesor_seminar.nume if self.profesor_seminar else "Fără profesor"
            componente.append(f"Seminar: {prof_seminar} ({self.ore_seminar}h)")
        if self.ore_laborator > 0:
            prof_lab = self.profesor_laborator.nume if self.profesor_laborator else "Fără profesor"
            componente.append(f"Laborator: {prof_lab} ({self.ore_laborator}h)")
        
        componente_text = ", ".join(componente) if componente else "Fără componente"
        grupe_text = ', '.join([g.nume for g in self.grupe_alocate]) if self.grupe_alocate else "Fără grupe"
        
        return f"{self.nume} | {componente_text} | Grupe: {grupe_text}"
    
    def __repr__(self):
        return self.__str__()