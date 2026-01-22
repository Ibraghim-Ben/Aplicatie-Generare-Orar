class Sala:
    def __init__(self, id_sala, nume):
        self.id = id_sala
        self.nume = nume
    
    def __str__(self):
        return self.nume
    
    def __repr__(self):
        return self.nume
    
    def __eq__(self, other):
        if not isinstance(other, Sala):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)