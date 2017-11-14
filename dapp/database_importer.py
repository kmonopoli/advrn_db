from csv_reader import Oligo_Reader,Write_TXT,Duplex_Reader,Result_Reader
from models import Oligo, Duplex, Result
import time
from easygui import ynbox,ccbox,msgbox
from decimal import Decimal
import sys
from CSVWriter import SheetMaker

#os.environ.setdefault("DJANGO_SETTINGS_MODULE","adv_dj_proj.settings")

class Oligo_Data:
    titles = ["OLIGO ID","OLIGO ID2","LOT #", "OLIGO NAME","NON MODIFIED SEQUENCE","MODIFIED SEQUENCE" ,"ESTIMATED MW (G/MOL)","EXTINCTION COEF. (UNITS/UMOL)","COMMENT","GENE NAME"]
    total_objects   = 0  # number of  objects initially based on how many are in csv file
    objects_added = 0 # number of objects added to database
    print_list = [] ## list to be printed to output file
    all_received = "" # yes or no
    errors = 0
    
    def __init__(self):
        self.errors = 0
    
    def prep(self):
        return
        
    def run(self):
        file1 = Oligo_Reader('oligo_migration_to_database.csv','oligo_import_output.txt') # csv file with object data
        file1.makeFMs()
        self.total_objects = file1.getNumber() #get number of objects to import
        txt_writer = Write_TXT("oligo_import_output.txt")
        #txt_writer.write_header()
        self.user_input()
        start = time.time()
        self.print_list.append( "")
        self.print_list.append( "")
        self.print_list.append( "Saving "+ str(self.total_objects)+ " Oligos to database...")
        self.varify_objects(file1)
        self.print_list.append(str( self.errors)+ " errors detected")
        self.print_list.append( "Process took "+str(time.time()-start)+" seconds")
        txt_writer.write_to_txt_file(self.print_list)
        if self.errors >0:
            msgbox("Process complete "+ str(self.errors)+" error(s) occured see oligo_import_output.txt for more information")
        print "Process complete"
        print "Check /adv_django/adv_dj_proj/database_imports/import_logs/oligo_import_output.txt for info regarding import"
        
        
    def run_received(self):
        #to import data for received oligos
        file1 = Oligo_Reader('received_oligos.csv','oligo_received_import_output.txt') # csv file with object data
        self.total_objects = file1.getNumber() #get number of objects to import
        txt_writer = Write_TXT("oligo_received_import_output.txt")
        self.all_received = "yes"
        start = time.time()
        self.print_list.append( "")
        self.print_list.append( "")
        self.print_list.append( "Updating "+ str(self.total_objects)+ " Oligos in database...")
        ## make changes below        
        
        self.varify_objects_rec(file1)
        
        self.print_list.append(str( self.errors)+ " errors detected")
        self.print_list.append( "Process took "+str(time.time()-start)+" seconds")
        txt_writer.write_to_txt_file(self.print_list)
        if self.errors >0:
            msgbox("Process complete "+ str(self.errors)+" error(s) occured see oligo_received_import_output.txt for more information")
        print "Process complete"
        print "Check /adv_django/adv_dj_proj/database_imports/import_logs/oligo_received_import_output.txt for info regarding import"
        


    def overWrite(self):
        writer = SheetMaker('oligo_migration_to_database_new.csv',self.titles,len(self.titles),1)
        writer.overwrite()
        
    def checkIfDuplicateIDs(self,oID,oID2):   
    ##Returns TRUE if there is already an oligo with the same ID and ID2 
        idLs = Oligo.objects.all().values_list('oligo_ID', flat=True) 
        if int(oID) in idLs:
            id2Ls= Oligo.objects.filter(oligo_ID = oID).values_list('oligo_ID2', flat=True)        
            if oID2 in id2Ls:
                return True
            else:
                return False
        else:
            return False
        
    
    def checkIfDuplicateLotN(self,lotN):
    ## Returns TRUE if there is already an oligo with the same Lot Number
    ## setting lot Number to 'n/a' in csv file overrides this method causing it to always return FALSE
    ## if all received = "no" then will return FALSE
        if self.all_received == "no":
            return False
        lotNLs = Oligo.objects.all().values_list('lot_number', flat=True) 
        lotNLs=[ln.lower() for ln in lotNLs]
        if (lotN.lower() in lotNLs) and (lotN.lower() != "n/a") :
            return True
        return False

    def user_input(self):
       # Shows yes/no dialogue box asking if oligos being import have been received
        msg = "Have all the oligos being imported been received?"
        title = "Please Confirm"
        if ynbox(msg, title):
            self.all_received = "yes"
            self.print_list.append( 'All imported Oligos received set to "yes"')
        else: 
            self.all_received = "no"            

    def varify_objects_rec(self,file1):
        # Calls update_object for all object data obtained from csv file that is varified
        index = 0
        while(self.total_objects > 0):
            oID = file1.getIDs()[index]
            oID2 = file1.getID2s()[index]
            lotN = file1.getLotNums()[index]
            mw = file1.getMWs()[index]
            ec = file1.getECs()[index]
            if oID == "": ## if oligo ID is blank, is a blank row and won't include it
                pass
            ## Check for blanks
            elif self.checkBlank(lotN,"Lot Number",oID):
                pass
            elif self.checkBlank(mw,"Estimated MW",oID):
                pass
            elif self.checkBlank(ec,"EC",oID):
                pass
            ## Check that oligo exists in database
            elif not self.checkIfDuplicateIDs(oID,oID2):
                self.print_list.append( "An Oligo with ID (" + str(oID) + "), and ID2 (" + str(oID2) + ") has not been imported to the database.")
                self.errors+=1
            ## check if lot number already exists in databse
            elif self.checkIfDuplicateLotN(lotN):
                self.print_list.append( "An Oligo with Lot # (" + str(lotN) + ") already exists in the database.")
                self.errors+=1
            else:
                self.update_object(file1,index)  
            index+=1
            self.total_objects -=1
        self.print_list.append("")
        self.print_list.append("PROCESS COMPLETE: "+str(self.objects_added)+" Oligos updated in the database")

        
    def checkBlank(self,n,name,oID):
        # Returns True if n is blank
        if n =="":
            ## alert user
            self.print_list.append("The "+name+" for Oligo "+str(oID)+" is blank")
            self.errors+=1
            return True
        else:
            return False
        
    def varify_objects(self,file1):
        # Calls make_object for all object data obtained from csv file that is varified
        index = 0
        while(self.total_objects > 0):
            oID = file1.getIDs()[index]
            oID2 = file1.getID2s()[index]
            lotN = file1.getLotNums()[index]
            if oID == "": ## if oligo ID is blank, is a blank row and won't include it
                pass
            elif self.checkIfDuplicateIDs(oID,oID2):
                self.print_list.append( "An Oligo with ID (" + str(oID) + "), and ID2 (" + str(oID2) + ") already exists in the database.")
                self.errors+=1
            elif self.checkIfDuplicateLotN(lotN):
                self.print_list.append( "An Oligo with Lot # (" + str(lotN) + ") already exists in the database.")
                self.errors+=1
            else:
                self.make_object(file1,index)
                
            index+=1
            self.total_objects -=1
        self.print_list.append("")
        self.print_list.append("PROCESS COMPLETE: "+str(self.objects_added)+" Oligos imported to the database")

        
    def get_EC(self,file1,index):
        ec = file1.getECs()[index]
        if ec == "":
            return None
        else:
            return ec
    
    def get_MW(self,file1,index):
        mw = file1.getMWs()[index]
        if mw == "":
            return None
        else:
            return mw
        
    def get_oligo(self,oID,oID2):   
    # Returns Oligo with oligo Ids
        idLs = Oligo.objects.all().values_list('oligo_ID', flat=True) 
        if int(oID) in idLs:
            id2Ls= Oligo.objects.filter(oligo_ID = oID, oligo_ID2 = oID2) #.values_list('oligo_ID2', flat=True) 
            if len(id2Ls) != 1:
                # error oID2 not found OR more than one
                self.print_list.append( str(len(id2Ls))+ " Oligos with the ID ("+str(oID) +") , and ID2 ("+ str(oID2)+")")
                self.errors+=1
            else:
                return id2Ls[0]
        else:
            # error oID not found
            self.print_list.append( " Oligo with the ID ("+ str(oID) + ") was not found")
            self.errors+=1
                
        
    def update_object(self,file1,index):
        # update received Oligos
        oligo2 = self.get_oligo(file1.getIDs()[index],file1.getID2s()[index])
        ## Checks if oligo is already received
        if oligo2.received == "yes":
            self.print_list.append("Oligo with ID ("+str(oligo2.oligo_ID)+") has already been received.")
            self.errors+=1
            return
        oligo2.lot_number = file1.getLotNums()[index]
        oligo2.extinction_coefficient = self.get_EC(file1,index)#file1.getECs()[index]
        oligo2.molecular_weight = self.get_MW(file1,index)#file1.getMWs()[index]
        oligo2.received = self.all_received
        oligo2.save()
        self.objects_added +=1
        return

    def make_object(self,file1,index):
        # make Oligo object
        oligo1 = Oligo.objects.create() #generate empty Oligo and save to database
        #add information about each oligo
        oligo1.oligo_ID = file1.getIDs()[index]
        oligo1.oligo_ID2 = file1.getID2s()[index]
        oligo1.oligo_name =file1.getNames()[index] 
        oligo1.lot_number = file1.getLotNums()[index]
        oligo1.sequence =file1.getSeqs()[index] 
        oligo1.modified_sequence = file1.getModSeqs()[index]
        oligo1.gene_name = file1.getGenes()[index]
        
        oligo1.extinction_coefficient = self.get_EC(file1,index)#file1.getECs()[index]
        oligo1.molecular_weight = self.get_MW(file1,index)#file1.getMWs()[index]
        
        oligo1.comment = file1.getComments()[index]
        oligo1.sense_or_antisense = file1.getSenseAntiSenses()[index]
        oligo1.received = self.all_received
        
        oligo1.fm = file1.getFMs()[index]        
        
        oligo1.save()
        self.objects_added +=1
        
    
        
    

