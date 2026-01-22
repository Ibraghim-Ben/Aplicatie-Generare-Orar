import sys
from PyQt5.QtWidgets import QApplication
from interfata.fereastra_principala import FerestraPrincipala


def main():
    aplicatie = QApplication(sys.argv)
    
    aplicatie.setStyle('Fusion')
    
    fereastra = FerestraPrincipala()
    fereastra.show()
    
    sys.exit(aplicatie.exec_())


if __name__ == '__main__':
    main()