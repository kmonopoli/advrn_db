from csv_reader import Oligo_Reader,Write_TXT,Duplex_Reader,Result_Reader
from models import Oligo, Duplex, Result
import time
from easygui import ynbox,ccbox,msgbox
from decimal import Decimal
import sys
from CSVWriter import SheetMaker

from models import Oligo, Duplex, Result, Duplex_products
from decimal import Decimal
import sys

#os.environ.setdefault("DJANGO_SETTINGS_MODULE","adv_dj_proj.settings")
   
class Product_Data:
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
        file1 = Result_Reader('product_import.csv')
        self.total_objects = file1.getNumber() #get number of objects to import
        txt_writer = Write_TXT("products_import_output.txt")
        #txt_writer.write_header()
        self.print_list.append( "")
        self.print_list.append("WARNING: This script does not check for duplicate Products")
        self.print_list.append( "")
        self.print_list.append( "Saving "+ str(self.total_objects)+ " Products to database...
        self.varify_objects(file1)
        self.print_list.append(str( self.errors)+ " errors detected")
        txt_writer.write_to_txt_file(self.print_list)
        if self.errors >0:
            msgbox("Process complete "+ str(self.errors)+" error(s) occured see results_impo
        print "Process complete"
        print "Check adv_django/adv_dj_proj/database_imports/import_logs/results_import_outp
#        quit() 

def make_duplex_product(dp):
	r = Duplex_products.objects.create()
	r.title = dp
	r.save()


o = Duplex.objects.all()
o = o[:10]
print len(o)

for x in o:
	make_duplex_product(x)




