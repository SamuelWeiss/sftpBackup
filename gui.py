import sys
from PyQt4 import QtGui

# Connection = {}

class GuiApp(QtGui.QWidget):

    def __init__(self):
        super(GuiApp, self).__init__()

        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()

        self.setLayout(self.grid)

        self.generateServerInformation()
        self.generateBackupSettings()

        self.setGeometry(600,300,1000,170)
        self.setWindowTitle('SFTP Backup')
        self.show()

    def initLabel(self, text, row, col):
        label = QtGui.QLabel(self)

        label.setText(text)
        label.adjustSize()

        self.grid.addWidget(label, row, col)
        return label

    def initEdit(self, row, col):
        edit = QtGui.QLineEdit(self)

        self.grid.addWidget(edit, row, col)
        return edit

    def initCombo(self, choices, row, col):
        combo = QtGui.QComboBox(self)

        for x in range(0, len(choices)):
            combo.addItem(choices[x])

        self.grid.addWidget(combo, row, col)
        return combo

    def initButton(self, text, call, row, col):
        button = QtGui.QPushButton(text, self)

        button.clicked.connect(call)
        button.adjustSize()

        self.grid.addWidget(button, row, col)
        return button




    def generateServerInformation(self):
        self.serverTitle = self.initLabel("-- Server Information --", 0, 0)
        
        self.serverNameLabel = self.initLabel("Server Name", 1, 0)
        self.serverNameEdit = self.initEdit(2, 0)

        self.destinationLabel = self.initLabel("Destination", 1, 1)
        self.destinationEdit = self.initEdit(2, 1)

        self.usernameLabel = self.initLabel("Username", 3, 0)
        self.usernameEdit = self.initEdit(4, 0)

        self.passwordLabel = self.initLabel("Password", 3, 1)
        self.passwordEdit = self.initEdit(4, 1)

    def generateBackupSettings(self):
        self.backupTitle = self.initLabel("-- Backup Settings --", 0, 2)

        patternOptions = ['--number--', 'one', 'two']
        self.patternLabel = self.initLabel("Pattern", 1, 2)
        self.patternCombo = self.initCombo(patternOptions, 2, 2)

        frequencyUnitOptions = ['--unit--', 'one', 'two']
        self.frequencyLabel = self.initLabel("Frequency", 3, 2)
        self.frequencyEdit = self.initEdit(4, 2)
        self.frequencyUnitCombo = self.initCombo(frequencyUnitOptions, 5, 2)

        functionOptions = ['--functions--', 'one', 'two']
        self.functionLabel  = self.initLabel("Function", 1, 3)
        self.functionCombo = self.initCombo(patternOptions, 2, 3)

        self.selectedLabel = self.initLabel("* did not select a folder *", 0, 4)
        self.selectedLabel.setStyleSheet("QLabel {color : red;}")
        self.folderLabel = self.initLabel("Folder to Back Up", 1, 4)
        self.browseButton = self.initButton("Browse", self.browse, 2, 4)

    def browse(self):
        self.directory = QtGui.QFileDialog.getExistingDirectory(self, 'Folder to Back Up')
        self.selectedLabel.setText("* did select a folder to back up *")
        self.selectedLabel.setStyleSheet("QLabel {color : green;}")

















def start():

        # Connections['connection'] = connection
        app = QtGui.QApplication(sys.argv)
        guiApp = GuiApp()
        sys.exit(app.exec_())

if __name__ == '__main__':
        start()
