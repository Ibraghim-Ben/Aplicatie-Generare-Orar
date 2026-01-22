import sqlite3
import json
import os
from modele.profesor import Profesor
from modele.materie import Materie
from modele.grupa import Grupa
from modele.sala import Sala
from modele.orar import Orar, InregistrareOrar


class ManagerBazaDate:
    def __init__(self, nume_fisier='orar_universitar.db'):
        directorul_curent = os.path.dirname(os.path.abspath(__file__))
        cale_completa = os.path.join(directorul_curent, nume_fisier)
        
        self.conexiune = sqlite3.connect(cale_completa, check_same_thread=False)
        self.creaza_tabele()
    
    def creaza_tabele(self):
        cursor = self.conexiune.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profesori (
                id INTEGER PRIMARY KEY,
                nume TEXT NOT NULL,
                zile_disponibile TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupe (
                id INTEGER PRIMARY KEY,
                nume TEXT NOT NULL UNIQUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sali (
                id INTEGER PRIMARY KEY,
                nume TEXT NOT NULL UNIQUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materii (
                id INTEGER PRIMARY KEY,
                nume TEXT NOT NULL,
                ore_pe_saptamana INTEGER NOT NULL,
                profesor_curs_id INTEGER,
                ore_curs INTEGER DEFAULT 0,
                profesor_seminar_id INTEGER,
                ore_seminar INTEGER DEFAULT 0,
                profesor_laborator_id INTEGER,
                ore_laborator INTEGER DEFAULT 0,
                FOREIGN KEY (profesor_curs_id) REFERENCES profesori(id) ON DELETE SET NULL,
                FOREIGN KEY (profesor_seminar_id) REFERENCES profesori(id) ON DELETE SET NULL,
                FOREIGN KEY (profesor_laborator_id) REFERENCES profesori(id) ON DELETE SET NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materie_grupe (
                materie_id INTEGER NOT NULL,
                grupa_id INTEGER NOT NULL,
                PRIMARY KEY (materie_id, grupa_id),
                FOREIGN KEY (materie_id) REFERENCES materii(id) ON DELETE CASCADE,
                FOREIGN KEY (grupa_id) REFERENCES grupe(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orare (
                id INTEGER PRIMARY KEY,
                nume TEXT NOT NULL,
                data_creare TEXT NOT NULL,
                algoritm_folosit TEXT,
                timp_generare REAL,
                scor_calitate REAL,
                conflicte INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inregistrari_orar (
                id INTEGER PRIMARY KEY,
                orar_id INTEGER NOT NULL,
                materie_id INTEGER NOT NULL,
                profesor_id INTEGER NOT NULL,
                grupa_id INTEGER NOT NULL,
                sala_id INTEGER NOT NULL,
                zi TEXT NOT NULL,
                numar_interval INTEGER NOT NULL,
                tip_lectie TEXT,
                FOREIGN KEY (orar_id) REFERENCES orare(id) ON DELETE CASCADE,
                FOREIGN KEY (materie_id) REFERENCES materii(id),
                FOREIGN KEY (profesor_id) REFERENCES profesori(id),
                FOREIGN KEY (grupa_id) REFERENCES grupe(id),
                FOREIGN KEY (sala_id) REFERENCES sali(id)
            )
        ''')
        
        self.conexiune.commit()
    
    def salveaza_profesor(self, profesor):
        cursor = self.conexiune.cursor()
        zile_json = json.dumps(profesor.zile_disponibile, ensure_ascii=False)
        
        try:
            cursor.execute('''
                INSERT INTO profesori (nume, zile_disponibile)
                VALUES (?, ?)
            ''', (profesor.nume, zile_json))
            
            self.conexiune.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Eroare salvare profesor: {e}")
            return None
    
    def obtine_toti_profesorii(self):
        cursor = self.conexiune.cursor()
        cursor.execute('SELECT id, nume, zile_disponibile FROM profesori ORDER BY nume')
        
        profesori = []
        for rand in cursor.fetchall():
            try:
                zile = json.loads(rand[2])
                prof = Profesor(rand[0], rand[1], zile)
                profesori.append(prof)
            except Exception as e:
                print(f"Eroare citire profesor: {e}")
        
        return profesori
    
    def sterge_profesor(self, id_profesor):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM profesori WHERE id = ?', (id_profesor,))
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare ștergere profesor: {e}")
            return False
    
    def actualizeaza_profesor(self, profesor):
        cursor = self.conexiune.cursor()
        zile_json = json.dumps(profesor.zile_disponibile, ensure_ascii=False)
        
        try:
            cursor.execute('''
                UPDATE profesori 
                SET nume = ?, zile_disponibile = ?
                WHERE id = ?
            ''', (profesor.nume, zile_json, profesor.id))
            
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare actualizare profesor: {e}")
            return False
    
    def salveaza_grupa(self, grupa):
        cursor = self.conexiune.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO grupe (nume)
                VALUES (?)
            ''', (grupa.nume,))
            
            self.conexiune.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print("Grupa cu acest nume există deja")
            return None
        except Exception as e:
            print(f"Eroare salvare grupă: {e}")
            return None
    
    def obtine_toate_grupele(self):
        cursor = self.conexiune.cursor()
        cursor.execute('SELECT id, nume FROM grupe ORDER BY nume')
        
        grupe = []
        for rand in cursor.fetchall():
            grupa = Grupa(rand[0], rand[1])
            grupe.append(grupa)
        
        return grupe
    
    def sterge_grupa(self, id_grupa):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM grupe WHERE id = ?', (id_grupa,))
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare ștergere grupă: {e}")
            return False
    
    def salveaza_sala(self, sala):
        cursor = self.conexiune.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO sali (nume)
                VALUES (?)
            ''', (sala.nume,))
            
            self.conexiune.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print("Sala cu acest nume există deja")
            return None
        except Exception as e:
            print(f"Eroare salvare sală: {e}")
            return None
    
    def obtine_toate_salile(self):
        cursor = self.conexiune.cursor()
        cursor.execute('SELECT id, nume FROM sali ORDER BY nume')
        
        sali = []
        for rand in cursor.fetchall():
            sala = Sala(rand[0], rand[1])
            sali.append(sala)
        
        return sali
    
    def sterge_sala(self, id_sala):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM sali WHERE id = ?', (id_sala,))
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare ștergere sală: {e}")
            return False
    
    def salveaza_materie(self, materie, lista_id_grupe):
        cursor = self.conexiune.cursor()
        
        try:
            ore_total = materie.ore_curs + materie.ore_seminar + materie.ore_laborator
            
            profesor_curs_id = materie.profesor_curs.id if materie.profesor_curs else None
            profesor_seminar_id = materie.profesor_seminar.id if materie.profesor_seminar else None
            profesor_laborator_id = materie.profesor_laborator.id if materie.profesor_laborator else None
            
            cursor.execute('''
                INSERT INTO materii (nume, ore_pe_saptamana, 
                                   profesor_curs_id, ore_curs,
                                   profesor_seminar_id, ore_seminar,
                                   profesor_laborator_id, ore_laborator)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (materie.nume, ore_total,
                  profesor_curs_id, materie.ore_curs,
                  profesor_seminar_id, materie.ore_seminar,
                  profesor_laborator_id, materie.ore_laborator))
            
            id_materie = cursor.lastrowid
            
            for id_grupa in lista_id_grupe:
                cursor.execute('''
                    INSERT INTO materie_grupe (materie_id, grupa_id)
                    VALUES (?, ?)
                ''', (id_materie, id_grupa))
            
            self.conexiune.commit()
            return id_materie
        except Exception as e:
            print(f"Eroare salvare materie: {e}")
            return None
    
    def obtine_toate_materiile(self):
        cursor = self.conexiune.cursor()
        
        cursor.execute('''
            SELECT m.id, m.nume, m.ore_pe_saptamana,
                   m.profesor_curs_id, m.ore_curs,
                   m.profesor_seminar_id, m.ore_seminar,
                   m.profesor_laborator_id, m.ore_laborator
            FROM materii m
            ORDER BY m.nume
        ''')
        
        materii = []
        for rand in cursor.fetchall():
            try:
                profesor_curs = None
                if rand[3]:
                    cursor.execute('SELECT id, nume, zile_disponibile FROM profesori WHERE id = ?', (rand[3],))
                    p = cursor.fetchone()
                    if p:
                        profesor_curs = Profesor(p[0], p[1], json.loads(p[2]))
                
                profesor_seminar = None
                if rand[5]:
                    cursor.execute('SELECT id, nume, zile_disponibile FROM profesori WHERE id = ?', (rand[5],))
                    p = cursor.fetchone()
                    if p:
                        profesor_seminar = Profesor(p[0], p[1], json.loads(p[2]))
                
                profesor_laborator = None
                if rand[7]:
                    cursor.execute('SELECT id, nume, zile_disponibile FROM profesori WHERE id = ?', (rand[7],))
                    p = cursor.fetchone()
                    if p:
                        profesor_laborator = Profesor(p[0], p[1], json.loads(p[2]))
                
                cursor.execute('''
                    SELECT g.id, g.nume
                    FROM grupe g
                    JOIN materie_grupe mg ON g.id = mg.grupa_id
                    WHERE mg.materie_id = ?
                    ORDER BY g.nume
                ''', (rand[0],))
                
                grupe = [Grupa(g[0], g[1]) for g in cursor.fetchall()]
                
                materie = Materie(
                    rand[0], rand[1], rand[2], grupe,
                    profesor_curs, rand[4],
                    profesor_seminar, rand[6],
                    profesor_laborator, rand[8]
                )
                materii.append(materie)
            except Exception as e:
                print(f"Eroare citire materie: {e}")
        
        return materii
    
    def sterge_materie(self, id_materie):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM materie_grupe WHERE materie_id = ?', (id_materie,))
            cursor.execute('DELETE FROM materii WHERE id = ?', (id_materie,))
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare ștergere materie: {e}")
            return False
    
    def salveaza_orar_complet(self, orar, nume_orar):
        from datetime import datetime
        
        cursor = self.conexiune.cursor()
        
        try:
            data_curenta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO orare (nume, data_creare, algoritm_folosit, timp_generare, scor_calitate, conflicte)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nume_orar, data_curenta, orar.algoritm_folosit, orar.timp_generare, 
                  orar.scor_calitate, orar.conflicte))
            
            id_orar = cursor.lastrowid
            
            for inreg in orar.inregistrari:
                tip_lectie = getattr(inreg, 'tip_lectie', 'Curs')
                
                cursor.execute('''
                    INSERT INTO inregistrari_orar 
                    (orar_id, materie_id, profesor_id, grupa_id, sala_id, zi, numar_interval, tip_lectie)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (id_orar, inreg.materie.id, inreg.profesor.id, inreg.grupa.id, 
                      inreg.sala.id, inreg.zi, inreg.numar_interval, tip_lectie))
            
            self.conexiune.commit()
            return id_orar
        except Exception as e:
            print(f"Eroare salvare orar: {e}")
            return None
    
    def obtine_lista_orare(self):
        cursor = self.conexiune.cursor()
        cursor.execute('SELECT id, nume, data_creare, algoritm_folosit FROM orare ORDER BY data_creare DESC')
        
        orare = []
        for rand in cursor.fetchall():
            orare.append({
                'id': rand[0],
                'nume': rand[1],
                'data': rand[2],
                'algoritm': rand[3] if rand[3] else 'Necunoscut'
            })
        
        return orare
    
    def incarca_orar(self, id_orar):
        cursor = self.conexiune.cursor()
        
        try:
            cursor.execute('''
                SELECT algoritm_folosit, timp_generare, scor_calitate, conflicte
                FROM orare WHERE id = ?
            ''', (id_orar,))
            
            rand_orar = cursor.fetchone()
            if not rand_orar:
                return None
            
            orar = Orar()
            orar.algoritm_folosit = rand_orar[0] if rand_orar[0] else ""
            orar.timp_generare = rand_orar[1] if rand_orar[1] else 0.0
            orar.scor_calitate = rand_orar[2] if rand_orar[2] else 0.0
            orar.conflicte = rand_orar[3] if rand_orar[3] else 0
            
            cursor.execute('''
                SELECT io.materie_id, io.profesor_id, io.grupa_id, io.sala_id, io.zi, io.numar_interval, io.tip_lectie,
                       m.nume, m.ore_pe_saptamana,
                       p.nume, p.zile_disponibile,
                       g.nume,
                       s.nume
                FROM inregistrari_orar io
                JOIN materii m ON io.materie_id = m.id
                JOIN profesori p ON io.profesor_id = p.id
                JOIN grupe g ON io.grupa_id = g.id
                JOIN sali s ON io.sala_id = s.id
                WHERE io.orar_id = ?
                ORDER BY io.zi, io.numar_interval
            ''', (id_orar,))
            
            for rand in cursor.fetchall():
                profesor = Profesor(rand[1], rand[9], json.loads(rand[10]))
                grupa = Grupa(rand[2], rand[11])
                sala = Sala(rand[3], rand[12])
                materie = Materie(rand[0], rand[7], rand[8], [grupa])
                
                inreg = InregistrareOrar(materie, profesor, grupa, sala, rand[5], rand[4])
                inreg.tip_lectie = rand[6] if rand[6] else 'Curs'
                orar.adauga_inregistrare(inreg)
            
            return orar
        except Exception as e:
            print(f"Eroare încărcare orar: {e}")
            return None
    
    def sterge_orar(self, id_orar):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM orare WHERE id = ?', (id_orar,))
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare ștergere orar: {e}")
            return False
    
    def goleste_toate_tabelele(self):
        cursor = self.conexiune.cursor()
        try:
            cursor.execute('DELETE FROM inregistrari_orar')
            cursor.execute('DELETE FROM orare')
            cursor.execute('DELETE FROM materie_grupe')
            cursor.execute('DELETE FROM materii')
            cursor.execute('DELETE FROM profesori')
            cursor.execute('DELETE FROM grupe')
            cursor.execute('DELETE FROM sali')
            self.conexiune.commit()
            return True
        except Exception as e:
            print(f"Eroare golire tabele: {e}")
            return False
    
    def inchide_conexiune(self):
        if self.conexiune:
            self.conexiune.close()