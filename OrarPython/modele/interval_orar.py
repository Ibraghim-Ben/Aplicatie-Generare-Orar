class IntervalOrar:
    def __init__(self, zi, ora_inceput, ora_sfarsit, numar_interval):
        self.zi = zi
        self.ora_inceput = ora_inceput
        self.ora_sfarsit = ora_sfarsit
        self.numar_interval = numar_interval
    
    def __str__(self):
        return f"{self.zi} {self.ora_inceput}-{self.ora_sfarsit}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, IntervalOrar):
            return False
        return (self.zi == other.zi and 
                self.numar_interval == other.numar_interval)
    
    def __hash__(self):
        return hash((self.zi, self.numar_interval))