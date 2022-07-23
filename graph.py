import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QCheckBox, QComboBox

def read_file(FileDir): # Takes in file directory & Reads it
    #print(type(FileDir[0]))
    #print(pd.read_csv('C:/Users/Joachim/Desktop/Coding Projects/Python Projects/Public Repos/SgEnable/Automating_Excel_Data_Transfer/TestQuery.csv'))
    return (pd.read_csv(FileDir[0]))

def main(centre,checklist):
    print(read_file(fname))
    print('This is main')
    print(centre)
    print(checklist)

# GUI Display
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load the ui file
        uic.loadUi("graphmain.ui",self)

        # Define our widgets
        self.port_from_button = self.findChild(QPushButton,"Browse")
        self.port_from_label = self.findChild(QLabel,"FileName")
        self.scroller = self.findChild(QComboBox,"Scroller")
        self.Capacity_CB = self.findChild(QCheckBox,"Capacity_CheckBox")
        self.Enrollment_CB = self.findChild(QCheckBox,"Enrollment_CheckBox")
        self.Waitlist_CB = self.findChild(QCheckBox,"Waitlist_CheckBox")
        self.Vacancy_CB = self.findChild(QCheckBox,"Vacancy_CheckBox")
        # self.port_to_button = self.findChild(QPushButton,"Port_To_Button")
        # self.port_to_label = self.findChild(QLabel,"Port_To_Label")
        # self.sheet_name_text = self.findChild(QTextEdit,"Sheet_Name_Text")
        self.submit_button = self.findChild(QPushButton,"Submit")
        self.quit_button = self.findChild(QPushButton,"Quit")

        # Click the dropdown box
        self.port_from_button.clicked.connect(self.port_from_clicker)
        self.submit_button.clicked.connect(self.submit_click)
        self.quit_button.clicked.connect(self.quit_click)

        # Show the app
        self.show()

    def checked_box(self): #checks which boxes are ticked and adds them to a list
        list_of_checkboxes = [self.Capacity_CB, self.Enrollment_CB, self.Waitlist_CB, self.Vacancy_CB]
        list_of_checked = []
        for x in list_of_checkboxes:
            if x.isChecked() == True: # check if box is checked if checked append the name into a list
                list_of_checked.append(x.text())
        return list_of_checked

    def quit_click(self): # to run when quit button is clicked
        self.close() # closes the window
    
    def submit_click(self): # to run when submit button is clicked
        #print(self.scroller.currentText())
        #print(self.checked_box())
        self.close() # closes the window
        main(self.scroller.currentText(),self.checked_box())
    
    def load_data(self): # Loads data and puts the different centre names into the scroller
        #print()
        self.scroller.addItems((read_file(fname))['SPName'].unique()) # search for centre names and puts them in a list into the scroller
        self.scroller.adjustSize() # adjust scroller size to fit biggest string

    def port_from_clicker(self):
        global PortFromFile, Port_From_Path, fname
        fname = QFileDialog.getOpenFileName(self, "Open CSV File", "","Excel Files (*.csv)") # open a file window and only allow CSV files to be seen

        # Output filename to screen
        if fname:
            Port_From_Path = fname[0]
            print(Port_From_Path)
            x = ((str(fname[0])).split('/'))[-1]
            PortFromFile = x
            self.port_from_label.setText(x)
        self.load_data()

# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()