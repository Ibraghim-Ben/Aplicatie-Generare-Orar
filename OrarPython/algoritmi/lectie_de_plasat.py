class LectieDePlasat:
    def __init__(self, materie, profesor, grupa):
        self.materie = materie
        self.profesor = profesor
        self.grupa = grupa
        self.tip_lectie = 'Curs'
    
    def __str__(self):
        return f"{self.materie.nume} - {self.grupa.nume} - {self.profesor.nume} ({self.tip_lectie})"
    
    def __repr__(self):
        return self.__str__()