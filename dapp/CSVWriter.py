"""
Created on Fri Mar 25 12:01:10 2016

@author: kathryn_monopoli

Write to .xls files
"""

import xlwt
import os
import time


class SheetMaker:
    file_name = ""
    column_num = 0
    row_num = 0
    data_list =[]
    working_dir = ""
    oligos = []
    duplexes = []
    results = []
    
    def __init__(self,file_name,data_list,columns,rows):
        self.file_name = file_name 
        self.data_list =data_list
        self.column_num = columns
        self.row_num= rows
        self.working_dir = os.getcwd()

    
        
    def makeFile(self):
        book = xlwt.Workbook(encoding="utf-8")
        sht1 = book.add_sheet(self.file_name.replace(".xls",""))
        self.editSheet(sht1)
        fileName = os.getcwd()+ "/database_exports/" + self.file_name
        print "File Created:", fileName
        os.chdir(os.getcwd().replace("exporter",""))
        book.save(fileName)
    
    def printInfo(self,x,y,rows,columns,tempList,sheet):
        ## Prints data in templist to sheet starting at x,y in table
        ## Iterate through list until max columns then move down a row
        i = 0   
        row = 0
        while i < len(tempList):
            col = 0
            while col < columns:
                try:
                    sheet.write(row+y,col+x,tempList[i])
                    col+=1
                    i+=1
                except:
                    print "Stopped working at i = ", i 

            row+=1
        return
    
    def overwrite(self):
        book = xlwt.Workbook(encoding="utf-8")
        sht1 = book.add_sheet(self.file_name.replace(".xls",""))
        self.editSheet(sht1)
        fileName = os.getcwd() + self.file_name
        print "File Created:", fileName
        book.save(fileName)
        

    
    def editSheet(self,sheet):
        self.printInfo(0,0,self.row_num,self.column_num,self.data_list,sheet)
    

 
    
        
    
        
        
        
    




        
        
        
        
        





