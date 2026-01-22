from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QRadioButton, QGroupBox, QProgressBar,
                             QMessageBox, QButtonGroup, QTextEdit, QInputDialog, QDialog, QDialogButtonBox, QLineEdit, QFormLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from baza_date.manager_bd import ManagerBazaDate
from servicii.generator_orar import GeneratorOrar


class ThreadGenerare(QThread):
    semnal_finalizare = pyqtSignal(object, bool, str)
    
    def __init__(self, generator, profesori, materii, grupe, sali, algoritm):
        super().__init__()
        self.generator = generator
        self.profesori = profesori
        self.materii = materii
        self.grupe = grupe
        self.sali = sali
        self.algoritm = algoritm
    
    def run(self):
        try:
            orar = self.generator.genereaza_orar(
                self.profesori, self.materii, self.grupe, self.sali, self.algoritm
            )
            
            if orar and len(orar.inregistrari) > 0:
                self.semnal_finalizare.emit(orar, True, "")
            else:
                self.semnal_finalizare.emit(None, False, "Nu s-a putut genera orarul. Verificați datele introduse.")
        except Exception as e:
            self.semnal_finalizare.emit(None, False, f"Eroare: {str(e)}")


class DialogSalvareOrar(QDialog):
    def __init__(self, text_implicit, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Salvare Orar")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.camp_nume = QLineEdit()
        self.camp_nume.setText(text_implicit)
        form_layout.addRow("Introduceți numele orarului:", self.camp_nume)
        
        layout.addLayout(form_layout)
        
        layout_butoane = QHBoxLayout()
        buton_ok = QPushButton("OK")
        buton_ok.clicked.connect(self.accept)
        buton_anuleaza = QPushButton("Anulează")
        buton_anuleaza.clicked.connect(self.reject)
        
        layout_butoane.addStretch()
        layout_butoane.addWidget(buton_ok)
        layout_butoane.addWidget(buton_anuleaza)
        
        layout.addLayout(layout_butoane)
        
        self.setLayout(layout)
    
    def obtine_nume(self):
        return self.camp_nume.text()


class PanouGenerareOrar(QWidget):
    
    def __init__(self):
        super().__init__()
        self.manager_bd = ManagerBazaDate()
        self.generator = GeneratorOrar()
        self.orar_generat = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titlu = QLabel("Generare Automată Orar Universitar")
        titlu.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(titlu)
        
        grup_algoritmi = QGroupBox("Selectați Algoritmul de Generare:")
        layout_algoritmi = QVBoxLayout()
        
        self.grup_butoane_algoritmi = QButtonGroup()
        
        self.radio_backtracking = QRadioButton("Backtracking")
        
        self.radio_astar = QRadioButton("A*")
        self.radio_astar.setChecked(True)
        
        self.radio_hungarian = QRadioButton("Hungarian Algorithm")
        
        self.grup_butoane_algoritmi.addButton(self.radio_backtracking)
        self.grup_butoane_algoritmi.addButton(self.radio_astar)
        self.grup_butoane_algoritmi.addButton(self.radio_hungarian)
        
        layout_algoritmi.addWidget(self.radio_backtracking)
        layout_algoritmi.addWidget(self.radio_astar)
        layout_algoritmi.addWidget(self.radio_hungarian)
        
        grup_algoritmi.setLayout(layout_algoritmi)
        layout.addWidget(grup_algoritmi)
        
        layout.addSpacing(20)
        
        self.eticheta_status = QLabel("Status: Gata de generare")
        self.eticheta_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #27ae60;")
        layout.addWidget(self.eticheta_status)
        
        self.bara_progres = QProgressBar()
        self.bara_progres.setVisible(False)
        layout.addWidget(self.bara_progres)
        
        self.buton_genereaza = QPushButton("GENEREAZĂ ORAR")
        self.buton_genereaza.clicked.connect(self.genereaza_orar)
        self.buton_genereaza.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        layout.addWidget(self.buton_genereaza)
        
        self.grup_rezultate = QGroupBox("Rezultat Generare:")
        self.grup_rezultate.setVisible(False)
        layout_rezultate = QVBoxLayout()
        
        self.text_rezultate = QTextEdit()
        self.text_rezultate.setReadOnly(True)
        self.text_rezultate.setMaximumHeight(210)
        layout_rezultate.addWidget(self.text_rezultate)
        
        layout_butoane_salvare = QHBoxLayout()
        self.buton_salveaza = QPushButton("Salvează Orar")
        self.buton_salveaza.clicked.connect(self.salveaza_orar)
        self.buton_salveaza.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        
        layout_butoane_salvare.addWidget(self.buton_salveaza)
        layout_butoane_salvare.addStretch()
        
        layout_rezultate.addLayout(layout_butoane_salvare)
        self.grup_rezultate.setLayout(layout_rezultate)
        
        layout.addWidget(self.grup_rezultate)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def obtine_algoritm_selectat(self):
        if self.radio_backtracking.isChecked():
            return "Backtracking"
        elif self.radio_astar.isChecked():
            return "A*"
        elif self.radio_hungarian.isChecked():
            return "Hungarian"
        return "A*"
    
    def genereaza_orar(self):
        profesori = self.manager_bd.obtine_toti_profesorii()
        materii = self.manager_bd.obtine_toate_materiile()
        grupe = self.manager_bd.obtine_toate_grupele()
        sali = self.manager_bd.obtine_toate_salile()
        
        if len(profesori) == 0:
            return
        
        if len(materii) == 0:
            return
        
        if len(grupe) == 0:
            return
        
        if len(sali) == 0:
            return
        
        self.eticheta_status.setText("Status: Generare în curs...")
        self.eticheta_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #f39c12;")
        self.bara_progres.setVisible(True)
        self.bara_progres.setRange(0, 0)
        self.buton_genereaza.setEnabled(False)
        self.grup_rezultate.setVisible(False)
        
        algoritm = self.obtine_algoritm_selectat()
        
        self.thread_generare = ThreadGenerare(
            self.generator, profesori, materii, grupe, sali, algoritm
        )
        self.thread_generare.semnal_finalizare.connect(self.generare_finalizata)
        self.thread_generare.start()
    
    def generare_finalizata(self, orar, succes, mesaj):
        self.bara_progres.setVisible(False)
        self.buton_genereaza.setEnabled(True)
        
        if succes and orar:
            self.orar_generat = orar
            
            self.eticheta_status.setText("Status: ✓ Orar generat cu succes!")
            self.eticheta_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #27ae60;")
            
            text_rezultat = f"""✓ ORAR GENERAT CU SUCCES!

Algoritm folosit: {orar.algoritm_folosit}
Timp de generare: {orar.timp_generare:.3f} secunde
Total lecții programate: {len(orar.inregistrari)}
Conflicte detectate: {orar.conflicte}
Scor calitate: {orar.scor_calitate:.1f}%

Mergeți la tab-ul "Vizualizare Orar" pentru a vedea rezultatul!"""
            
            self.text_rezultate.setText(text_rezultat)
            self.grup_rezultate.setVisible(True)
        else:
            self.orar_generat = None
            self.eticheta_status.setText("Status: ✗ Eroare la generare")
            self.eticheta_status.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
    
    def salveaza_orar(self):
        if not self.orar_generat:
            return
        
        dialog = DialogSalvareOrar(f"Orar {self.orar_generat.algoritm_folosit}", self)
        
        if dialog.exec_() == QDialog.Accepted:
            nume_orar = dialog.obtine_nume().strip()
            if nume_orar:
                id_orar = self.manager_bd.salveaza_orar_complet(self.orar_generat, nume_orar)
    
    def obtine_orar_generat(self):
        return self.orar_generat