class Duplex_Data:
    total_objects   = 0  # number of  objects initially based on how many are in csv file
    objects_added = 0 # number of objects added to database
    print_list = [] ## list to be printed to output file
    errors = 0
    sense_IDs = []
    antisense_IDs = []
    sense_Lots = []
    antisense_Lots = []
    dates = []
    duplex_IDs = []
    
    
    def __init__(self):
        self.errors = 0
        
    def run(self):
        file1 = Duplex_Reader('duplexes_to_add_to_db.csv')
        self.total_objects = file1.getNumber() #get number of objects to import
        txt_writer = Write_TXT("duplex_import_output.txt")
        #txt_writer.write_header()
        self.print_list.append( "")
        self.print_list.append( "")
        self.print_list.append( "Saving "+ str(self.total_objects)+ " Duplexes to database...")
        self.varify_objects(file1)
        self.print_list.append(str( self.errors)+ " errors detected")
        txt_writer.write_to_txt_file(self.print_list)
        if self.errors >0:
            msgbox("Process complete "+ str(self.errors)+" error(s) occured see duplex_import_output.txt for more information")
        print "Process complete"
        print "Check /adv_django/adv_dj_proj/database_imports/import_logs/duplex_import_output.txt for info regarding import"

    

    def get_info(self,file1):
        self.sense_IDs = file1.get_sense_IDs()
        self.sense_Lots = file1.get_s_LotNs()
        self.antisense_IDs = file1.get_antisense_IDs()
        self.antisense_Lots = file1.get_as_LotNs()
        self.duplex_IDs = file1.get_duplex_IDs()
        self.dates = file1.get_dates_prep()
    
    def varify_objects(self,file1):
        # Calls make_object for all object data obtained from csv file that is varified
        self.get_info(file1)
        
        index = 0
        while(self.total_objects > 0):
            duplex_ID = self.duplex_IDs[index]            
            dt = self.dates[index]
            sLN = self.sense_Lots[index]
            asLN = self.antisense_Lots[index]
            sID = self.sense_IDs[index]
            asID = self.antisense_IDs[index]
            if sID == "": 
                # If there is no sense ID, is a blank row and won't include it
                pass
            elif len(Duplex.objects.filter(sense_ID__lot_number = sLN,antisense_ID__lot_number = asLN,date_prep = dt))> 0:
                # If there is already duplex made with same oligos AND same date prepared is a duplicate and won't include
                self.print_list.append("Duplex "+str(duplex_ID)+" made of Oligos with lot #'s "+str(sLN)+" & "+str(asLN)+" and date prepared "+str(dt.month)+"."+str(dt.day)+"."+str(dt.year)+" already exists.")
                self.print_list.append( "Duplex with ID ("+str(duplex_ID)+") was not imported")                 
                self.errors+= 1   
            elif (self.validateOligoIDs(sID,sLN)) and (self.validateOligoIDs(asID,asLN)): 
                # Check that oligos are in database and are not duplicated (based on lot #s and IDs)
                self.make_object(file1,index)
            else:
                self.print_list.append( "Duplex with ID ("+str(duplex_ID)+") was not imported") 
                self.errors+=1
            index+=1
            self.total_objects -=1
        self.print_list.append("")
        self.print_list.append("PROCESS COMPLETE: "+str(self.objects_added)+" Duplexes imported to the database")


    def validateOligoIDs(self, ID,lotN):
        # If oligo exists in database (and only one oligo has the Lot # and ID) returns True if not returns False
        oligos = Oligo.objects.filter(oligo_ID = ID,lot_number = lotN)
        if len(oligos)==1:
            return True
        elif len(oligos)>1:
            # Oligo does not exist in database
            self.print_list.append( "WARNING: More than one oligo has the ID ("+str(ID)+") and lot # ("+str(lotN)+").")
            return False
        else:
            # More than one oligo with Lot  and Oligo ID
            self.print_list.append( "Oligo with ID ("+str(ID)+ ") and lot # ("+str(lotN)+") has not been imported to the database.")
            return False
    
    def getOligoObject(self,ID,lotN):
        oligos = Oligo.objects.filter(oligo_ID = ID,lot_number = lotN)
        return oligos[0]
    
    def getFm(self,d_id):
        if d_id > 39999:
            return "fm"
        else:
            return ""
    
    def make_object(self,file1,index):
        #generate empty Duplex and save to database
        duplex1 = Duplex.objects.create()
        #add information about each Duplex
        d_id = int(self.duplex_IDs[index])
        duplex1.duplex_ID = self.duplex_IDs[index]
        duplex1.duplex_ID2 = file1.get_duplex_ID2s()[index]
        duplex1.duplex_Name = file1.get_names()[index] 
        duplex1.sense_ID = self.getOligoObject(self.sense_IDs[index],self.sense_Lots[index])
        duplex1.antisense_ID =self.getOligoObject(self.antisense_IDs[index],self.antisense_Lots[index])
        duplex1.targetting_region = file1.get_targetting_regions()[index]
        duplex1.date_prep = self.dates[index]
        duplex1.fm = self.getFm(d_id)
        duplex1.targetting_region_80mer = file1.get_80_mer_targ_regs()[index]
        duplex1.save()   
        self.objects_added +=1
        
        
    

        


