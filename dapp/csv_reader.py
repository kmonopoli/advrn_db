"""
Created on Mon Jun  6 13:42:24 2016

@author: kathryn_monopoli

CSV reader
"""
import csv
import os.path, datetime
import shutil
import time
from easygui import msgbox

class Oligo_Reader:
    fileName = ""
    print_list = []    
    txt_fileName = ""
    
    oligo_id = [] #Oligo ID
    oligo_id2 = [] #Variant Oligo ID
    lot_number = [] #Lot Number
    oligo_name = [] #Oligo Name
    sequence = [] #Sequence
    modified_sequence = [] #Modified Sequence
    gene_name = [] #Gene Name
    ext_coeff = [] #Extinction Coefficient
    mol_wt = [] #Estimated Molecular Weight
    comment = [] #Comment
    sense_antisense = [] #sense or antisense
    fm_ls = []

    def __init__(self, fileName, txt_fileName):
        self.fileName = fileName
        self.txt_fileName = txt_fileName
        if fileName == "received_oligos.csv":
            self.run_importer()
        else:
            self.run()
        self.clean_data()
        self.sense_or_anti()
        self.print_list.append("Number of Oligos to add to database: "+str(len(self.gene_name)))
        self.print_list.append(self.fileName + " parsed")
        self.writeText()
        self.saveBackup()
    
  

    def run(self):
        try:
            i = 0
            with open(self.fileName, 'rU') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel_tab)
                for row in reader:
                    i+=1
                    if i > 1: #row where data starts
                        #each row is a list that contains a single string element
                        curRow = row[0]
                        #need to split this string element up into a list for each column value (separated by ",")
                        rowList = curRow.split(",")
                        i+=1
    
                        #get info for each field
                        if rowList[0] != "": ## If there is no oligo ID is a blank row and won't inlcude it
                            self.oligo_id.append(rowList[0])
                            self.oligo_id2.append(rowList[1])
                            self.lot_number.append(rowList[2])
                            self.oligo_name.append(rowList[3])
                            self.sequence.append(rowList[4])
                            self.modified_sequence.append(rowList[5])
                            self.mol_wt.append(rowList[6])
                            self.ext_coeff.append(rowList[7])
                            self.comment.append(rowList[8])
                            self.gene_name.append(rowList[9])

        except:
            self.alertUser("Error reading csv file. Be sure "+self.fileName +" exists in " + os.getcwd())
            quit()
            
    
    def run_importer(self):
        try:
            i = 0
            with open(self.fileName, 'rU') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel_tab)
                for row in reader:
                    i+=1
                    if i > 1: #row where data starts
                        #each row is a list that contains a single string element
                        curRow = row[0]
                        #need to split this string element up into a list for each column value (separated by ",")
                        rowList = curRow.split(",")
                        i+=1
    
                        #get info for each field
                        if rowList[0] != "": ## If there is no oligo ID is a blank row and won't inlcude it
                            self.oligo_id.append(rowList[0])
                            self.oligo_id2.append(rowList[1])
                            self.lot_number.append(rowList[2])
                            self.mol_wt.append(rowList[3])
                            self.ext_coeff.append(rowList[4])


        except:
            self.alertUser("Error reading csv file. Be sure "+self.fileName +" exists in " + os.getcwd())
            quit()
            
            
    def sense_or_anti(self):
    #Determine if sense or antisense
        self.isCorrectType(self.oligo_id,int,"Oligo_ID")
        for string in self.oligo_id:
            if int(string) < 20000:
                self.sense_antisense.append("sense")
            else:
                self.sense_antisense.append("antisense")
                
    def clean_data(self):
        #checks data is formatted correctly
    
        self.checkBlank(self.oligo_id,"Oligo ID")
        self.checkBlank(self.oligo_name,"Oligo Name")
        self.checkBlank(self.sequence,"Nonmodified Sequence")
        self.checkBlank(self.modified_sequence,"Modified Sequence")
        self.checkBlank(self.sense_antisense,"sense/antisense")
        self.checkBlank(self.gene_name,"Gene Name")
        
        self.isCorrectType(self.oligo_id,int,"Oligo ID")
        self.isCorrectType(self.mol_wt,float,"MW")
        self.isCorrectType(self.ext_coeff,float,"EC")

        self.checkLength(self.oligo_id,"Oligo ID",5)
        self.checkLength(self.oligo_id2,"Oligo ID2", 30)
        self.checkLength(self.lot_number,"Lot #",30)
        self.checkLength(self.oligo_name,"Oligo Name", 50)
        self.checkLength(self.sequence,"Nonmodified Sequence",500)
        self.checkLength(self.modified_sequence,"Modified Sequence",500)
        self.checkDecimalLength(self.mol_wt,"MW")
        self.checkDecimalLength(self.ext_coeff,"EC")
        self.checkLength(self.comment,"Comment",500)
        self.checkLength(self.gene_name,"Gene Name",10)
        
        return
          
    
        
    def checkBlank(self,value_list,name):
        ## checks for blanks in columns that can't be blank (except lot # which is checked later)
        for value in value_list:
            if value == "":            
                msg ="ERROR: a(n) "+ str( name) +" is blank"
                self.print_list.append( msg)
                self.print_list.append("0 Oligos imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def checkLength(self,value_list,name, maxLen):
        for value in value_list:
            if len(value) > maxLen:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too long (max length for this field is "+str(maxLen)+" characters)"
                self.print_list.append( msg)
                self.print_list.append("0 Oligos imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def checkDecimalLength(self,value_list,name):
        maxLen = 7
        max_value = 99999
        for value in value_list:
            if value == "":
                return
            v = value.replace(".","")
            if len(v) > maxLen:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too long (max length for this field is "+str(maxLen)+" characters). NOTE: database stores decimals with only two decimal places."
                self.print_list.append( msg)
                self.print_list.append("0 Oligos imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
            elif float(value) > max_value:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too great (max value for this field is "+str(max_value)+"). NOTE: database stores decimals with only two decimal places."
                self.print_list.append( msg)
                self.print_list.append("0 Oligos imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg )
                quit()
        return
    def isCorrectType(self,value_list,typ,name):
        ## checks datatype (tp) of value_list with name if wrong datatype will exit program and print error to log file        
        typS = ""
        
        if typ == int:
            typS = "integer"
        elif typ == str:
            typS = "string"
        elif typ == float:
            typS = "float"
        for value in value_list:
            if value == "":
                return
            try:
                typ(value)
            except:
                msg ="ERROR: "+ str( name) +": '" + str(value)+ "' is not of type "+str(typS)
                self.print_list.append( msg)
                self.print_list.append("0 Oligos imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def alertUser(self,message):
        msgbox(message)
    
        
        
    def writeText(self):
        writer = Write_TXT(self.txt_fileName)
        writer.write_header()
        writer.write_to_txt_file(self.print_list)

    def saveBackup(self):
        Backup_CSV("oligos",self.fileName)
           
    def check_fm(self,seq):
        fm_comp = "fmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfmfm"
        fm_seq = ""
        ## remove Pm from antisense modified sequences
        if seq[:2] == "Pm":
            seq = seq[2:]
        
        for s in seq:
            if (s == "m") or (s == "f"):
                fm_seq += s 
        fm_comp_short = fm_comp[:len(fm_seq)]
        return fm_comp_short == fm_seq
    
    def makeFMs(self):
        for s in self.modified_sequence:
            if self.check_fm(s):
                self.fm_ls.append("fm")
            else:
                self.fm_ls.append("")
    
    def getFMs(self):
        return self.fm_ls
            
    def getIDs(self):
        return self.oligo_id
    def getLotNums(self):
        return self.lot_number
    def getNames(self):
        return self.oligo_name
    def getModSeqs(self):
        return self.modified_sequence
    def getGenes(self):
        return self.gene_name
    def getNumber(self):
        ## Returns number of Oligos in csv file
        return len(self.oligo_id)
    def getSeqs(self):
        return self.sequence
    def getECs(self):
        return self.ext_coeff
    def getMWs(self):
        return self.mol_wt
    def getID2s(self):
        return self.oligo_id2
    def getComments(self):
        return self.comment
    def getSenseAntiSenses(self):
        return self.sense_antisense

class Duplex_Reader:
    fileName = ""
    print_list = [] 
    errors = 0
    duplex_IDs = []
    duplex_ID2s = []
    duplex_names = []
    sense_IDs = []
    s_lotNs = []
    antisense_IDs = []
    as_lotNs = []
    targetting_regions = []
    dates_prepared = []
    dates_prepared_conv = []
    t80_mer = []

    def __init__(self, fileName):
        self.fileName = fileName
        self.errors = 0
        self.run()
        self.clean_data()
        self.print_list.append("Number of Duplexes to add to database: "+ str(len(self.sense_IDs)))
        if self.errors > 0:
            self.print_list.append( str(self.errors)+" errors detected; all errors must be addressed before importing data")
            self.writeText()
            print str(self.errors)+" errors detected; all errors must be addressed before importing data"
            print "see duplex_import_output.txt for information on these errors"
            quit()
        else:
            self.print_list.append( self.fileName + " parsed")
        self.saveBackup()
        self.writeText()

        
    def run(self):  
        try:
            i = 0
            with open(self.fileName, 'rU') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel_tab)
                for row in reader:
                    i+=1
                    if i > 1: #row where data starts
                        #each row is a list that contains a single string element
                        curRow = row[0]
                        #need to split this string element up into a list for each column value_list (separated by ",")
                        rowList = curRow.split(",")
                        i+=1
    
                        #get info for each field
                        if rowList[0] != "":
                            self.duplex_IDs.append(rowList[0])
                            self.duplex_ID2s.append(rowList[1])
                            self.duplex_names.append(rowList[2])
                            self.sense_IDs.append(rowList[3])
                            self.s_lotNs.append(rowList[4])
                            self.antisense_IDs.append(rowList[5])
                            self.as_lotNs.append(rowList[6])
                            self.targetting_regions.append(rowList[7])
                            self.dates_prepared.append(rowList[8])
                            self.t80_mer.append(rowList[9])
        except:
            self.alertUser("Error reading csv file. Be sure "+self.fileName +" exists in " + os.getcwd())
            quit()
            
        
        
    def clean_data(self):
        #checks data is formatted correctly
    
        self.checkBlank(self.duplex_IDs,"Duplex ID")
        self.checkBlank(self.duplex_ID2s,"Duplex ID2")
        self.checkBlank(self.duplex_names,"Duplex Name")
        self.checkBlank(self.sense_IDs,"Sense ID")
        self.checkBlank(self.s_lotNs,"Sense Lot #")
        self.checkBlank(self.antisense_IDs,"Antisense ID")
        self.checkBlank(self.as_lotNs,"Antisense Lot #")
        self.checkBlank(self.targetting_regions,"20 mer Targetting Region")
        self.checkBlank(self.dates_prepared, "Date prepared")
        self.checkBlank(self.t80_mer, "80 mer Targetting Region")
        
        self.convert_dates()
        
        self.isCorrectType(self.duplex_IDs,int,"Duplex ID")
        self.isCorrectType(self.sense_IDs,int,"Sense ID")
        self.isCorrectType(self.antisense_IDs,int,"Antisense ID")
        
        self.checkLength(self.duplex_IDs,"Duplex ID",5)
        self.checkLength(self.duplex_ID2s,"Duplex ID2",40)
        self.checkLength(self.duplex_names,"Duplex Name",45)
        self.checkLength(self.sense_IDs,"Sense ID",5)
        self.checkLength(self.antisense_IDs,"Antisense ID",5)
        self.checkLength(self.targetting_regions,"20 mer Targetting Region",500)
        self.checkLength(self.t80_mer,"80 mer Targetting Region",400)
        
        return
                
    def checkBlank(self,value_list,name):
        ## checks for blanks in columns that can't be blank (except lot # which is checked later)
        for value in value_list:
            if value == "":            
                msg ="ERROR: a(n) "+ str( name) +" is blank"
                self.print_list.append( msg)
                self.print_list.append("0 Duplexes imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def checkLength(self,value_list,name, maxLen):
        for value in value_list:
            if len(value) > maxLen:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too long (max length for this field is "+str(maxLen)+" characters)"
                self.print_list.append( msg)
                self.print_list.append("0 Duplexes imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def isCorrectType(self,value_list,typ,name):
        ## checks datatype (typ) of value in value_list with name if wrong datatype will exit program and print error to log file        
        typS = ""
        if typ == int:
            typS = "integer"
        elif typ == str:
            typS = "string"
        elif typ == float:
            typS = "float"
        for value in value_list:
            if value == "":
                return
            try:
                typ(value)
            except:
                msg ="ERROR: "+ str( name) +": '" + str(value)+ "' is not of type "+str(typS)
                self.print_list.append( msg)
                self.print_list.append("0 Duplexes imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"." )
                quit()
        return

    def convert_dates(self):
        for date in self.dates_prepared:
            # Converts date in mm.dd.yyyy string format to datetime object
            if len(date) != 10:
                # Checks if date is wrong number of characters  (so 02.22.201565 won't work)
                msg= "Date: '"+ date + "' was not formatted correctly (or is invalid date)"
                self.print_list.append(msg)
                self.print_list.append( "Dates must be formatted in mm.dd.yyyy format")
                self.alertUser( msg)
                self.print_list.append("0 Duplexes imported to the database")
                self.errors +=1
                self.writeText()
                quit()
            else:
                try:
                    m  = date[:2:]
                    d = date[3]+date[4]
                    y = date[6:]
                    self.dates_prepared_conv.append(datetime.date(int(y),int(m),int(d)))
                except:
                    ## alert user and quit if does not work
                    msg= "Date: '"+ date + "' was not formatted correctly (or is invalid date)"
                    self.print_list.append(msg)
                    self.print_list.append( "Dates must be formatted in mm.dd.yyyy format")
                    self.alertUser( msg)
                    self.print_list.append("0 Duplexes imported to the database")
                    self.errors +=1
                    self.writeText()
                    quit()
    def alertUser(self,message):
        msgbox(message)   
                       
    def saveBackup(self):
        Backup_CSV("duplexes",self.fileName) 
    def writeText(self):
        writer = Write_TXT('duplex_import_output.txt')
        writer.write_header()
        writer.write_to_txt_file(self.print_list)
        
    # Get Info
    def get_duplex_IDs(self):
        return self.duplex_IDs
    def get_duplex_ID2s(self):
        return self.duplex_ID2s
    def get_names(self):
        return self.duplex_names
    def get_sense_IDs(self):
        return self.sense_IDs
    def get_s_LotNs(self):
        return self.s_lotNs
    def get_antisense_IDs(self):
        return self.antisense_IDs
    def get_as_LotNs(self):
        return self.as_lotNs
    def get_targetting_regions(self):
        return self.targetting_regions
    def getNumber(self):
        return len(self.sense_IDs)
    def get_dates_prep(self):
        return self.dates_prepared_conv
    def get_80_mer_targ_regs(self):
        return self.t80_mer
    
class Result_Reader:
    fileName = ""
    print_list = []
    errors = 0
    duplex_IDs = []
    dates_prep = []
    expression_percents = []
    std_devs = []
    positive_control_percents = []
    NTC_percents = []
    ExpDates = []
    cell_lines = []
    screen_types = []
    comments = []
    Conv_Exp_Dates=[]
    Conv_Dates_Prep=[]


    def __init__(self, fileName):
        self.fileName = fileName
        self.errors = 0
        self.run()
        self.clean_data()
        self.print_list.append("Number of Results to add to database: "+ str(len(self.duplex_IDs)))

        if self.errors > 0:
            self.print_list.append( str(self.errors)+" errors detected; all errors must be addressed before importing data")
            self.writeText()
            quit()
        self.print_list.append( self.fileName + " parsed")
        self.saveBackup()
        self.writeText()
        
    def run(self):     
        try:
            i = 0
            with open(self.fileName, 'rU') as csvfile:
                reader = csv.reader(csvfile, dialect=csv.excel_tab)
                for row in reader:
                    i+=1
                    if i > 1: #row where data starts
                        #each row is a list that contains a single string element
                        curRow = row[0]
                        #need to split this string element up into a list for each column value (separated by ",")
                        rowList = curRow.split(",")
                        i+=1
    
                        #get info for each field
                        if rowList[0] != "":
                            q = 1
                            self.duplex_IDs.append(rowList[q-1])
                            self.dates_prep.append(rowList[q])
                            self.expression_percents.append(rowList[q+1])
                            self.std_devs.append(rowList[q+2])
                            self.positive_control_percents.append(rowList[q+3])
                            self.NTC_percents.append(rowList[q+4])
                            self.ExpDates.append(rowList[q+5])
                            self.cell_lines.append(rowList[q+6])
                            self.screen_types.append(rowList[q+7])
                            self.comments.append(rowList[q+8])
        except:
            self.alertUser("Error reading csv file. Be sure "+self.fileName +" exists in " + os.getcwd())
            quit()

    def clean_data(self):
        #checks data is formatted correctly
    
        self.checkBlank(self.duplex_IDs,"Duplex ID")
        self.checkBlank(self.dates_prep,"Date prepared")
#        self.checkBlank(self.expression_percents,"Expression %")
#        self.checkBlank(self.NTC_percents,"NTC %")
        self.checkBlank(self.ExpDates,"Experiment Date")
        self.checkBlank(self.cell_lines,"Cell line")
        self.checkBlank(self.screen_types,"Screen Type")
        
        self.convert_dates(self.dates_prep,self.Conv_Dates_Prep)
        self.convert_dates(self.ExpDates,self.Conv_Exp_Dates)
        
        self.isCorrectType(self.duplex_IDs,int,"Duplex ID")
        self.isCorrectType(self.expression_percents,float,"Expression %")
        self.isCorrectType(self.NTC_percents,float,"NTC %")
        self.isCorrectType(self.std_devs,float,"Std dev") ### can be blank need to fix this
        self.isCorrectType(self.positive_control_percents,float,"Positive Control %") ### can be blank need to fix this
        
        self.checkLength(self.duplex_IDs,"Duplex ID",5)
        self.checkDecimalLength(self.expression_percents,"Expression %")
        self.checkDecimalLength(self.std_devs,"Std dev")
        self.checkDecimalLength(self.positive_control_percents,"Positive Control %")
        self.checkDecimalLength(self.NTC_percents,"NTC %")
        self.checkLength(self.cell_lines,"Cell line",100)
        self.checkLength(self.screen_types,"Screen Type",100)
        self.checkLength(self.comments,"Comment",500)
        
        return
                
        
    def checkBlank(self,value_list,name):
        ## checks for blanks in columns that can't be blank (except lot # which is checked later)
        for value in value_list:
            if value == "":            
                msg ="ERROR: a(n) "+ str( name) +" is blank"
                self.print_list.append( msg)
                self.print_list.append("0 Results imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def checkLength(self,value_list,name, maxLen):
        for value in value_list:
            if len(value) > maxLen:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too long (max length for this field is "+str(maxLen)+" characters)"
                self.print_list.append( msg)
                self.print_list.append("0 Results imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return
    def checkDecimalLength(self,value_list,name):
        maxLen = 7
        max_value = 99999
        for value in value_list:
            v = value.replace(".","")
            if v == "":
                return
            if len(v) > maxLen:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too long (max length for this field is "+str(maxLen)+" characters). NOTE: database stores decimals with only four decimal places."
                self.print_list.append( msg)
                self.print_list.append("0 Results imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
            elif float(value) > max_value:
                msg ="ERROR: "+str(name)+ " '" + str(value) + "' is too great (max value for this field is "+str(max_value)+"). NOTE: database stores decimals with only four decimal places."
                self.print_list.append( msg)
                self.print_list.append("0 Results imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg )
                quit()
        return
    def isCorrectType(self,value_list,typ,name):
        ## checks datatype (tp) of value_list with name if wrong datatype will exit program and print error to log file  
        ## ignores blank values
        typS = ""
        if typ == int:
            typS = "integer"
        elif typ == str:
            typS = "string"
        elif typ == float:
            typS = "float"
        for value in value_list:
            if value == "":
                return
            try:
                typ(value)
            except:
                msg ="ERROR: "+ str( name) +": '" + str(value)+ "' is not of type "+str(typS)
                self.print_list.append( msg)
                self.print_list.append("0 Results imported to the database")
                self.writeText()
                self.alertUser("Formatting error. "+ msg +"."  )
                quit()
        return

    def convert_dates(self,ls1,ls2):
        for dt in ls1:
            if len(dt) != 10:
                # Checks date is appropriate length (so 02.22.201567 or 1.2.16 or 04.22.15 won't work)
                msg= "Date: '"+ dt + "' was not formatted correctly (or is invalid date)"
                self.print_list.append(msg)
                self.print_list.append( "Dates must be formatted in mm.dd.yyyy format")
                self.alertUser( msg)
                self.print_list.append("0 Duplexes imported to the database")
                self.errors +=1
                self.writeText()
                quit()
            else:
            # Converts date in mm.dd.yyyy string format to datetime object  
                try:
                    m = int(dt[0]+dt[1])
                    d = int(dt[3]+dt[4])
                    y = int(dt[6]+dt[7]+dt[8]+dt[9])
                    t = datetime.date(y,m,d)
                    ls2.append(t)
                except:
                # If the date is invalid but was the appropriate length (i.e. 02.30.2015) will prompt the user to fix it
                    msg = "WARNING: Date: "+str(dt) + " formatted incorrectly (or is an invalid date). Dates must be formatted in mm.dd.yyyy format"
                    self.print_list.append(msg)
                    self.print_list.append("0 Results imported to the database")
                    self.writeText()
                    self.alertUser(msg)
                    quit()
    def alertUser(self,message):
        msgbox(message)
 


    
    def saveBackup(self):
        Backup_CSV("results",self.fileName) 
    def writeText(self):
        writer = Write_TXT('results_import_output.txt')
        writer.write_header()
        writer.write_to_txt_file(self.print_list)
        
    # Get Info
    def get_duplex_IDs(self):
        return self.duplex_IDs
    def get_expression_percents(self):
        return self.expression_percents
    def get_std_devs(self):
        return self.std_devs
    def get_positive_control_percents(self):
        return self.positive_control_percents
    def get_NTC_percents(self):
        return self.NTC_percents
    def get_comments(self):
        return self.comments
    def get_cell_lines(self):
        return self.cell_lines
    def get_screen_types(self):
        return self.screen_types
    def get_Exp_Dates(self):
        return self.Conv_Exp_Dates
    def get_Dates_Prep(self):
        return self.Conv_Dates_Prep
    def getNumber(self):
        return len(self.duplex_IDs)



class Backup_CSV:
    which_file = ""  # data type (oligos/duplexes/results)
    fileName = ""
    def __init__(self,which, file_name):
        self.which_file = which 
        self.fileName = file_name
        self.make_backup()
        
    def alertUser(self,message):
        msgbox(message)
 
    def make_backup(self):
        ## saves a copy of the csv file to the database_imports/which_file folder
        cd = os.getcwd()
        move_to_dir = cd + "/database_imports/"+self.which_file
        date = self.formatDates(datetime.datetime.now())
        n = 1
        new_name = date + " ("+str(n)+") "+self.fileName
        try:
            shutil.copy2((cd+"/"+self.fileName), move_to_dir)
            os.chdir(move_to_dir)
        except:
            msg = "IMPORT BACKUP ERROR: "+ move_to_dir + " and/or " + cd + "/" + self.fileName + " does not exist. Place the appropriate files/folders in the appropriate locations to ensure imports are backed up."
            self.alertUser(msg)
        while os.listdir(os.getcwd()).__contains__(new_name):
            n +=1
            new_name = date + " ("+str(n)+") "+self.fileName
        try:
            os.rename(self.fileName,new_name)
        except:
           msg = "IMPORT BACKUP ERROR: Cannot rename file to "+new_name+ " possibly because a file already exists with this name in "+str(os.getcwd())
           self.alertUser(msg)
        try:
            os.chdir(cd)
        except:
            msg ="IMPORT BACKUP ERROR: "+ cd + " does not exist. Place the appropriate files/folders in the appropriate locations before importing."
            self.alertUser(msg)
        print "Copy of ",self.fileName," saved to ",move_to_dir
        return
        
    def formatDates(self,date):
        m = str(date.month)
        d = str(date.day)
        y = str(date.year)
        
        if len(m)<2:
            m = "0"+m
        if len(d)<2:
            d = "0"+d
        y = y[2:]
        return m+d+y

class Backup_CSV_Report:
    which_file = ""  # data type (oligos/duplexes/results)
    fileName = ""
    def __init__(self,which, file_name):
        self.which_file = which 
        self.fileName = file_name
        self.make_backup()
        
    def alertUser(self,message):
        msgbox(message)
 
    def make_backup(self):
        ## saves a copy of the csv file to the database_imports/which_file folder
        cd = os.getcwd()
        move_to_dir = cd + "/database_imports/"+self.which_file
        date = self.formatDates(datetime.datetime.now())
        n = 1
        new_name = date + " ("+str(n)+") "+self.fileName
        try:
            shutil.copy2((cd+"/"+self.fileName), move_to_dir)
            os.chdir(move_to_dir)
        except:
            msg = "IMPORT BACKUP ERROR: "+ move_to_dir + " and/or " + cd + "/" + self.fileName + " does not exist. Place the appropriate files/folders in the appropriate locations to ensure imports are backed up."
            self.alertUser(msg)
        while os.listdir(os.getcwd()).__contains__(new_name):
            n +=1
            new_name = date + " ("+str(n)+") "+self.fileName
        try:
            os.rename(self.fileName,new_name)
        except:
           msg = "IMPORT BACKUP ERROR: Cannot rename file to "+new_name+ " possibly because a file already exists with this name in "+str(os.getcwd())
           self.alertUser(msg)
        try:
            os.chdir(cd)
        except:
            msg ="IMPORT BACKUP ERROR: "+ cd + " does not exist. Place the appropriate files/folders in the appropriate locations before importing."
            self.alertUser(msg)
        print "Copy of ",self.fileName," saved to ",move_to_dir
        return
        
    def formatDates(self,date):
        m = str(date.month)
        d = str(date.day)
        y = str(date.year)
        
        if len(m)<2:
            m = "0"+m
        if len(d)<2:
            d = "0"+d
        y = y[2:]
        return m+d+y



class Write_TXT:
    file_name = ""
    working_dir = "" ## Where python script is run (~adv_django/adv_dj_proj/dapp)  (can change this if remove from the constructor)
    log_dir = "" ## Where txt log files are stored (can change this if remove from the constructor)
    def __init__(self,file_name):
        self.file_name = file_name
        self.working_dir = os.getcwd()
        self.log_dir = os.getcwd() + "/database_imports/import_logs"
        
    def write_to_txt_file(self,ls):
        try:
            os.chdir(self.log_dir)
            fo = open(self.file_name, 'a')
            lines_to_add = len(ls)
            ct = 0
            while ct < lines_to_add:
                fo.write(ls[ct])
                fo.write("\n")
                ct+=1
            fo.close()
            os.chdir(self.working_dir)
        except:
            msg = "IMPORT LOG WRITING ERROR: There was a problem writing the "+self.file_name+ " log file. Be sure this file exists in " + self.log_dir 
            self.alertUser(msg)
    def write_header(self):
        try:
            os.chdir(self.log_dir)
            fo = open(self.file_name, 'a')        
            t = time.localtime()
            date = (str(t.tm_mon)+"."+str(t.tm_mday)+"."+str(t.tm_year))+"  "+(str(t.tm_hour-4)+":"+str(t.tm_min)+":"+str(t.tm_sec))
            fo.write("\n")
            fo.write("-------------------------  "+str(date)+"  -------------------------")
            fo.write("\n")
            fo.close()
            os.chdir(self.working_dir)
        except:
            msg = "IMPORT LOG WRITING ERROR: There was a problem writing the "+self.file_name+ " log file. Be sure this file exists in " + self.log_dir 
            self.alertUser(msg)
    def alertUser(self,message):
        msgbox(message)
        
        
        
"""   
        self.checkCommas(self.oligo_id2,"Oligo ID2")
        self.checkCommas(self.lot_number,"Lot #")
        self.checkCommas(self.oligo_name,"Oligo name")
        self.checkCommas(self.sequence,"Sequence")
        self.checkCommas(self.modified_sequence,"Modified sequence")
        self.checkCommas(self.gene_name,"Gene name")
#        self.checkCommas(self.comment,"Comment")
    
        return
                
    def checkCommas(self,value_list,name):
        ## if commas are present, the importer will recognize this as a collumn separation, therefore this method converts all commas to semicolons (;)
        for value in value_list:
            if value.__contains__(","):
                value.replace(",",";")
                self.print_list.append("A comma was replaced with a semicolon for "+name+ " "+value)
        return
        
        
        
        
        self.checkCommas(self.duplex_ID2s,"Duplex ID2")
        self.checkCommas(self.duplex_names,"Duplex name")
        self.checkCommas(self.s_lotNs,"Sense Lot #")
        self.checkCommas(self.targetting_regions,"Targetting regions")

        return
    
   
    def checkCommas(self,value_list,name):
        ## if commas are present, the importer will recognize this as a collumn separation, therefore this method converts all commas to semicolons (;)
        for value in value_list:
            if value.__contains__(","):
                value.replace(",",";")
                self.print_list.append("A comma was replaced with a semicolon for "+name+ " "+value)
        return
        
        
        
        
        
                
        self.checkCommas(self.duplex_IDs,"Duplex ID")
        self.checkCommas(self.cell_lines,"Cell line")
        self.checkCommas(self.screen_types,"Screen type")
        self.checkCommas(self.comments,"Comment")
        
        return
        
    def checkCommas(self,value_list,name):
        ## if commas are present, the importer will recognize this as a collumn separation, therefore this method converts all commas to semicolons (;)
        for value in value_list:
            if value.__contains__(","):
                value.replace(",",";")
                self.print_list.append("A comma was replaced with a semicolon for "+name+ " "+value)
        return
"""
