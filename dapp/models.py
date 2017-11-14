from django.db import models
from decimal import Decimal
from django.db.models import Q
from django.core.exceptions import ValidationError
from datetime import datetime
from django import forms
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
### WARNING: modifying any of the fields below may permanently delete database contents



class Oligo(models.Model):
    SENSE = 'sense'
    ANTISENSE = 'antisense'
    SENSER_OR_ANTISENSE_CHOICES = (
        (SENSE, 'sense'),
        (ANTISENSE, 'antisense'),
    )
    YES = 'yes'
    NO = 'no'
    YES_OR_NO_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
    )
    FM = 'fm'
    NO = ''
    FM_CHOICES = (
        (FM, 'fm'),
        (NO, ''),
    )
    
    sense_or_antisense = models.CharField(max_length=12, choices = SENSER_OR_ANTISENSE_CHOICES, default='sense')
    oligo_ID = models.IntegerField(default =99999)
    oligo_ID2 = models.CharField(max_length=30, default='', blank = True)
    lot_number = models.CharField(max_length=30, default='',blank = True)
    oligo_name = models.CharField(max_length=50, default='')
    sequence = models.CharField(max_length=500, default='')
    modified_sequence = models.CharField(max_length=500, default='' )
    gene_name = models.CharField(max_length=10, default='', blank = True)
    extinction_coefficient = models.DecimalField(max_digits=7,decimal_places=2,default=Decimal('0.00'),blank = True,null = True)
    molecular_weight = models.DecimalField(max_digits=7,decimal_places=2,default=Decimal('0.00'),blank = True,null = True)
    location = models.CharField(max_length=500, default='', blank = True)
    comment = models.CharField(max_length=500, default='', blank = True)
    received = models.CharField(('Recieved'),max_length=12, choices = YES_OR_NO_CHOICES, default='no')
    date_added = models.DateField(('Date added to database'),default=datetime.now, blank=True)
    fm = models.CharField(('fm'),max_length=6, choices = FM_CHOICES, default='',blank = True)
    
    def save(self, *args, **kwargs):        
        ## check if OID is in use, if not set in_use to 'yes' if it has been recieved or set in_use to 'ordered' if not
        use = ""
        if self.received == "yes":
            use = "yes"
        else:
            use = "ordered"
        ls = Id_Number.objects.filter(number = self.oligo_ID)
        if len(ls)==0:
            ## if Id_Number database does not contain oligo ID, create Id_Number object (unless it is the default OID 99999)
            if self.oligo_ID == 99999:
                super(Oligo, self).save(*args, **kwargs) # Call the "real" save() method.
                return
            ## set ID_Number in_use to use
            Id_Number(number= self.oligo_ID, in_use = use).save()
        else:
            ## if Id_Number exists, and if in_use is not already set to "yes", set in_use to use
            if ls[0].in_use != 'yes':
                ls[0].setInUse(use) 
        super(Oligo, self).save(*args, **kwargs) # Call the "real" save() method.    

        
    def validate(self, oligo_ID):
    ## Check for Errors (for admin interface only)    
        ## Check that oligo ID entered is valid
        if not isinstance( oligo_ID , int ):
            raise forms.ValidationError("Oligo ID must be an integer")
            return
        errorMessageLs = [] 
        if oligo_ID >29999:
            errorMessageLs.append("Oligo IDs must be below 29999")
        if oligo_ID > 19999:
            if self.sense_or_antisense == 'sense':
                errorMessageLs.append("Sense Oligo ID must be below 19999")
        if oligo_ID < 19999:
            if self.sense_or_antisense == 'antisense':
                errorMessageLs.append("Antisense Oligo ID must be in the range 20000-29999")
        
        ## Check that oligo is unique (IDs)
        idLs = Oligo.objects.all().values_list('oligo_ID', flat=True) 
        id2Ls= Oligo.objects.filter(oligo_ID = self.oligo_ID).values_list('oligo_ID2', flat=True)
        if oligo_ID in idLs:
            if not self in Oligo.objects.filter(oligo_ID = self.oligo_ID): ## Will not raise error if duplicate is the current oligo (if editing rather than creating a new one)
                if (self.oligo_ID2 == ""):
                    errorMessageLs.append("Another Oligo has that ID, please select a different ID or add a unique ID2")
                elif (self.oligo_ID2 in id2Ls): 
                    errorMessageLs.append("Another Oligo has that ID and ID2 combination, please select a different ID and/or ID2")        
        ## If oligo has been received needs a lot number, MW, and EC
        if self.received == "yes":
            if self.lot_number == "":
                errorMessageLs.append("All received oligos must have lot numbers, set to 'n/a' if no lot number")
            if self.extinction_coefficient == None or self.extinction_coefficient == "":
                errorMessageLs.append("All received oligos must have an extinction coefficient")
            if self.molecular_weight == None or self.molecular_weight == "":
                errorMessageLs.append("All received oligos must have a molecular weight")
            else:
                ## Checks that lot number is unique
                lotNLs = Oligo.objects.all().values_list('lot_number', flat=True) 
                if (self.lot_number in lotNLs) and (self.lot_number.lower() != "n/a"): ## Will not raise error if duplicate is the current oligo (if editing rather than creating a new one)
                    if not self in Oligo.objects.filter(lot_number = self.lot_number):
                        errorMessageLs.append("Another Oligo has that lot number, set to 'n/a' if no lot number")     
        ## Raise errors if any
        if len(errorMessageLs) > 0:
            raise forms.ValidationError(errorMessageLs)



    def clean(self):
        self.validate(self.oligo_ID)   
        

            

        
    def __unicode__(self):
        return u'%s %s %s' % (self.oligo_ID," ", self.oligo_ID2)
        
    class Meta:
        verbose_name = "Oligo"
        verbose_name_plural = "Oligos"
    

        
