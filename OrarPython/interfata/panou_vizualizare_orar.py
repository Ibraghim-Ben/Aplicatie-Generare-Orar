from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
                             QMessageBox, QHeaderView, QGroupBox, QDialog, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from baza_date.manager_bd import ManagerBazaDate
from utilitare.constante import INTERVALE_ORARE, ZILE_LUCRATOARE


class DialogSelectareOrar(QDialog):
    def __init__(self, orare, titlu, mesaj, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titlu)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        
        self.orare = orare
        self.orar_selectat_id = None
        
        layout = QVBoxLayout()
        
        label_mesaj = QLabel(mesaj)
        layout.addWidget(label_mesaj)
        
        self.lista_orare = QListWidget()
        for orar in orare:
            text = f"{orar['nume']} ({orar['data']}) - {orar['algoritm']}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, orar['id'])
            self.lista_orare.addItem(item)
        
        if len(orare) > 0:
            self.lista_orare.setCurrentRow(0)
        
        layout.addWidget(self.lista_orare)
        
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
    
    def obtine_id_selectat(self):
        item_curent = self.lista_orare.currentItem()
        if item_curent:
            return item_curent.data(Qt.UserRole)
        return None


class PanouVizualizareOrar(QWidget):
    
    def __init__(self, panou_generare):
        super().__init__()
        self.manager_bd = ManagerBazaDate()
        self.panou_generare = panou_generare
        self.orar_curent = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titlu = QLabel("Vizualizare Orar Universitar")
        titlu.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(titlu)
        
        grup_filtrare = QGroupBox("Opțiuni Vizualizare:")
        layout_filtrare = QHBoxLayout()
        
        layout_filtrare.addWidget(QLabel("Filtrare după:"))
        
        self.combo_tip_filtrare = QComboBox()
        self.combo_tip_filtrare.addItems(["Grupă", "Profesor", "Sală"])
        self.combo_tip_filtrare.currentTextChanged.connect(self.actualizeaza_optiuni_filtrare)
        layout_filtrare.addWidget(self.combo_tip_filtrare)
        
        self.combo_optiuni_filtrare = QComboBox()
        layout_filtrare.addWidget(self.combo_optiuni_filtrare)
        
        buton_incarca_generat = QPushButton("Încarcă Orar Generat")
        buton_incarca_generat.clicked.connect(self.incarca_orar_generat)
        buton_incarca_generat.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px; font-weight: bold;")
        layout_filtrare.addWidget(buton_incarca_generat)
        
        buton_incarca_salvat = QPushButton("Încarcă Orar Salvat")
        buton_incarca_salvat.clicked.connect(self.incarca_orar_salvat)
        buton_incarca_salvat.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        layout_filtrare.addWidget(buton_incarca_salvat)
        
        buton_sterge_salvat = QPushButton("Șterge Orar Salvat")
        buton_sterge_salvat.clicked.connect(self.sterge_orar_salvat)
        buton_sterge_salvat.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; font-weight: bold;")
        layout_filtrare.addWidget(buton_sterge_salvat)
        
        buton_filtreaza = QPushButton("Filtrează")
        buton_filtreaza.clicked.connect(self.filtreaza_orar)
        buton_filtreaza.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px; font-weight: bold;")
        layout_filtrare.addWidget(buton_filtreaza)
        
        layout_filtrare.addStretch()
        
        grup_filtrare.setLayout(layout_filtrare)
        layout.addWidget(grup_filtrare)
        
        self.tabel_orar = QTableWidget()
        self.tabel_orar.setColumnCount(6)
        self.tabel_orar.setHorizontalHeaderLabels(["Interval"] + ZILE_LUCRATOARE)
        self.tabel_orar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabel_orar.setAlternatingRowColors(True)
        self.tabel_orar.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #bdc3c7;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #2c3e50;
            }
        """)
        
        layout.addWidget(self.tabel_orar)
        
        self.eticheta_info = QLabel("Încărcați un orar pentru a-l vizualiza")
        self.eticheta_info.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 10px;")
        layout.addWidget(self.eticheta_info)
        
        self.setLayout(layout)
        self.actualizeaza_optiuni_filtrare()
    
    def actualizeaza_optiuni_filtrare(self):
        self.combo_optiuni_filtrare.clear()
        
        tip = self.combo_tip_filtrare.currentText()
        
        if tip == "Grupă":
            grupe = self.manager_bd.obtine_toate_grupele()
            for grupa in grupe:
                self.combo_optiuni_filtrare.addItem(grupa.nume, grupa.id)
        elif tip == "Profesor":
            profesori = self.manager_bd.obtine_toti_profesorii()
            for prof in profesori:
                self.combo_optiuni_filtrare.addItem(prof.nume, prof.id)
        else:
            sali = self.manager_bd.obtine_toate_salile()
            for sala in sali:
                self.combo_optiuni_filtrare.addItem(sala.nume, sala.id)
    
    def incarca_orar_generat(self):
        orar_temp = self.panou_generare.obtine_orar_generat()
        
        if orar_temp and len(orar_temp.inregistrari) > 0:
            self.orar_curent = orar_temp
            self.filtreaza_orar()
    
    def incarca_orar_salvat(self):
        orare = self.manager_bd.obtine_lista_orare()
        
        if len(orare) == 0:
            return
        
        dialog = DialogSelectareOrar(orare, "Încarcă Orar Salvat", "Selectați orarul:", self)
        
        if dialog.exec_() == QDialog.Accepted:
            id_orar = dialog.obtine_id_selectat()
            if id_orar:
                self.orar_curent = self.manager_bd.incarca_orar(id_orar)
                if self.orar_curent:
                    self.filtreaza_orar()
    
    def sterge_orar_salvat(self):
        orare = self.manager_bd.obtine_lista_orare()
        
        if len(orare) == 0:
            return
        
        dialog = DialogSelectareOrar(orare, "Șterge Orar Salvat", "Selectați orarul de șters:", self)
        
        if dialog.exec_() == QDialog.Accepted:
            id_orar = dialog.obtine_id_selectat()
            if id_orar:
                msg = QMessageBox()
                msg.setWindowTitle("Confirmare")
                msg.setText("Sigur doriți să ștergeți acest orar din baza de date?")
                msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
                buton_da = msg.addButton("Da", QMessageBox.YesRole)
                buton_nu = msg.addButton("Nu", QMessageBox.NoRole)
                msg.exec_()
                
                if msg.clickedButton() == buton_da:
                    if self.manager_bd.sterge_orar(id_orar):
                        self.eticheta_info.setText("Orar șters cu succes!")
    
    def filtreaza_orar(self):
        if not self.orar_curent:
            return
        
        tip_filtrare = self.combo_tip_filtrare.currentText()
        id_selectat = self.combo_optiuni_filtrare.currentData()
        nume_selectat = self.combo_optiuni_filtrare.currentText()
        
        if id_selectat is None:
            return
        
        if tip_filtrare == "Grupă":
            inregistrari = [inreg for inreg in self.orar_curent.inregistrari if inreg.grupa.id == id_selectat]
            self.eticheta_info.setText(f"Orar pentru grupa: {nume_selectat} | Total lecții: {len(inregistrari)}")
        elif tip_filtrare == "Profesor":
            inregistrari = [inreg for inreg in self.orar_curent.inregistrari if inreg.profesor.id == id_selectat]
            self.eticheta_info.setText(f"Orar pentru profesorul: {nume_selectat} | Total lecții: {len(inregistrari)}")
        else:
            inregistrari = [inreg for inreg in self.orar_curent.inregistrari if inreg.sala.id == id_selectat]
            self.eticheta_info.setText(f"Orar pentru sala: {nume_selectat} | Total lecții: {len(inregistrari)}")
        
        self.afiseaza_orar_in_tabel(inregistrari)
    
    def afiseaza_orar_in_tabel(self, inregistrari):
        self.tabel_orar.setRowCount(7)
        
        for row in range(7):
            interval = INTERVALE_ORARE[row + 1]
            item_interval = QTableWidgetItem(f"{interval[0]}\n{interval[1]}")
            item_interval.setTextAlignment(Qt.AlignCenter)
            item_interval.setBackground(QColor("#ecf0f1"))
            self.tabel_orar.setItem(row, 0, item_interval)
        
        for col in range(1, 6):
            for row in range(7):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                self.tabel_orar.setItem(row, col, item)
        
        for inreg in inregistrari:
            col_index = ZILE_LUCRATOARE.index(inreg.zi) + 1
            row_index = inreg.numar_interval - 1
            
            text = f"{inreg.materie.nume}\n{inreg.sala.nume}\n{inreg.profesor.nume}"
            
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("#3498db"))
            item.setForeground(QColor("white"))
            
            self.tabel_orar.setItem(row_index, col_index, item)
        
        self.tabel_orar.resizeRowsToContents()