class Grupa:
    def __init__(self, id_grupa, nume):
        self.id = id_grupa
        self.nume = nume
    
    def __str__(self):
        return self.nume
    
    def __repr__(self):
        return self.nume
    
    def __eq__(self, other):
        if not isinstance(other, Grupa):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)