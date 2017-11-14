from models import Id_Number
from models import Oligo


#generate list of numbers to add to database
totalOligIDs = range(25002,29999)#range(10001,19999) + range(20001,29999)




allOligoIDsToSave = 0

    
        
print "Saving ", len(totalOligIDs), " Id_Number's to database..."
print "This may take a few minutes"


#generate Id_Number objects and save to the database
n = len(totalOligIDs)
i = 0
total = n
while(n > 0):    
    o1 = totalOligIDs[i]
    #check if Id_Number already exists in database (based on number)
    if len(Id_Number.objects.filter(number = o1))>0:
       print "Id_Number ", o1," already exists." 
   
    else:
        #generate empty Id_Number and save to database
        id_num = Id_Number.objects.create()
        #add information about Id_Number
        id_num.number = o1
        # add opposite cnumber
        if o1 <20000:
            id_num.opposite = o1 +10000
        else:
            id_num.opposite = o1 - 10000
        #check if oligo is in use
        if len(Oligo.objects.filter(oligo_ID = o1)) > 0:
            id_num.in_use = 'yes'
        
        id_num.save()
        allOligoIDsToSave += 1
        
    if i % 500 == 0:
        #print n
        print str((float(i)/float(total))*100)[:4],"% complete"
        
    i += 1
    n = n-1
        

print "PROCESS COMPLETE: ", allOligoIDsToSave, " Id_Numbers saved to the database"


quit()