class Result_Data:
    total_objects   = 0  # number of  objects initially based on how many are in csv file
    objects_added = 0 # number of objects added to database
    print_list = [] ## list to be printed to output file
    all_received = "" # yes or no
    errors = 0
    dates = []
    duplex_ids = []

    def __init__(self):
        self.errors = 0
        
    def run(self):
#        self.prompt_User()
        file1 = Result_Reader('results_to_add_to_db.csv')
        self.total_objects = file1.getNumber() #get number of objects to import
        txt_writer = Write_TXT("results_import_output.txt")
        #txt_writer.write_header()
        self.print_list.append( "")
        self.print_list.append("WARNING: This script does not check for duplicate Results")
        self.print_list.append( "")
        self.print_list.append( "Saving "+ str(self.total_objects)+ " Results to database...")
        self.varify_objects(file1)
        self.print_list.append(str( self.errors)+ " errors detected")
        txt_writer.write_to_txt_file(self.print_list)
        if self.errors >0:
            msgbox("Process complete "+ str(self.errors)+" error(s) occured see results_import_output.txt for more information")
        print "Process complete"
        print "Check adv_django/adv_dj_proj/database_imports/import_logs/results_import_output.txt for info regarding import"
#        quit()
        
    def prompt_User(self):
        msg = "WARNING: This importer does not check for duplicate Results. Do you want to continue?"
        title = "Please Confirm"
        if ccbox(msg, title):     # show a Continue/Cancel dialog
            pass  # user chose Continue
        else:  # user chose Cancel
		sys.exit(0)  
  
    def getDuplexObject(self,ID1,date):
        o = Duplex.objects.filter(duplex_ID = ID1,date_prep = date)
        if len(o) == 1:
            return o[0] 
        elif len(o) == 0:
            self.print_list.append( "There is no duplex with the ID ("+str(ID1)+") and date prepared "+str(date)+" in database.")
            self.errors +=1
            return False
        else:
            self.print_list.append("WARNING: More than one duplex has the ID ("+str(ID1)+ ") and date prepared "+str(date)+". This Result must be added to the database manually.") 
            self.errors +=1            
            return False
        
    def varify_objects(self,file1):
        # Calls make_object for all object data obtained from csv file that is varified
        index = 0
        self.dates = file1.get_Dates_Prep()
        self.duplex_ids = file1.get_duplex_IDs()
        while(self.total_objects > 0):
            duplex_id =self.duplex_ids[index]
            date = self.dates[index]
            if duplex_id =="":
            # If there is no Duplex ID, is a blank row and won't include it
                pass
            elif self.getDuplexObject(duplex_id,date) != False:
            # If there are no duplexes with this ID won't include it
                self.make_object(file1,index)
            else:
                self.print_list.append("Result: " + str(duplex_id)+" was not imported" )
                
            index+=1
            self.total_objects -=1
        self.print_list.append("")
        self.print_list.append("PROCESS COMPLETE: "+str(self.objects_added)+" Results imported to the database")

    def get_expression_percent(self,file1,index):
        n= file1.get_expression_percents()[index]
        if n == '':
            return
        else:
            return Decimal(n)
    
    def get_std_dev(self,file1,index):
        n = file1.get_std_devs()[index]
        if n == '':
            return
        else:
            return Decimal(n)
    
    def get_positive_control_percent(self,file1,index):
        n= file1.get_positive_control_percents()[index]
        if n == '':
            return
        else:
            return Decimal(n)
    
    def get_NTC_percent(self,file1,index):
        n = file1.get_NTC_percents()[index]
        if n == '':
            return
        else:
            return Decimal(n)
            
    def make_object(self,file1,index):
        #generate empty Result and save to database
        r = Result.objects.create()
        #add information about each Result
        r.duplex = self.getDuplexObject(self.duplex_ids[index],self.dates[index])
        r.duplex_ID=file1.get_duplex_IDs()[index]
        r.expression_percent = self.get_expression_percent(file1,index)
        r.std_dev = self.get_std_dev(file1,index)
        r.positive_control_percent = self.get_positive_control_percent(file1,index)
        r.NTC_percent = self.get_NTC_percent(file1,index)
        r.comments = file1.get_comments()[index]
        r.cell_line = file1.get_cell_lines()[index]
        r.screen_type = file1.get_screen_types()[index]
        r.exp_date= file1.get_Exp_Dates()[index]
        r.save()
        self.objects_added +=1











