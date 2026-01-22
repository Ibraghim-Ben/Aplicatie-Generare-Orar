from algoritmi.planificator_backtracking import PlanificatorBacktracking
from algoritmi.planificator_astar import PlanificatorAStar
from algoritmi.planificator_hungarian import PlanificatorHungarian


class GeneratorOrar:
    
    def __init__(self):
        self.planificator_backtracking = PlanificatorBacktracking()
        self.planificator_astar = PlanificatorAStar()
        self.planificator_hungarian = PlanificatorHungarian()
    
    def genereaza_cu_backtracking(self, profesori, materii, grupe, sali):
        try:
            return self.planificator_backtracking.genereaza_orar(profesori, materii, grupe, sali)
        except Exception as e:
            print(f"Eroare generare Backtracking: {e}")
            return None
    
    def genereaza_cu_astar(self, profesori, materii, grupe, sali):
        try:
            return self.planificator_astar.genereaza_orar(profesori, materii, grupe, sali)
        except Exception as e:
            print(f"Eroare generare A*: {e}")
            return None
    
    def genereaza_cu_hungarian(self, profesori, materii, grupe, sali):
        try:
            return self.planificator_hungarian.genereaza_orar(profesori, materii, grupe, sali)
        except Exception as e:
            print(f"Eroare generare Hungarian: {e}")
            return None
    
    def genereaza_orar(self, profesori, materii, grupe, sali, tip_algoritm="A*"):
        if tip_algoritm == "Backtracking":
            return self.genereaza_cu_backtracking(profesori, materii, grupe, sali)
        elif tip_algoritm == "A*":
            return self.genereaza_cu_astar(profesori, materii, grupe, sali)
        elif tip_algoritm == "Hungarian":
            return self.genereaza_cu_hungarian(profesori, materii, grupe, sali)
        else:
            return self.genereaza_cu_astar(profesori, materii, grupe, sali)