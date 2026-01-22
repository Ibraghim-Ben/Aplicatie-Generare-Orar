from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox, QAction
from PyQt5.QtCore import Qt
from interfata.panou_date_initiale import PanouDateInitiale
from interfata.panou_generare_orar import PanouGenerareOrar
from interfata.panou_vizualizare_orar import PanouVizualizareOrar


class FerestraPrincipala(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Generator Automat de Orar Universitar")
        self.setGeometry(100, 100, 1400, 900)
        
        self.creaza_meniu()
        
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        layout_principal = QVBoxLayout()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                background: white;
            }
            QTabBar::tab {
                background: #ecf0f1;
                color: #2c3e50;
                padding: 12px 30px;
                margin-right: 2px;
                font-weight: bold;
                font-size: 15px;
                min-width: 200px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background: #5dade2;
                color: white;
            }
        """)
        
        self.panou_date = PanouDateInitiale()
        self.panou_generare = PanouGenerareOrar()
        self.panou_vizualizare = PanouVizualizareOrar(self.panou_generare)
        
        self.tab_widget.addTab(self.panou_date, "📚 Date Inițiale")
        self.tab_widget.addTab(self.panou_generare, "⚙️ Generare Orar")
        self.tab_widget.addTab(self.panou_vizualizare, "📅 Vizualizare Orar")
        
        self.tab_widget.tabBar().setExpanding(False)
        
        layout_principal.addWidget(self.tab_widget)
        
        widget_central.setLayout(layout_principal)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 19px;
            }
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
            }
            QListWidget {
                font-size: 14px;
            }
            QTableWidget {
                font-size: 14px;
            }
            QTextEdit {
                font-size: 14px;
            }
            QCheckBox {
                font-size: 14px;
            }
            QSpinBox {
                font-size: 14px;
                padding: 5px;
            }
        """)
    
    def creaza_meniu(self):
        bara_meniu = self.menuBar()
        
        meniu_ajutor = bara_meniu.addMenu("Ajutor")
        
        actiune_despre = QAction("Despre", self)
        actiune_despre.triggered.connect(self.afiseaza_despre)
        meniu_ajutor.addAction(actiune_despre)
    
    def afiseaza_despre(self):
        QMessageBox.about(self, "Despre Aplicație",
                         """
<h2>Generator Automat de Orar Universitar</h2>
<p><b>Versiunea:</b> 1.0</p>
<p><b>Anul:</b> 2025</p>

<p>Aplicație pentru generarea automată și optimizată a orarului universitar 
folosind trei algoritmi avansați:</p>

<ul>
<li><b>Backtracking</b> - Garantează găsirea soluției</li>
<li><b>A*</b> - Optimizează calitatea orarului</li>
<li><b>Hungarian Algorithm</b> - Cel mai rapid algoritm</li>
</ul>

<p><b>Tehnologii:</b> Python, PyQt5, SQLite</p>
                         """)
    
    def closeEvent(self, event):
        raspuns = QMessageBox.question(self, "Confirmare",
                                      "Sigur doriți să închideți aplicația?",
                                      QMessageBox.Yes | QMessageBox.No)
        
        if raspuns == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()