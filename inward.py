
import sys
from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox
from PyQt5 import QtWidgets
import re
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
import csv
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from datetime import datetime,date
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow
import logging
import qdarkstyle
import numpy



logging.basicConfig(filename=f'logs/{date.today()}.log', filemode='a', level=logging.INFO)
class LoginScreen(QDialog,QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.loginbtn.clicked.connect(self.loginfunction)
        
        pixmap = QPixmap('logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
  
        
        
       
        self.cname.setText("DTPL INWARD SYSTEM")
     


    def loginfunction(self):
        
        uname =self.uname.text()
        pwd = self.pwd.text()

        if len(uname)==0 and len(pwd)==0:
            self.showdialog("Please Enter ID and PASSWORD")
        elif len(uname) == 0:
            self.showdialog("Please Enter Username")
        elif len(pwd) == 0:
            self.showdialog("Please Enter The Password")
            

        else:
            try:
                conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                cr = conn.cursor()
                # print(f"SELECT PASSWORD FROM emplogin WHERE USERNAME = {uname}")
                query = 'SELECT password,username FROM emplogin WHERE username =\''+uname+"\'"
                try: 
                    cr.execute(query)
                    conf = cr.fetchone()[0]
                
                
                    if conf != pwd:
                        self.showdialog("Invalid Password")
                        
                    else:
                        logging.info(f"Successful login by user: {uname} at {datetime.now()}")
  

                        fillprofile = Form(uname)
                        widget.addWidget(fillprofile)
                        widget.setCurrentIndex(widget.currentIndex()+1)
                        
                        
                except Exception as e:
                    logging.error(f" Loggin attempt at {datetime.now()}")           
                    self.showdialog("Invalid User Name")   
                    
                    
                    
            except Exception as e:
                logging.error("error  ",e)           
                self.showdialog(e)  
   

            finally:
                conn.close()
        
    def showdialog(self,e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("This Error Occurs")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(msgbtn)
        retval = msg.exec_()      
       
class Form(QtWidgets.QMainWindow):
    
    offset = 0
    def __init__(self,uname):

        super(QMainWindow,self).__init__()
        loadUi("inward.ui",self)

        self.submit.clicked.connect(self.saveData)

        self.update1.hide()
        self.switch_2.hide()
        self.update1.clicked.connect(self.updateData)
        
        self.switch_2.clicked.connect(self.switchbtn)
        
        self.searchbtn.clicked.connect(self.search)
        self.next.clicked.connect(self.next1)
        self.previous.clicked.connect(self.previous1)
    
        pixmap = QPixmap('logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        
        self.exportcsv.clicked.connect(self.exportToCSV)

        
        
        try:
            year=["ALL DATA"]
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            cr.execute("SELECT YEAR(Entry_date) FROM Data group by YEAR(Entry_date) order by Year(Entry_date) desc")
            finyear = cr.fetchall()
 

            for b in finyear:
                for a in b:
                    year.append(f"FY - {str(a)}-{str(a+1)}")
                 
                
        except Exception as e:
            print(e)
            print("Error")        

        finally:
            conn.close()
                
        
        self.fyear.addItems(year)
        self.fyear.activated[str].connect(self.onSelectYear)
        if self.fyear != str():
            self.fyear = year[0]
            self.sdate = self.fyear
        
            
         
        self.fshow.clicked.connect(self.search)
        
        if uname == "Satish2002":
            adduser = QAction('Add User', self)
            adduser.triggered.connect(self.addUser)
            self.logout.addAction(adduser)
            
        
        exit_action = QAction('Logout', self)
        exit_action.triggered.connect(self.loggedout)
        self.logout.addAction(exit_action)


        
        f= open('Companyname.txt','r')
        for i in f:
            name =i
        f.close()
        self.companyname.setText(name)
        l1=[]

        
        try:
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            
            cr = conn.cursor()
            cr.execute("select DISTINCT company_name from Data")
            cn = cr.fetchall()
            for tp in cn:
                for it in tp:
                    l1.append(it)

            
        except Exception as e:
            print(e)
         
        finally:
            conn.close()
       
        completer = QCompleter(l1)

        # create line edit and add auto complete                                
      
        self.company.setCompleter(completer)
        l2=[]
        
        try:
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            cr.execute("Select DISTINCT item_name from Data")
            cn = cr.fetchall()
            for tp in cn:
                for it in tp:
                    l2.append(it)
   
            
        except Exception as e:
            print(e)

        finally:
            conn.close()
       
        completer1 = QCompleter(l2)

        # create line edit and add auto complete                                
      
        self.itemname.setCompleter(completer1)

        try:
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            if self.fyear =="ALL DATA":
                d = f"Select Count(*) from Data "
            else:
                d =f"Select Count(*) from Data WHERE Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31')"

            cr.execute(d)
            total = cr.fetchone()

            for a in total:
                total = a
                self.num_rows = a
            
            if total < self.offset:
                self.offset = 0
            self.total_entry.setText(f'{total}')
            showing = self.offset
            if total < showing+20:
               
                self.range.setText(f'{total}')  
            else:
                self.range.setText(f'{self.offset+20}')  
            self.showing.setText(f'{showing+1}')
            self.range.setText(f'{showing+20}')
            self.record.display(total)
 
            
        except Exception as e:
            print(e)
            print("Error")        

        finally:
            conn.close()
        try:
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            query = 'SELECT * FROM emplogin WHERE username =\''+uname+"\'"
            print(query)
            cr.execute(query)
            self.empdata= cr.fetchone()
       
            self.uname.setText(str(self.empdata[3]))
  
            
        except Exception as e:
            print(e)
            
            
        
        self.date.setText(str(date.today()))
        loc = ""
        f= open('Location.txt','r')
        for i in f:
            loc =i
        f.close()
                
        uomlist=[]
        f= open('uom.txt','r')
        for uomlt in f:
          uomlist.append(uomlt)
        lnlist = []
        for item in uomlist:
            lnlist.append(item.replace('\n',''))
              
        
                
        f.close()
        self.loc.setText(loc)
        self.uom.addItems(lnlist)
        
        self.uom.activated[str].connect(self.onSelect)
        if self.uom != str():
            self.uom = lnlist[0]

    
 
    
        srch=[]
        f= open('search.txt','r')
        for d in f:
          srch.append(d)
        searchlist = []
        for item in srch:
            searchlist.append(item.replace('\n',''))
        
        self.gsearch.addItems(searchlist)
        
        self.gsearch.activated[str].connect(self.onSelectSearch)
        if self.gsearch != str():
            self.gsearch = searchlist[0]
            
        
        self.tableViews()
        
    def onSelectYear(self,fyear):
        self.fyear = fyear 
        self.sdate = self.fyear[5:9]

    def addUser(self):
        print(self.empdata[1])
        if self.empdata[1] == "Satish2002":
            
            adduser = SignupScreen(self.empdata[1])
            
            widget.addWidget(adduser)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            logging.warning(f"Tried to add a User By {self.empdata[2]} at {datetime.now()}")
            self.showdialog("You Dont have the permision to add the user")
        
    def loggedout(self):
        
                # Create a QDialog instance
        dialog = QDialog()
        dialog.setWindowTitle("Logout Confirmation")

        # Create layout and widgets for the dialog
        layout = QVBoxLayout()
        message_label = QLabel("Do you want to log out?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        # Add widgets to the layout
        layout.addWidget(message_label)
        layout.addWidget(yes_button)
        layout.addWidget(no_button)

        # Set the layout for the dialog
        dialog.setLayout(layout)

        # Connect button actions (close the dialog)
        yes_button.clicked.connect(dialog.accept)
        no_button.clicked.connect(dialog.reject)

        # Show the login dialog
        # 
        result = dialog.exec_()

        # Handle the result of the dialog (e.g., check if it was accepted)
        if result == QDialog.Accepted:
            self.hide()
           
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
           
            logging.info(f"{self.empdata[1]}User Logged out Sucessfully at {datetime.now()}")
        else:
            self.show()

    def onSelectSearch(self,gsearch):
        self.gsearch = gsearch    
    
    def exportToCSV(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            

            try:
                self.csvdata.to_csv(file_path, index=False)
                print(f"Data exported to {file_path}")
                logging.info(f"Data exported to {file_path} by {self.empdata[1]} at  {datetime.now()}")
               
            except Exception as e:
                print(f"Error exporting data: {e}")

    def onSelect(self,uom):
        self.uom = uom
        
    def search(self):
        # self.tableView.clear()
        name_get = self.search1.text()


        try:
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cursor = conn.cursor()
            # self.tableView.setRowCount(cursor.rowcount) 
            
            limit = 20
            
            
                
            if name_get == None or name_get == '' and self.fyear != "ALL DATA":
           
                count_q = f"SELECT COUNT(*) AS num_rows FROM Data WHERE Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31')"
                
            elif name_get == None or name_get == '' and self.fyear == "ALL DATA":
           
                count_q = f"SELECT COUNT(*) AS num_rows FROM Data"

                
            elif self.gsearch == 'ALL' and self.fyear == "ALL DATA":
                
                count_q = f"Select count(*) from Data WHERE  COMPANY_NAME like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'  or ITEM_NAME like '%{name_get}%' or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%'" 
                
            elif self.gsearch == 'ALL' and self.fyear != "ALL DATA":
                
                count_q = f"Select count(*) from Data WHERE ( COMPANY_NAME like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'  or ITEM_NAME like '%{name_get}%' or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%') and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') " 
            
            elif self.gsearch == 'ENTRY_DATE' and self.fyear == "ALL DATA":
                count_q = f"Select count(*) from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'" 
                
            elif self.gsearch == 'ENTRY_DATE' and self.fyear != "ALL DATA":
                count_q = f"Select count(*) from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') "
                
        
            
            
            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear == "ALL DATA":
                
                count_q = f"SELECT COUNT(*) AS num_rows FROM Data WHERE {self.gsearch}= '{name_get}' or {self.gsearch} like '%{name_get}%'"
                
            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear != "ALL DATA":
                
                count_q = f"SELECT COUNT(*) AS num_rows FROM Data WHERE {self.gsearch}= '{name_get}' or {self.gsearch} like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31')"
                

            cursor.execute(count_q)
            row = cursor.fetchone() 
            self.num_rows = row[0]
            self.record.display(self.num_rows)
            if self.num_rows < self.offset:
                self.offset = 0

            self.total_entry.setText(f'{self.num_rows}')
            showing = self.offset
            # if self.num_rows < 20:
            if self.num_rows < showing+20:
                self.range.setText(f'{self.num_rows}')  
            else:
                self.range.setText(f'{self.offset+20}')  
            self.showing.setText(f'{showing+1}')
            
            
            list1=[]
            if name_get == None or name_get == '' and self.fyear != "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by ID desc"
                b += " limit "+ str(limit) + " offset " + str(self.offset)
                
            elif name_get == None or name_get == '' and self.fyear == "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data  order by ID desc"
                b += " limit "+ str(limit) + " offset " + str(self.offset)
            
            elif self.gsearch == 'ALL' and self.fyear != "ALL DATA" and name_get!="":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE (ID like '%{name_get}%' or COMPANY_NAME like '%{name_get}%' or ITEM_NAME like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'  or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%') and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc  limit "+ str(limit) + " offset " + str(self.offset)

            
            elif self.gsearch == 'ALL' and self.fyear == "ALL DATA" and name_get!="":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE ID like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'  or COMPANY_NAME like '%{name_get}%' or ITEM_NAME like '%{name_get}%' or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%' order by id desc  limit "+ str(limit) + " offset " + str(self.offset)

            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear != "ALL DATA" and name_get !="":
                
                b = f"SELECT ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark FROM Data WHERE {self.gsearch}= '{name_get}' or {self.gsearch} like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc  limit "+ str(limit) + " offset " + str(self.offset)
                
                
            elif self.gsearch == 'ENTRY_DATE' and self.fyear != "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc limit "+ str(limit) + " offset " + str(self.offset)
                
           
            elif self.gsearch == 'ENTRY_DATE' and self.fyear == "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'order by id desc limit "+ str(limit) + " offset " + str(self.offset)

            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear != "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE {self.gsearch} like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc limit "+ str(limit) + " offset " + str(self.offset)
                
            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear == "ALL DATA":
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE {self.gsearch} like '%{name_get}%' order by id desc limit "+ str(limit) + " offset " + str(self.offset)

            
                
                
            else:
                b = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data  order by id desc limit "+ str(limit) + " offset " + str(self.offset)




            csvl = []
            if name_get == None or name_get == '' and self.fyear != "ALL DATA":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by ID desc"
               
            elif name_get == None or name_get == '' and self.fyear == "ALL DATA":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data  order by ID desc"
        
            elif self.gsearch == 'ALL' and self.fyear != "ALL DATA" and name_get!="":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE (ID like '%{name_get}%' or COMPANY_NAME like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%' or ITEM_NAME like '%{name_get}%' or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%') and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc "
            
            elif self.gsearch == 'ALL' and self.fyear == "ALL DATA" and name_get!="":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE ID like '%{name_get}%' or DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%' or COMPANY_NAME like '%{name_get}%' or ITEM_NAME like '%{name_get}%' or QUANTITY like '%{name_get}%' or UOM like '%{name_get}%' OR CHALAN_NO like '%{name_get}%' or REMARK like '%{name_get}%' order by id desc "
            
            elif self.gsearch == 'ENTRY_DATE' and self.fyear != "ALL DATA":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc"
                
           
            elif self.gsearch == 'ENTRY_DATE' and self.fyear == "ALL DATA":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE DATE_FORMAT(ENTRY_DATE, '%Y-%m-%d') like '%{name_get}%'order by id desc "

            elif self.gsearch != 'ALL' and self.gsearch != 'ENTRY_DATE' and self.fyear != "ALL DATA":
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data WHERE {self.gsearch} like '%{name_get}%' and Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31') order by id desc "
            else:
                c = f"Select ID,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data  order by id desc"



            cursor.execute(c)
            csvd = cursor.fetchall()
            for d in csvd:
            
                csvl.append(list(d))
            
            self.csvdata = pd.DataFrame(
                csvl
                , columns = ['SR.NO.', 'Date', 'Company','Item', 'Quantity', 'UOM','Challan Number', 'Remark'])
    
        
            cursor.execute(b)
            data1 = cursor.fetchall()
            for d in data1:
                
                list1.append(list(d))
      
         
            self.data = pd.DataFrame(
                list1
                , columns = ['SR.NO.', 'Date', 'Company','Item', 'Quantity', 'UOM','Challan Number', 'Remark'])
            self.model = TableModel(self.data)
            self.tableView.setModel(self.model)
         
     
            self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            
            
            header = self.tableView.horizontalHeader()
            # header.setSectionResizeMode(2,QHeaderView.Stretch)
            header.setSectionResizeMode(3,QHeaderView.Stretch)
            # header.setSectionResizeMode(6,QHeaderView.Stretch)
            # header.setSectionResizeMode(7,QHeaderView.Stretch)
            header.setSectionResizeMode(4,QHeaderView.Fixed)
            header.resizeSection(0,20)
            header.resizeSection(6,130)
            header.resizeSection(2,300)
            header.resizeSection(1,160)
            header.resizeSection(5,20)
            header.resizeSection(7,300)
            
            self.tableView.setRowHeight(0,35)
            self.tableView.setRowHeight(1,35)
            self.tableView.setRowHeight(2,35)
            self.tableView.setRowHeight(3,35)
            self.tableView.setRowHeight(4,35)
            self.tableView.setRowHeight(5,35)
            self.tableView.setRowHeight(6,35)
            self.tableView.setRowHeight(7,35)
            self.tableView.setRowHeight(8,35)
            self.tableView.setRowHeight(9,35)
            self.tableView.setRowHeight(10,35)
            self.tableView.setRowHeight(11,35)
            self.tableView.setRowHeight(12,35)
            self.tableView.setRowHeight(13,35)
            self.tableView.setRowHeight(14,35)
            self.tableView.setRowHeight(15,35)
            self.tableView.setRowHeight(16,35)
            self.tableView.setRowHeight(17,35)
            self.tableView.setRowHeight(18,35)
            self.tableView.setRowHeight(19,35)
            self.tableView.setRowHeight(20,35)


            
        except Exception as e:
            print(e)
            print("Error")
                
        finally:
            conn.close()
                  
    def next1(self):
        try:
            limit = 20 
            if self.offset + limit <self.num_rows and self.offset< self.num_rows:

                self.offset = limit + self.offset
                self.search()
                
        except Exception as e:
            print(e)
                 
    def previous1(self):
        
        try:
            
              
            limit = 20
             
                
            if self.offset <= self.num_rows and self.offset-limit>=0 :
                self.offset = self.offset - limit
                self.search()
                
        except Exception as e:
            print(e)
            print("Error")
    
    def showdialog(self,e):
        msg = QMessageBox()
        # msg.setIcon(QMessageBox.information)
        msg.setText("This Error Occurs")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Error")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(msgbtn)
        retval = msg.exec_()
            
    def tableViews(self):
        try:
            list1=[]
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            if self.fyear == "ALL DATA":
                b = f"Select id,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data order by id desc limit 20"
            else:
                b = f"Select id,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data where Entry_date BETWEEN DATE('{self.sdate}-04-01') AND DATE('{int(self.sdate)+1}-03-31')  order by id desc limit 20"

            cr.execute(b)
            data1 = cr.fetchall()
            for d in data1:
                list1.append(list(d))
        
                
         
            self.data = pd.DataFrame(
                list1
                , columns = ['SR.NO.', 'Date', 'Company','Item', 'Quantity', 'UOM','Challan Number', 'Remark'])
            
            csvl = []
            
            if self.fyear =="ALL DATA":
                c = f"Select id,Entry_date,company_name,item_name,quantity,uom,chalan_no,remark from Data  order by id desc"
            else:
                c = b.replace("limit 20","")
            cr.execute(c)
            csvd = cr.fetchall()
            for d in csvd:
                
                csvl.append(list(d))
            
            self.csvdata = pd.DataFrame(
                csvl
                , columns = ['SR.NO.', 'Date', 'Company','Item', 'Quantity', 'UOM','Challan Number', 'Remark'])
            
         
                
        
            
            self.model = TableModel(self.data)
            self.tableView.setModel(self.model)
            # self.tableView.setTextAlignment(Qt.AlignLeft)

     
            self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.tableView.setRowHeight(0,35)
            self.tableView.setRowHeight(1,35)
            self.tableView.setRowHeight(2,35)
            self.tableView.setRowHeight(3,35)
            self.tableView.setRowHeight(4,35)
            self.tableView.setRowHeight(5,35)
            self.tableView.setRowHeight(6,35)
            self.tableView.setRowHeight(7,35)
            self.tableView.setRowHeight(8,35)
            self.tableView.setRowHeight(9,35)
            self.tableView.setRowHeight(10,35)
            self.tableView.setRowHeight(11,35)
            self.tableView.setRowHeight(12,35)
            self.tableView.setRowHeight(13,35)
            self.tableView.setRowHeight(14,35)
            self.tableView.setRowHeight(15,35)
            self.tableView.setRowHeight(16,35)
            self.tableView.setRowHeight(17,35)
            self.tableView.setRowHeight(18,35)
            self.tableView.setRowHeight(19,35)
            self.tableView.setRowHeight(20,35)
            # self.tableView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            
            
            header = self.tableView.horizontalHeader()

            

            header.setSectionResizeMode(3,QHeaderView.Stretch)
            # header.setSectionResizeMode(6,QHeaderView.Stretch)
            # header.setSectionResizeMode(7,QHeaderView.Stretch)
            header.setSectionResizeMode(4,QHeaderView.Fixed)
            header.resizeSection(0,20)
            header.resizeSection(6,130)
            header.resizeSection(2,300)
            header.resizeSection(1,160)
            header.resizeSection(5,20)
            header.resizeSection(7,300)

     

            
            
            self.tableView.clicked.connect( self.on_item_clicked)
        

        except Exception as e:
            print(e)

            
        finally:
            conn.close()

    def on_item_clicked(self, index):
        row = index.row()
        col = index.column()

        # Retrieve the text using the model's data method
        model = index.model()
        item = model.data(index, Qt.DisplayRole)
        
        if col == 0:
            try:
                conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                cr = conn.cursor()
                
                qry = f"SELECT COMPANY_NAME,ITEM_NAME,QUANTITY,UOM,CHALAN_NO,REMARK FROM Data where ID = {item}"

                cr.execute(qry)
                
                ulist = cr.fetchone()
 
                self.company.setText(str(ulist[0]))
            
                self.itemname.setText(str(ulist[1]))
                self.quantity.setText(str(ulist[2]))
                self.uom = ulist[3]
                  
                
                self.challan.setText(str(ulist[4]))
                self.remark.setText(str(ulist[5]))
                
                self.submit.hide()
                self.update1.show()
                self.switch_2.show()
                self.exportcsv.hide()
       
                self.pval = item
                
            except Exception as e:
                print(e)
   
                
            finally:
                conn.close()

    def updateData(self):
        try:
            
            company=self.company.text()
                
            itemname = self.itemname.text()
            qt = self.quantity.text()
            uom = self.uom
                
            challan = self.challan.text()
            remark = self.remark.text()

            vld =[str(company),str(itemname),str(qt),str(uom),str(challan),str(remark)]
            if self.validate_input(vld): 

                conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                cr = conn.cursor()
                        
                qry = """
                            UPDATE Data
                            SET COMPANY_NAME = %s ,ITEM_NAME = %s, QUANTITY = %s, UOM = %s, CHALAN_NO = %s, REMARK = %s
                            WHERE ID = %s
                            """
                udata = [company,itemname,qt,uom,challan,remark,self.pval]
                cr.execute(qry,udata)
                        
                conn.commit()
                
                logging.info (f"Data of {id} is update at {datetime.now()} by {self.empdata[1]}")
                self.tableViews()
                    
                    
        except Exception as e:
            conn.rollback()
            print(e)
                
        finally:
            conn.close()
    
    def switchbtn(self):
        
        self.submit.show()
        self.update1.hide()
        self.exportcsv.show()
        self.switch_2.hide()
        self.company.setText("")
            
        self.itemname.setText("")
        self.quantity.setText("")
        # self.uom.addItems()    
        self.challan.setText("")
        self.remark.setText("")
        
    def saveData(self):
        company=self.company.text()
        loc=self.loc.text()
        itemname = self.itemname.text()
        qt = self.quantity.text()
        uom = self.uom
    
        challan = self.challan.text()
        remark = self.remark.text()
        
        
        
        
        
        if len(challan)>=21:
            self.showdialog("Length of Challan Should be Less than 20")
            
        elif len(remark)>=51:
            
            self.showdialog("Length of Remark Should be Less than 50")
        
        elif len(company) == 0 or len(loc)==0 or len(itemname)==0 or float(qt)<0 :
            self.showdialog("All * Fields are Mandatory ")

        
            
          
   
            
        else:
            vld =[str(company),str(loc),str(itemname),str(qt),str(uom),str(challan),str(remark)]
            if self.validate_input(vld):
           
                
       
                try:
                    conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                    cr = conn.cursor()
                

                    data =[str(company),str(loc),str(itemname),float(qt),str(uom),str(challan),str(remark),str(datetime.now())]
                    cr.execute(f"INSERT INTO Data (COMPANY_NAME,LOC,ITEM_NAME,QUANTITY,UOM,CHALAN_NO,REMARK,ENTRY_DATE) values(%s,%s,%s,%s,%s,%s,%s,%s)",data)
                    
                    
                    self.showdialog("You Data Save Sucessfully ")
                    
                    conn.commit()
                    self.tableViews()
                    self.company.setText("")
            
                    self.itemname.setText("")
                    self.quantity.setText("")
                
                    self.challan.setText("")
                    self.remark.setText("")
                    logging.info(f"COMPANY_NAME = {str(company)},ITEM_NAME={str(itemname)},QUANTITY={float(qt)},UOM = {str(uom)},CHALAN_NO={str(challan)},REMARK ={str(remark)} this Data is Inserted by {self.empdata[1] } at {datetime.now()} Sucessfully")
                except Exception as e:
                    print(e)
                    self.showdialog(e)
                    conn.rollback()
                
                finally:
                    conn.close()
                    
                try:
                    conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                    cr = conn.cursor()
                    cr.execute("Select Count(*) from Data")
                    total = cr.fetchone()
                    # print(total)
                    for a in total:
                        total = a
        
                    self.record.display(total)
                    
                except Exception as e:
                    print(e)
                    print("Error")        

                finally:
                    conn.close()
                    
            else:
                logging.error(f"Invalid input. Only A-Z, a-z, 0-9, and =_#%- are allowed. error occured COMPANY_NAME = {str(company)},ITEM_NAME={str(itemname)},QUANTITY={float(qt)},UOM = {str(uom)},CHALAN_NO={str(challan)},REMARK ={str(remark)} by the {self.empdata[1] } at {datetime.now()} ")
                self.showdialog("Invalid input. Only A-Z, a-z, 0-9, and =_#%- are allowed.")
                              
    def validate_input(self,l1):
    # Define the regex pattern for valid input
        pattern = r'^[a-zA-Z0-9=#%$-.]+$'
        flag = 1  # Initialize flag to 1

        for a in l1:
            # Check if the input matches the pattern
            if not re.match(pattern, a):  # Use "not" to check if it doesn't match
    
                flag = 0  # Set flag to 0 if any item doesn't match the condition
  
        return flag
              
class SignupScreen(QDialog,QtWidgets.QMainWindow):
    
    def __init__(self,uname):

        self.uname = uname
        super(SignupScreen, self).__init__()
        loadUi("new.ui",self)
        self.signup.clicked.connect(self.signupf)
        
        pixmap = QPixmap('logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        
        self.closebtn.clicked.connect(self.loggedout)
        self.back.clicked.connect(lambda: self.backbtn(uname))
        
        
        self.tableViews()
        
        
       
        self.cname.setText("DTPL INWARD SYSTEM")
        
    def tableViews(self):
        try:
            user=[]
            conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
            cr = conn.cursor()
            
            qry = "select USERNAME, FNAME,LNAME,PHONE FROM emplogin"
        
         

            cr.execute(qry)
            csvd = cr.fetchall()
            for d in csvd:
                
                user.append(list(d))
            
            udata = pd.DataFrame(
                user
                , columns = ['USERNAME', 'FNAME', 'LNAME','PHONE'])
            
        
            
            model = TableModel(udata)
            self.usertable.setModel(model)
            
            
            header = self.usertable.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        

        except Exception as e:
            print(e)


            
        finally:
            conn.close()

    
    def backbtn(self,uname):
  
        login = Form(uname)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def loggedout(self):
        
                # Create a QDialog instance
        dialog = QDialog()
        dialog.setWindowTitle("Logout Confirmation")

        # Create layout and widgets for the dialog
        layout = QVBoxLayout()
        message_label = QLabel("Do you want to log out?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        # Add widgets to the layout
        layout.addWidget(message_label)
        layout.addWidget(yes_button)
        layout.addWidget(no_button)

        # Set the layout for the dialog
        dialog.setLayout(layout)

        # Connect button actions (close the dialog)
        yes_button.clicked.connect(dialog.accept)
        no_button.clicked.connect(dialog.reject)

        # Show the login dialog
        # 
        result = dialog.exec_()

        # Handle the result of the dialog (e.g., check if it was accepted)
        if result == QDialog.Accepted:
            
            self.hide()
           
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            logging.info(f"{self.uname}User Logged out Sucessfully at {datetime.now()}")
           
            
        else:
            self.show()

    def signupf(self):
        username = self.uname.text()
        password = self.pwd.text()
        rpass = self.pwd1.text()
        fname = self.fname.text()
        lname = self.lname.text()
        phone = self.phone.text()
        if len(username) == 0  or len(password) == 0 or len(rpass)==0 or len(fname) == 0 or len(lname)==0 or len(phone)==0:
            self.showdialog("All Fields are Mondarory")
        
        elif password == rpass:
             
            try:
                conn = pymysql.connect(host="localhost",user="root", password="D33#p@k119",database='INWARD')
                cr = conn.cursor()
                data =[str(username),str(password),str(fname),str(lname),str(phone)]

                cr.execute(f"INSERT INTO emplogin (USERNAME,PASSWORD,FNAME,LNAME,PHONE) values(%s,%s,%s,%s,%s)",data)
                
                
                self.showdialog("You Have Registred Sucessfully ")
                
                conn.commit()
                logging.info(f"{username} registed sucessfully at {datetime.now()} by the Super User")
                self.tableViews()
            except Exception as e:
                print(e)
                self.showdialog(e)
                conn.rollback()
            
            finally:
                conn.close()

    def showdialog(self,e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Message")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("Message")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok)
        # msg.buttonClicked.connect(msgbtn)
        retval = msg.exec_()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

app = QApplication(sys.argv)
welcome = LoginScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setWindowFlags(widget.windowFlags() | Qt.WindowMaximized)


widget.setWindowTitle(" DTPL INWARD SYSTEM")
widget.showMaximized()


# widget.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5(qt_api='pyqt5', theme='light_fusion'))

app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
    
  