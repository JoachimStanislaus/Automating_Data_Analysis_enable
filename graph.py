import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import sys
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QCheckBox, QComboBox, QListWidget, QLineEdit

def read_file(FileDir): # Takes in file directory & Reads it
    #print(type(FileDir[0]))
    #print(pd.read_csv('C:/Users/Joachim/Desktop/Coding Projects/Python Projects/Public Repos/SgEnable/Automating_Excel_Data_Transfer/TestQuery.csv'))
    return (pd.read_csv(FileDir[0]))

def main(centre,checklist):
    CreatedDataframe = (read_file(fname))
    #print(centre)
    #print(checklist)
    totalchecklist = ''
    countchecklist = 0
    for x in checklist:
        if countchecklist < len(checklist)-1:
            totalchecklist += x + ' , '
        else:
            totalchecklist += x
        countchecklist +=1
    CreatedDataframe["RepDate"] = pd.to_datetime(CreatedDataframe["RepDate"],format = "%d/%m/%Y")
    SortedbyName = CreatedDataframe.set_index('SPName')
    SortedbyName['Shortfall'] = SortedbyName['Capacity'] - (SortedbyName['Enrollment'] + SortedbyName['Waitlist'])
    SortedbyName['Demand'] = (SortedbyName['Enrollment'] + SortedbyName['Waitlist'])
    SortedbyName = SortedbyName.loc[centre]
    SortedbyName.sort_values(by='RepDate',inplace=True)
    #print(SortedbyName)
    if len(centre)>1:
        SortedbyName=(SortedbyName.groupby(SortedbyName['RepDate'].dt.date).sum())
        start_date = datetime.date(int(start_year),1,1)
        end_date = datetime.date(int(end_year),12,31)
        SortedbyName = (SortedbyName.loc[start_date:end_date])
    else:
        SortedbyName.set_index("RepDate", inplace = True)
        start_date = datetime.date(int(start_year),1,1)
        end_date = datetime.date(int(end_year),12,31)
        SortedbyName = (SortedbyName.loc[start_date:end_date])
        #print(SortedbyName)
    
    SortedbyName[checklist].plot(marker='.',markersize=10, title=f'{Graph_Title_Text}', figsize=(10,6)).get_figure().savefig(f'{Graph_Title_Text}.png')
    #plt.show()



# GUI Display
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load the ui file
        uic.loadUi("graphmain.ui",self)

        # Define our widgets
        self.port_from_button = self.findChild(QPushButton,"Browse")
        self.port_from_label = self.findChild(QLabel,"FileName")
        self.Scroll_List = self.findChild(QListWidget,"Scroll_List")
        self.Service_List = self.findChild(QListWidget,"Service_List")
        self.Capacity_CB = self.findChild(QCheckBox,"Capacity_CheckBox")
        self.Enrollment_CB = self.findChild(QCheckBox,"Enrollment_CheckBox")
        self.Waitlist_CB = self.findChild(QCheckBox,"Waitlist_CheckBox")
        self.Vacancy_CB = self.findChild(QCheckBox,"Vacancy_CheckBox")
        self.Shortfall_CB = self.findChild(QCheckBox,"Shortfall_CheckBox")
        self.Demand_CB = self.findChild(QCheckBox,"Demand_CheckBox")
        self.Start_Year_Scroller = self.findChild(QComboBox,"Start_Year")
        self.End_Year_Scroller = self.findChild(QComboBox,"End_Year")
        self.Graph_Title  = self.findChild(QLineEdit,"Graph_Title")
        self.submit_button = self.findChild(QPushButton,"Submit")
        self.quit_button = self.findChild(QPushButton,"Quit")

        # Click the dropdown box
        self.Scroll_List.itemClicked.connect(self.printItemText)
        self.Service_List.itemClicked.connect(self.printServiceText)
        self.port_from_button.clicked.connect(self.port_from_clicker)
        self.submit_button.clicked.connect(self.submit_click)
        self.quit_button.clicked.connect(self.quit_click)

        # Show the app
        self.show()

    def printItemText(self):
        items = self.Scroll_List.selectedItems()
        global Scroll_Selected_Items
        Scroll_Selected_Items = []

        for i in range(len(items)):
            Scroll_Selected_Items.append(str(self.Scroll_List.selectedItems()[i].text()))
        print(Scroll_Selected_Items)

    def printServiceText(self):
        Service = self.Service_List.selectedItems()
        global Scroll_Selected_Items
        Scroll_Selected_Items = []
        holderlst = []
        centrelist = (read_file(fname))['SPName'].unique()

        for i in range(len(Service)):
            Scroll_Selected_Items.append(str(self.Service_List.selectedItems()[i].text()))
        #print(Scroll_Selected_Items)
        for x in Scroll_Selected_Items:
            for centre in centrelist:
                if x in centre:
                    holderlst.append(centre)
        Scroll_Selected_Items = holderlst
        

    def checked_box(self): #checks which boxes are ticked and adds them to a list
        list_of_checkboxes = [self.Capacity_CB, self.Enrollment_CB, self.Waitlist_CB, self.Vacancy_CB, self.Shortfall_CB, self.Demand_CB]
        list_of_checked = []
        for x in list_of_checkboxes:
            if x.isChecked() == True: # check if box is checked if checked append the name into a list
                list_of_checked.append(x.text())
        return list_of_checked

    def quit_click(self): # to run when quit button is clicked
        self.close() # closes the window
    
    def submit_click(self): # to run when submit button is clicked
        global start_year, end_year, Graph_Title_Text
        start_year = self.Start_Year_Scroller.currentText()
        end_year = self.End_Year_Scroller.currentText()
        Graph_Title_Text = self.Graph_Title.text()
        #print(self.checked_box())
        #self.close() # closes the window
        main(Scroll_Selected_Items,self.checked_box())
    
    def load_data(self): # Loads data and puts the different centre names into the scroller
        self.Scroll_List.addItems((read_file(fname))['SPName'].unique()) # search for centre names and puts them in a list into the scroller
        self.Scroll_List.setMinimumWidth(self.Scroll_List.sizeHintForColumn(0)) # adjust scroller size to fit biggest string
        
        self.Service_List.addItems(['(ADH)','(Hostel)','(CDH)','(DAC)','(SW)']) # Adds Different Services Offered and puts them in a list into the scroller
        self.Service_List.setMinimumWidth(self.Scroll_List.sizeHintForColumn(0)) # adjust scroller size to fit biggest string
        
        emptylst=[]
        for x in ((read_file(fname))['RepDate'].unique()):
            x = int(x[-4:])
            emptylst.append(x)
        sortedlst = (list(set(emptylst)))
        sortedlst.sort()
        sortedlst = [str(i) for i in sortedlst]
        #print(sortedlst)
        self.Start_Year_Scroller.addItems(sortedlst) # search for centre names and puts them in a list into the scroller
        self.Start_Year_Scroller.adjustSize() # adjust scroller size to fit biggest string
        self.End_Year_Scroller.addItems(sortedlst) # search for centre names and puts them in a list into the scroller
        self.End_Year_Scroller.adjustSize() # adjust scroller size to fit biggest string

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