class Duplex(models.Model):
    YES = 'fm'
    NO = ''
    FM_CHOICES = (
        (YES, 'fm'),
        (NO, ''),
    )
    
    duplex_ID = models.IntegerField(default =99999)
    duplex_ID2 = models.CharField(max_length=40, default='',blank = True, null = True)
    duplex_Name = models.CharField(max_length=45, default='',blank = True, null = True)
    ## Sense ID2 & Antisense ID2 are necessary to select correct oligo, but are not stored in database
    sense_ID = models.ForeignKey(
        Oligo,
        on_delete=models.PROTECT,
        limit_choices_to = Q(sense_or_antisense = 'sense', received = 'yes'), 
        blank = True,
        null = True
        )
    antisense_ID = models.ForeignKey(
        Oligo,
        on_delete=models.PROTECT,
        limit_choices_to = Q(sense_or_antisense = 'antisense', received = 'yes'),
        related_name = 'antisense',
        blank = True,
        null = True
        )
    date_prep = models.DateField(('Date duplex was prepared'),default=datetime.now, blank=True)
    targetting_region = models.CharField(max_length=500, default='',blank = True, null = True)
    date_added = models.DateField(('Date added to database'),default=datetime.now, blank=True)
    fm = models.CharField(max_length=12, choices = FM_CHOICES, default='',blank = True)
    targetting_region_80mer = models.CharField(('80mer Targetting Region'), max_length=500, default='',blank = True, null = True)
    
    
    def validate(self, duplex_ID):
    ## Check for Errors (for admin interface only)  
        ## Check that duplex ID entered is valid
        if not isinstance( duplex_ID , int ):
            raise forms.ValidationError("Duplex ID must be an integer")
            return
        errorMessageLs = [] 
        if duplex_ID >49999 or duplex_ID < 30000:
            errorMessageLs.append("Duplex IDs must be between 30000-49999")
        
        ## Check Duplex ID is unique with date prepared
        idLs = Duplex.objects.all().values_list('duplex_ID',flat=True) 
        dateLs = Duplex.objects.all().values_list('date_prep',flat=True) 
        if (duplex_ID in idLs) and (self.date_prep in dateLs):
            if not self in Duplex.objects.filter(duplex_ID = self.duplex_ID,date_prep = self.date_prep): 
            ## Will not raise error if duplicate is the current duplex (if editing rather than creating a new one)
                errorMessageLs.append("Another Duplex has that ID, and date prepared")
                
        ## Check that labelled as fm if 400000
        if (self.duplex_ID > 39999) and (self.fm == ""):
            errorMessageLs.append("Duplex IDs in 40000's indicate fm")
        if (self.duplex_ID < 40000) and (self.fm == "fm"):
            errorMessageLs.append("fm Duplexes must have Duplex IDs in 40000's")
        ## Raise errors if any
        if len(errorMessageLs) > 0:
            raise forms.ValidationError(errorMessageLs)
        
    
        
    def clean(self):
        self.validate(self.duplex_ID) 

    def __unicode__(self):
        return u'%s' % (self.duplex_ID)

    class Meta:
        verbose_name = "Duplex"
        verbose_name_plural = "Duplexes"
        


