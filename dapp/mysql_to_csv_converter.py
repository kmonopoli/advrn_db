#!//anaconda/bin/python

from dapp.models import Oligo
from dapp.models import Duplex
from dapp.models import Result
from CSVWriter import SheetMaker
import time

## adv_django/adv_dj_proj/database_exports/database_exporter
## import database_exports.mysql_to_csv_converter import Oligo_Backup
#from database_exports.mysql_to_csv_converter import Oligo_Backup
#from database_exports.database_exporter.mysql_to_csv_converter import Oligo_Backup

class Oligo_Backup:
    oligos = set(Oligo.objects.all())
    oligo_info = ["Oligo ID","Oligo ID2","Lot Number","Sense or Antisense","Oligo Name", "Sequence", "Modified Sequence","Gene Name", "Extinction Coefficient","Molecular Weight","Location","Comment","Received","Date Added to Database","FM"]
    n = len(oligo_info)
    def run(self):
        self.get_info()
        self.write_info()
        
    def get_info(self):
        for o in self.oligos:
            self.oligo_info.append(str(o.oligo_ID))
            self.oligo_info.append(str(o.oligo_ID2))
            self.oligo_info.append(str(o.lot_number))
            self.oligo_info.append(str(o.sense_or_antisense))
            self.oligo_info.append(str(o.oligo_name))
            self.oligo_info.append(str(o.sequence))
            self.oligo_info.append(str(o.modified_sequence))
            self.oligo_info.append(str(o.gene_name))
            self.oligo_info.append(str(o.extinction_coefficient))
            self.oligo_info.append(str(o.molecular_weight))
            self.oligo_info.append(str(o.location))
            self.oligo_info.append(str(o.comment))
            self.oligo_info.append(str(o.received))
            self.oligo_info.append(str(o.date_added))
            self.oligo_info.append(str(o.fm))
    def write_info(self):
        file_name="oligos_db_export.xls"#"oligos_"+self.date()+".xls"
        data_list=self.oligo_info
        columns=self.n
        rows = int(len(self.oligo_info)/columns)
        SheetMaker(file_name,data_list,columns,rows).makeFile()
        
    def date(self):
        d = time.localtime()
        return str(d.tm_mon)+"."+str(d.tm_mday)+"."+str(d.tm_year)
        
class Duplex_Backup:
    duplexes = set(Duplex.objects.all())
    duplex_info = ["Duplex ID",
	"Duplex ID2",
	"Duplex Name",
	"Sense ID",
#	"Sense ID2",
	"Sense Lot #", 
	"Antisense ID", 
#	"Antisense ID2",
	"Antisense Lot #", 
	"Date Prepared", 
	"Targetting Region",
	"Date Added",
	"FM",
	"80 mer Targetting Region"]
    n = len(duplex_info)  
    def run(self):
        self.get_info()
        self.write_info()
    def get_info(self):
        for o in self.duplexes:
            self.duplex_info.append(str(o.duplex_ID))
            self.duplex_info.append(str(o.duplex_ID2))
            self.duplex_info.append(str(o.duplex_Name))
            self.duplex_info.append(str(o.sense_ID.oligo_ID))
#	    self.duplex_info.append(str(o.sense_ID.oligo_ID2))
	    self.duplex_info.append(str(o.sense_ID.lot_number))
            self.duplex_info.append(str(o.antisense_ID.oligo_ID))
#            self.duplex_info.append(str(o.antisense_ID.oligo_ID2))
	    self.duplex_info.append(str(o.antisense_ID.lot_number))
            self.duplex_info.append(str(o.date_prep))
            self.duplex_info.append(str(o.targetting_region))
            self.duplex_info.append(str(o.date_added))
            self.duplex_info.append(str(o.fm))
            self.duplex_info.append(str(o.targetting_region_80mer))

    def write_info(self):
        file_name="duplexes_db_export.xls"#"duplexes_"+self.date()+".xls"
        data_list=self.duplex_info
        columns=self.n
        rows = int(len(self.duplex_info)/columns)
        SheetMaker(file_name,data_list,columns,rows).makeFile()
    
    def date(self):
        d = time.localtime()
        return str(d.tm_mon)+"."+str(d.tm_mday)+"."+str(d.tm_year)

class Results_Backup:
    results = set(Result.objects.all())
    results_info = ["Duplex ID","Date Prepared","Expression %","Std Dev","Positive Control %","NTC %", "Comments", "Cell Line", "Screen Type","Experiment Date"]
    n = len(results_info)  
    def run(self):
        self.get_info()
        self.write_info()
    def get_info(self):
        for o in self.results:
            self.results_info.append(str(o.duplex.duplex_ID))
	    self.results_info.append(str(o.duplex.date_prep))
            self.results_info.append(str(o.expression_percent))
            self.results_info.append(str(o.std_dev))
            self.results_info.append(str(o.positive_control_percent))
            self.results_info.append(str(o.NTC_percent))
            self.results_info.append(str(o.comments))
            self.results_info.append(str(o.cell_line))
            self.results_info.append(str(o.screen_type))
            self.results_info.append(str(o.exp_date))
  
    def write_info(self):
        file_name="results_db_export.xls"#"results_"+self.date()+".xls"
        data_list=self.results_info
        columns=self.n
        rows = int(len(self.results_info)/columns)
        SheetMaker(file_name,data_list,columns,rows).makeFile()
    
    def date(self):
        d = time.localtime()
        return str(d.tm_mon)+"."+str(d.tm_mday)+"."+str(d.tm_year)
    

o = Oligo_Backup()
o.run()
d = Duplex_Backup()
d.run()
r = Results_Backup()
r.run()
quit()

