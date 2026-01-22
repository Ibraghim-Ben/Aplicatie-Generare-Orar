class Profesor:
    def __init__(self, id_profesor, nume, zile_disponibile):
        self.id = id_profesor
        self.nume = nume
        self.zile_disponibile = zile_disponibile if zile_disponibile else []
        self.ore_alocate = 0
    
    def este_disponibil(self, zi):
        return zi in self.zile_disponibile
    
    def adauga_ora(self):
        self.ore_alocate += 1
    
    def reseteaza_ore(self):
        self.ore_alocate = 0
    
    def __str__(self):
        zile_text = ', '.join(self.zile_disponibile) if self.zile_disponibile else 'Nicio zi'
        return f"{self.nume} ({zile_text})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Profesor):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)