class Id_Number(models.Model):  
    YES = 'yes'
    NO = 'no'
    ORDERED = 'ordered' # ordered and therefore technically in use, but the Oligo has not been imported to the database yet
    USED_PREV = 'used previously' # no longer in use but was used previously
    YES_OR_NO_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
        (USED_PREV, 'used previously'),
        (ORDERED, 'ordered'),
    )
    
    number = models.IntegerField(default =9999)
    in_use = models.CharField(max_length=50, choices = YES_OR_NO_CHOICES, default='no') 
    opposite = models.IntegerField(('Complementary'),default =19999,blank = True, null = True)    
    
    def validate(self, Id_Number):
        if self.number > 10000:
            raise forms.ValidationError("ERROR TEST")
        return
    
    def setInUse(self, x):
        self.in_use = x
        self.save()
        
        
    def oppInUse(self):
        ls = Id_Number.objects.filter(number = self.opposite)
        if len(ls)>0:
            return ls[0].in_use == "yes"
        else:
            return False
        
    def save(self, *args, **kwargs): 
        # select opposite Id
        n = int(self.number)
        nO1 = n - 10000 # opposite number
        if nO1 < 10000: 
            # corrects for sense/antisense
            nO1 = n + 10000
        # if the opposite Id_Number does not exist, sets opposite to None
        ls = Id_Number.objects.filter(number = nO1)
        if len(ls) == 0:
            nO1 = None
        # if number is above 29999 or below 10000 then the opposite is set to None
        if n < 10000 or n >29999:
            nO1 = None
        self.opposite = nO1
        super(Id_Number, self).save(*args, **kwargs) # Call the "real" save() method. 
        
        
    def __unicode__(self):
        return u'%s' % (self.number)
    class Meta:
        verbose_name = "ID Number"
        verbose_name_plural = "ID Numbers"
        
class Result(models.Model):
    
    duplex = models.ForeignKey(
        Duplex,
        on_delete=models.PROTECT,
        blank = True,
        null = True
        )
    expression_percent = models.DecimalField(('Expression'),max_digits=7,decimal_places=4,default=Decimal('0.0000'),blank = True, null = True)
    std_dev = models.DecimalField(('Stdev'),max_digits=7,decimal_places=4,default=Decimal('0.0000'),blank = True, null = True)
    positive_control_percent =models.DecimalField(('Pos control %'),max_digits=7,decimal_places=4, blank = True,null = True)
    NTC_percent = models.DecimalField(max_digits=7,decimal_places=4,default=Decimal('0.0000'),blank = True, null = True)
    comments = models.CharField(max_length=500, default=' ',blank = True, null = True)
    cell_line = models.CharField(max_length=100, default='',blank = True, null = True)
    screen_type = models.CharField(max_length=100, default='',blank = True, null = True)
    exp_date = models.DateField(('Experiment date'), default = datetime.min, blank=True) 
        
    def __unicode__(self):
        return u'%s' % (self.duplex,)
    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"        


class Duplex_products(models.Model):
    YES = 'yes'
    NO = 'no'
    YES_OR_NO_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
    )

    product_url = models.CharField(max_length=500, default='')
#    title = models.CharField(max_length=100, default='')
    title = models.ForeignKey(
        Duplex,
        on_delete=models.PROTECT,
       # limit_choices_to = Q(sense_or_antisense = 'sense', received = 'yes'),
        blank = True,
        null = True
        )
    description = models.CharField(max_length=5000, default='')
    product_type = models.CharField(max_length=500, default='Physical')
    tags = models.CharField(max_length=5000, default='') ## actually should be a list, i        
    catagories = models.CharField(max_length=500, default='Validated sdRNA')
    visible = models.CharField(('Recieved'),max_length=12, choices = YES_OR_NO_CHOICES,default='no' )
    hosted_image_urls = models.CharField(max_length=5000, default='') ## actually should        
    sku = models.CharField(max_length=50, default='10000A')
    price = models.DecimalField(max_digits=7,decimal_places=2,default=Decimal('0.00'))
    stock = models.CharField(max_length=500, default='Unlimited')
    ## add remaining fields for squarespace import

    def __unicode__(self):
        return u'%s %s %s %s' % (self.title," ", self.product_type, self.price)

    class Meta:
        verbose_name = "Duplex Product"
        verbose_name_plural = "Duplexes Products"














        

        
@receiver(post_delete, sender=Oligo, dispatch_uid='oligo_delete_signal')
# When an Oligo is deleted, corresponding ID_Number in_use field is set from 'yes' to 'used previously'
def set_not_in_use(sender, instance, using, **kwargs):
    n_remaining = len(Oligo.objects.filter(oligo_ID = instance.oligo_ID))
    n = Id_Number.objects.filter(number = instance.oligo_ID)
    if len(n)>0 and n_remaining == 0:
        n[0].setInUse('used previously')    
    return
        
        
        
        
        



    









    
    




