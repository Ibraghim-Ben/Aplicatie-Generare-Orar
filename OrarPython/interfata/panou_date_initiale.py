from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QLabel, QLineEdit, QPushButton, QListWidget, 
                             QCheckBox, QGroupBox, QFormLayout, QComboBox,
                             QSpinBox, QMessageBox, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt
from baza_date.manager_bd import ManagerBazaDate
from modele.profesor import Profesor
from modele.grupa import Grupa
from modele.sala import Sala
from modele.materie import Materie


class PanouDateInitiale(QWidget):
    
    def __init__(self):
        super().__init__()
        self.manager_bd = ManagerBazaDate()
        self.initUI()
    
    def initUI(self):
        layout_principal = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        
        self.tab_profesori = self.creaza_tab_profesori()
        self.tab_grupe = self.creaza_tab_grupe()
        self.tab_sali = self.creaza_tab_sali()
        self.tab_materii = self.creaza_tab_materii()
        
        self.tab_widget.addTab(self.tab_profesori, "Profesori")
        self.tab_widget.addTab(self.tab_grupe, "Grupe")
        self.tab_widget.addTab(self.tab_sali, "Săli")
        self.tab_widget.addTab(self.tab_materii, "Materii")
        
        layout_principal.addWidget(self.tab_widget)
        self.setLayout(layout_principal)
    
    def creaza_tab_profesori(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.camp_nume_profesor = QLineEdit()
        self.camp_nume_profesor.setPlaceholderText("Ex: Popescu Ion")
        form_layout.addRow("Nume profesor:", self.camp_nume_profesor)
        
        grup_zile = QGroupBox("Zile disponibile:")
        layout_zile = QVBoxLayout()
        
        self.checkbox_luni = QCheckBox("Luni")
        self.checkbox_marti = QCheckBox("Marți")
        self.checkbox_miercuri = QCheckBox("Miercuri")
        self.checkbox_joi = QCheckBox("Joi")
        self.checkbox_vineri = QCheckBox("Vineri")
        
        layout_zile.addWidget(self.checkbox_luni)
        layout_zile.addWidget(self.checkbox_marti)
        layout_zile.addWidget(self.checkbox_miercuri)
        layout_zile.addWidget(self.checkbox_joi)
        layout_zile.addWidget(self.checkbox_vineri)
        
        grup_zile.setLayout(layout_zile)
        
        buton_adauga_profesor = QPushButton("Adaugă Profesor")
        buton_adauga_profesor.clicked.connect(self.adauga_profesor)
        buton_adauga_profesor.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        
        layout.addLayout(form_layout)
        layout.addWidget(grup_zile)
        layout.addWidget(buton_adauga_profesor)
        
        layout.addWidget(QLabel("Listă profesori:"))
        self.lista_profesori = QListWidget()
        layout.addWidget(self.lista_profesori)
        
        layout_butoane = QHBoxLayout()
        buton_sterge_profesor = QPushButton("Șterge Profesor")
        buton_sterge_profesor.clicked.connect(self.sterge_profesor)
        buton_sterge_profesor.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")
        layout_butoane.addWidget(buton_sterge_profesor)
        layout_butoane.addStretch()
        
        layout.addLayout(layout_butoane)
        
        widget.setLayout(layout)
        self.actualizeaza_lista_profesori()
        return widget
    
    def adauga_profesor(self):
        nume = self.camp_nume_profesor.text().strip()
        
        if not nume:
            return
        
        zile = []
        if self.checkbox_luni.isChecked():
            zile.append("Luni")
        if self.checkbox_marti.isChecked():
            zile.append("Marți")
        if self.checkbox_miercuri.isChecked():
            zile.append("Miercuri")
        if self.checkbox_joi.isChecked():
            zile.append("Joi")
        if self.checkbox_vineri.isChecked():
            zile.append("Vineri")
        
        if len(zile) == 0:
            return
        
        profesor = Profesor(None, nume, zile)
        id_profesor = self.manager_bd.salveaza_profesor(profesor)
        
        if id_profesor:
            self.camp_nume_profesor.clear()
            self.checkbox_luni.setChecked(False)
            self.checkbox_marti.setChecked(False)
            self.checkbox_miercuri.setChecked(False)
            self.checkbox_joi.setChecked(False)
            self.checkbox_vineri.setChecked(False)
            self.actualizeaza_lista_profesori()
            self.actualizeaza_combo_profesori()
    
    def sterge_profesor(self):
        item_selectat = self.lista_profesori.currentItem()
        if not item_selectat:
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Confirmare")
        msg.setText("Sigur doriți să ștergeți acest profesor?")
        msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        buton_da = msg.addButton("Da", QMessageBox.YesRole)
        buton_nu = msg.addButton("Nu", QMessageBox.NoRole)
        msg.exec_()
        
        if msg.clickedButton() == buton_da:
            id_profesor = item_selectat.data(Qt.UserRole)
            if self.manager_bd.sterge_profesor(id_profesor):
                self.actualizeaza_lista_profesori()
                self.actualizeaza_combo_profesori()
    
    def actualizeaza_lista_profesori(self):
        self.lista_profesori.clear()
        profesori = self.manager_bd.obtine_toti_profesorii()
        
        for prof in profesori:
            text = f"{prof.nume} ({', '.join(prof.zile_disponibile)})"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, prof.id)
            self.lista_profesori.addItem(item)
    
    def creaza_tab_grupe(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.camp_nume_grupa = QLineEdit()
        self.camp_nume_grupa.setPlaceholderText("Ex: FAF-201")
        form_layout.addRow("Nume grupă:", self.camp_nume_grupa)
        
        buton_adauga_grupa = QPushButton("Adaugă Grupă")
        buton_adauga_grupa.clicked.connect(self.adauga_grupa)
        buton_adauga_grupa.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px; font-weight: bold;")
        
        layout.addLayout(form_layout)
        layout.addWidget(buton_adauga_grupa)
        
        layout.addWidget(QLabel("Listă grupe:"))
        self.lista_grupe = QListWidget()
        layout.addWidget(self.lista_grupe)
        
        layout_butoane = QHBoxLayout()
        buton_sterge_grupa = QPushButton("Șterge Grupă")
        buton_sterge_grupa.clicked.connect(self.sterge_grupa)
        buton_sterge_grupa.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")
        layout_butoane.addWidget(buton_sterge_grupa)
        layout_butoane.addStretch()
        
        layout.addLayout(layout_butoane)
        
        widget.setLayout(layout)
        self.actualizeaza_lista_grupe()
        return widget
    
    def adauga_grupa(self):
        nume = self.camp_nume_grupa.text().strip()
        
        if not nume:
            return
        
        grupa = Grupa(None, nume)
        id_grupa = self.manager_bd.salveaza_grupa(grupa)
        
        if id_grupa:
            self.camp_nume_grupa.clear()
            self.actualizeaza_lista_grupe()
            self.actualizeaza_lista_grupe_materii()
    
    def sterge_grupa(self):
        item_selectat = self.lista_grupe.currentItem()
        if not item_selectat:
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Confirmare")
        msg.setText("Sigur doriți să ștergeți această grupă?")
        msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        buton_da = msg.addButton("Da", QMessageBox.YesRole)
        buton_nu = msg.addButton("Nu", QMessageBox.NoRole)
        msg.exec_()
        
        if msg.clickedButton() == buton_da:
            id_grupa = item_selectat.data(Qt.UserRole)
            if self.manager_bd.sterge_grupa(id_grupa):
                self.actualizeaza_lista_grupe()
                self.actualizeaza_lista_grupe_materii()
    
    def actualizeaza_lista_grupe(self):
        self.lista_grupe.clear()
        grupe = self.manager_bd.obtine_toate_grupele()
        
        for grupa in grupe:
            item = QListWidgetItem(grupa.nume)
            item.setData(Qt.UserRole, grupa.id)
            self.lista_grupe.addItem(item)
    
    def creaza_tab_sali(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.camp_nume_sala = QLineEdit()
        self.camp_nume_sala.setPlaceholderText("Ex: B201")
        form_layout.addRow("Nume sală:", self.camp_nume_sala)
        
        buton_adauga_sala = QPushButton("Adaugă Sală")
        buton_adauga_sala.clicked.connect(self.adauga_sala)
        buton_adauga_sala.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;")
        
        layout.addLayout(form_layout)
        layout.addWidget(buton_adauga_sala)
        
        layout.addWidget(QLabel("Listă săli:"))
        self.lista_sali = QListWidget()
        layout.addWidget(self.lista_sali)
        
        layout_butoane = QHBoxLayout()
        buton_sterge_sala = QPushButton("Șterge Sală")
        buton_sterge_sala.clicked.connect(self.sterge_sala)
        buton_sterge_sala.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")
        layout_butoane.addWidget(buton_sterge_sala)
        layout_butoane.addStretch()
        
        layout.addLayout(layout_butoane)
        
        widget.setLayout(layout)
        self.actualizeaza_lista_sali()
        return widget
    
    def adauga_sala(self):
        nume = self.camp_nume_sala.text().strip()
        
        if not nume:
            return
        
        sala = Sala(None, nume)
        id_sala = self.manager_bd.salveaza_sala(sala)
        
        if id_sala:
            self.camp_nume_sala.clear()
            self.actualizeaza_lista_sali()
    
    def sterge_sala(self):
        item_selectat = self.lista_sali.currentItem()
        if not item_selectat:
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Confirmare")
        msg.setText("Sigur doriți să ștergeți această sală?")
        msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        buton_da = msg.addButton("Da", QMessageBox.YesRole)
        buton_nu = msg.addButton("Nu", QMessageBox.NoRole)
        msg.exec_()
        
        if msg.clickedButton() == buton_da:
            id_sala = item_selectat.data(Qt.UserRole)
            if self.manager_bd.sterge_sala(id_sala):
                self.actualizeaza_lista_sali()
    
    def actualizeaza_lista_sali(self):
        self.lista_sali.clear()
        sali = self.manager_bd.obtine_toate_salile()
        
        for sala in sali:
            item = QListWidgetItem(sala.nume)
            item.setData(Qt.UserRole, sala.id)
            self.lista_sali.addItem(item)
    
    def creaza_tab_materii(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.camp_nume_materie = QLineEdit()
        self.camp_nume_materie.setPlaceholderText("Ex: Programare Java")
        form_layout.addRow("Nume materie:", self.camp_nume_materie)
        
        layout.addLayout(form_layout)
        
        grup_componente = QGroupBox("Componente Materii:")
        layout_componente = QFormLayout()
        
        layout_curs = QHBoxLayout()
        self.combo_profesor_curs = QComboBox()
        layout_curs.addWidget(self.combo_profesor_curs, 3)
        self.spin_ore_curs = QSpinBox()
        self.spin_ore_curs.setMinimum(0)
        self.spin_ore_curs.setMaximum(7)
        self.spin_ore_curs.setValue(0)
        layout_curs.addWidget(self.spin_ore_curs, 1)
        layout_componente.addRow("Curs:", layout_curs)
        
        layout_seminar = QHBoxLayout()
        self.combo_profesor_seminar = QComboBox()
        layout_seminar.addWidget(self.combo_profesor_seminar, 3)
        self.spin_ore_seminar = QSpinBox()
        self.spin_ore_seminar.setMinimum(0)
        self.spin_ore_seminar.setMaximum(7)
        self.spin_ore_seminar.setValue(0)
        layout_seminar.addWidget(self.spin_ore_seminar, 1)
        layout_componente.addRow("Seminar:", layout_seminar)
        
        layout_laborator = QHBoxLayout()
        self.combo_profesor_laborator = QComboBox()
        layout_laborator.addWidget(self.combo_profesor_laborator, 3)
        self.spin_ore_laborator = QSpinBox()
        self.spin_ore_laborator.setMinimum(0)
        self.spin_ore_laborator.setMaximum(7)
        self.spin_ore_laborator.setValue(0)
        layout_laborator.addWidget(self.spin_ore_laborator, 1)
        layout_componente.addRow("Laborator:", layout_laborator)
        
        grup_componente.setLayout(layout_componente)
        layout.addWidget(grup_componente)
        
        grup_grupe = QGroupBox("Grupe asignate:")
        layout_grupe = QVBoxLayout()
        self.lista_grupe_materii = QListWidget()
        self.lista_grupe_materii.setSelectionMode(QAbstractItemView.MultiSelection)
        layout_grupe.addWidget(self.lista_grupe_materii)
        grup_grupe.setLayout(layout_grupe)
        layout.addWidget(grup_grupe)
        
        buton_adauga_materie = QPushButton("Adaugă Materie")
        buton_adauga_materie.clicked.connect(self.adauga_materie)
        buton_adauga_materie.setStyleSheet("background-color: #e67e22; color: white; padding: 8px; font-weight: bold;")
        layout.addWidget(buton_adauga_materie)
        
        layout.addWidget(QLabel("Listă materii:"))
        self.lista_materii = QListWidget()
        layout.addWidget(self.lista_materii)
        
        layout_butoane = QHBoxLayout()
        buton_sterge_materie = QPushButton("Șterge Materie")
        buton_sterge_materie.clicked.connect(self.sterge_materie)
        buton_sterge_materie.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")
        layout_butoane.addWidget(buton_sterge_materie)
        layout_butoane.addStretch()
        
        layout.addLayout(layout_butoane)
        
        widget.setLayout(layout)
        self.actualizeaza_combo_profesori()
        self.actualizeaza_lista_grupe_materii()
        self.actualizeaza_lista_materii()
        return widget
    
    def actualizeaza_combo_profesori(self):
        self.combo_profesor_curs.clear()
        self.combo_profesor_seminar.clear()
        self.combo_profesor_laborator.clear()
        
        self.combo_profesor_curs.addItem("Fără profesor", None)
        self.combo_profesor_seminar.addItem("Fără profesor", None)
        self.combo_profesor_laborator.addItem("Fără profesor", None)
        
        profesori = self.manager_bd.obtine_toti_profesorii()
        
        for prof in profesori:
            self.combo_profesor_curs.addItem(prof.nume, prof.id)
            self.combo_profesor_seminar.addItem(prof.nume, prof.id)
            self.combo_profesor_laborator.addItem(prof.nume, prof.id)
    
    def actualizeaza_lista_grupe_materii(self):
        self.lista_grupe_materii.clear()
        grupe = self.manager_bd.obtine_toate_grupele()
        
        for grupa in grupe:
            item = QListWidgetItem(grupa.nume)
            item.setData(Qt.UserRole, grupa.id)
            self.lista_grupe_materii.addItem(item)
    
    def adauga_materie(self):
        nume_materie = self.camp_nume_materie.text().strip()
        
        if not nume_materie:
            return
        
        ore_curs = self.spin_ore_curs.value()
        ore_seminar = self.spin_ore_seminar.value()
        ore_laborator = self.spin_ore_laborator.value()
        
        if ore_curs == 0 and ore_seminar == 0 and ore_laborator == 0:
            return
        
        items_selectate = self.lista_grupe_materii.selectedItems()
        if len(items_selectate) == 0:
            return
        
        lista_id_grupe = [item.data(Qt.UserRole) for item in items_selectate]
        
        profesori = self.manager_bd.obtine_toti_profesorii()
        
        profesor_curs = None
        id_curs = self.combo_profesor_curs.currentData()
        if id_curs and ore_curs > 0:
            profesor_curs = next((p for p in profesori if p.id == id_curs), None)
        
        profesor_seminar = None
        id_seminar = self.combo_profesor_seminar.currentData()
        if id_seminar and ore_seminar > 0:
            profesor_seminar = next((p for p in profesori if p.id == id_seminar), None)
        
        profesor_laborator = None
        id_laborator = self.combo_profesor_laborator.currentData()
        if id_laborator and ore_laborator > 0:
            profesor_laborator = next((p for p in profesori if p.id == id_laborator), None)
        
        ore_total = ore_curs + ore_seminar + ore_laborator
        
        materie = Materie(
            None, nume_materie, ore_total, [],
            profesor_curs, ore_curs,
            profesor_seminar, ore_seminar,
            profesor_laborator, ore_laborator
        )
        
        id_materie = self.manager_bd.salveaza_materie(materie, lista_id_grupe)
        
        if id_materie:
            self.camp_nume_materie.clear()
            self.spin_ore_curs.setValue(0)
            self.spin_ore_seminar.setValue(0)
            self.spin_ore_laborator.setValue(0)
            self.actualizeaza_lista_materii()
    
    def sterge_materie(self):
        item_selectat = self.lista_materii.currentItem()
        if not item_selectat:
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Confirmare")
        msg.setText("Sigur doriți să ștergeți această materie?")
        msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        buton_da = msg.addButton("Da", QMessageBox.YesRole)
        buton_nu = msg.addButton("Nu", QMessageBox.NoRole)
        msg.exec_()
        
        if msg.clickedButton() == buton_da:
            id_materie = item_selectat.data(Qt.UserRole)
            if self.manager_bd.sterge_materie(id_materie):
                self.actualizeaza_lista_materii()
    
    def actualizeaza_lista_materii(self):
        self.lista_materii.clear()
        materii = self.manager_bd.obtine_toate_materiile()
        
        for materie in materii:
            item = QListWidgetItem(str(materie))
            item.setData(Qt.UserRole, materie.id)
            self.lista_materii.addItem(item)