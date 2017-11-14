from django.contrib import admin
from django.db.models import Q
from dapp.models import Oligo, Duplex, Result, Id_Number, Duplex_products
from django.forms import TextInput, Textarea
from django.db import models
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

superUserList = ['usr4']



##Register your models here.


admin.site.register(Duplex_products)#, OligoAdmin)

def set_received(modelAdmin, request,queryset):
    queryset.update(received = 'yes')
set_received.short_description = "Mark selected oligos as received"


    
class FMFilter(admin.SimpleListFilter):
    title = _('fm')
    parameter_name = 'oligo_ID2'
    
    def lookups(self,request,model_admin):
        return(
            ('0',_('fm')),
            ('1',_('not fm')),
        )
    def queryset(self, request, queryset):
        if self.value() == '0':
            q = queryset.filter(fm = "fm")
            return q
        if self.value() == '1':
            q = queryset.filter(fm = "")
            return q
            






class OligoAdmin(admin.ModelAdmin):
    search_fields = [
    # what can be search by the searchbar
    'sense_or_antisense', 
    'oligo_ID', 
    'oligo_ID2', 
    'lot_number', 
    'oligo_name', 
    'sequence', 
    'modified_sequence', 
    'gene_name', 
    'extinction_coefficient', 
    'molecular_weight', 
    'location', 
    'comment', 
    'date_added',
    'received',
    'fm',
    ]
    list_display = (
    # what shows up in the table
    'oligo_ID',
    'oligo_ID2',
    'lot_number',
    'gene_name',
    'oligo_name', 
    'modified_sequence', 
    'sequence', 
    'extinction_coefficient', 
    'molecular_weight', 
    'received',
    'date_added',
    'fm', 
    )  
    list_filter = (
    #Filters on the right side of the window
    'sense_or_antisense',
    'received',
    FMFilter,  
    'gene_name',  
    'date_added',
    )
    actions = [set_received]
    ##Make date/time field readonly    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('date_added',)
        return self.readonly_fields
    
    ##Disable delete selected oligos for any users but the superuser(s) listed
    def get_actions(self, request):
        actions = super(OligoAdmin, self).get_actions(request)
        if request.user.username in superUserList:
            return actions
        else:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions
   
    ##Disable delete specific oligo for any users but the superuser(s) listed
    def has_delete_permission(self, request, obj=None):
        if request.user.username in superUserList:
            return True
        else:
            return False
            
    

    
admin.site.register(Oligo, OligoAdmin)



class DuplexAdmin(admin.ModelAdmin):
    search_fields = [
    'duplex_ID',
    'duplex_ID2',
    'duplex_Name',
    'sense_ID__oligo_name',
    'antisense_ID__oligo_name',
    'sense_ID__oligo_ID', 
    'sense_ID__oligo_ID2', 
    'sense_ID__lot_number', 
    'sense_ID__oligo_name', 
    'sense_ID__sequence', 
    'sense_ID__modified_sequence', 
    'sense_ID__gene_name', 
    'sense_ID__extinction_coefficient', 
    'sense_ID__molecular_weight', 
    'sense_ID__location', 
    'sense_ID__comment', 
    'sense_ID__date_added',
    'antisense_ID__oligo_ID', 
    'antisense_ID__oligo_ID2', 
    'antisense_ID__lot_number', 
    'antisense_ID__oligo_name', 
    'antisense_ID__sequence', 
    'antisense_ID__modified_sequence', 
    'antisense_ID__gene_name', 
    'antisense_ID__extinction_coefficient', 
    'antisense_ID__molecular_weight', 
    'antisense_ID__location', 
    'antisense_ID__comment', 
    'antisense_ID__date_added',
    'date_prep',
    'targetting_region',
    'date_added',
    'targetting_region_80mer',
    ]
    list_display = (
    'duplex_ID',
    'duplex_ID2',  
    'duplex_Name',  
    'sense_ID',
    'antisense_ID',
    'date_prep',
    'targetting_region',  
    'date_added',
    'fm', 

    )
    list_filter = (
    'fm', 
    'date_added',
    'sense_ID__gene_name'  
    )    
    
    #Make date/time field readonly    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('date_added',)
        return self.readonly_fields

    ##Disable delete selected duplexes for any users but the superuser(s) listed
    def get_actions(self, request):
        actions = super(DuplexAdmin, self).get_actions(request)
        if request.user.username in superUserList:
            return actions
        else:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions
   
    ##Disable delete specific duplex for any users but the superuser(s) listed
    def has_delete_permission(self, request, obj=None):
        if request.user.username in superUserList:
            return True
        else:
            return False
        
admin.site.register(Duplex, DuplexAdmin)





class ResultsAdmin(admin.ModelAdmin):
    search_fields = [
    'duplex__duplex_ID2',
    'duplex__duplex_Name',
    'duplex__duplex_ID',
    'expression_percent',
    'std_dev',
    'positive_control_percent',
    'comments',
    'NTC_percent',
    'cell_line',
    'screen_type',
    'exp_date',                        
    ]
    list_display = (
    'duplex',
    'expression_percent',  
    'std_dev',
    'positive_control_percent',
    'NTC_percent', 
    'cell_line', 
    'screen_type',
    'exp_date',
    'comments',             
    )
    
    
    list_filter = ( 
    'duplex__fm',  
    'screen_type',
    'exp_date',
    'cell_line', 
    'duplex__sense_ID__gene_name',                       
    )   


    ##Disable delete selected results for any users but the superuser(s) listed
    def get_actions(self, request):
        actions = super(ResultsAdmin, self).get_actions(request)
        if request.user.username in superUserList:
            return actions
        else:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions
   
    ##Disable delete specific result for any users but the superuser(s) listed
    def has_delete_permission(self, request, obj=None):
        if request.user.username in superUserList:
            return True
        else:
            return False

admin.site.register(Result, ResultsAdmin)


    




class SenseFilter(admin.SimpleListFilter):
    title = _('Sense or Antisense')
    parameter_name = 'sense'
    
    def lookups(self,request,model_admin):
        return(
            ('s',_('Sense')),
            ('as',_('Antisense')),
        )
    def queryset(self, request, queryset):
        if self.value() == 's':
            return queryset.filter(number__gte = 10000,
                                    number__lte = 19999)
        if self.value() == 'as':
            return queryset.filter(number__gte=20000,
                                   number__lte=29999)



class OppInUseFilter(admin.SimpleListFilter):
    title = _('Complementary oligo in Use')
    parameter_name = 'in_use'

    
    def lookups(self,request,model_admin):
        return(
            ('0',_('Neither in Use')),
            ('2',_('Both in Use')),
            ('1',_('Comp in Use')),
            ('3',_('Comp not in Use')),
        )
    def queryset(self, request, queryset):
                        
        if self.value() == '0':
            sense_num= set([o.number for o in queryset if (o.in_use =='no') and (o.number < 20000)]) 
            anti_opp= set([o.opposite for o in queryset if (o.in_use =='no') and (o.number > 19999)])
            sense_in_anti = sense_num.intersection(anti_opp)
            final = set([o.number for o in queryset if (o.opposite in sense_in_anti) or (o.number in sense_in_anti)])
            return queryset.filter(number__in = final)
        if self.value() == '1':
            sense_num= set([o.number for o in queryset if (o.in_use =='no') and (o.number < 20000)]) 
            sense_num_opp_in_use = set([o.opposite for o in queryset if (o.in_use =='yes') and (o.opposite in sense_num) and (o.number > 19999)])
            anti_num = set([o.number for o in queryset if (o.in_use =='no') and (o.number >19999)]) 
            anti_num_opp_in_use = set([o.opposite for o in queryset if (o.in_use =='yes') and (o.opposite in anti_num) and (o.number <20000)])
            final = anti_num_opp_in_use.union(sense_num_opp_in_use)
            return queryset.filter(number__in = final)
        if self.value() == '2':
            sense_num= set([o.number for o in queryset if (o.in_use =='yes') and (o.number < 20000)]) 
            anti_opp= set([o.opposite for o in queryset if (o.in_use =='yes') and (o.number > 19999)])
            sense_in_anti = sense_num.intersection(anti_opp)
            final = set([o.number for o in queryset if (o.opposite in sense_in_anti) or (o.number in sense_in_anti)])
            return queryset.filter(number__in = final)
        if self.value() == '3':
            sense_num= set([o.number for o in queryset if (o.in_use =='yes') and (o.number < 20000)]) 
            sense_num_opp_not_in_use = set([o.opposite for o in queryset if (o.in_use =='no') and (o.opposite in sense_num) and (o.number > 19999)])
            anti_num = set([o.number for o in queryset if (o.in_use =='yes') and (o.number >19999)]) 
            anti_num_opp_not_in_use = set([o.opposite for o in queryset if (o.in_use =='no') and (o.opposite in anti_num) and (o.number <20000)])
            final = sense_num_opp_not_in_use.union(anti_num_opp_not_in_use)
            return queryset.filter(number__in = final)

  

def make_in_use(modeladmin, request, queryset):
## Set marked ID_Numbers as in use
    queryset.update(in_use = 'yes')
make_in_use.short_description = "Mark selected ID Numbers as in use"

def make_both_in_use(modeladmin, request, queryset):
# Mark selected files and CORRESPONDING ANTISENSE as in use
    for obj in queryset:     
        st = ""
        n = obj.number
        if n < 20000:#sense
            n = n + 10000
            st = "antisense"#opposite strand name
        else: #antisense
            n = n - 10000
            st = "sense"#opposite strand name
        ls = Id_Number.objects.filter(number = n)
        if len(ls)==0:
            modeladmin.message_user(request, "ERROR: corresponding "+st+" oligo ID Number "+str(n)+" does not exist",level=messages.ERROR)
        else:
            ls[0].setInUse('yes')
            obj.setInUse('yes')     
make_both_in_use.short_description = "Mark selected ID Numbers and complementary ID Numbers as in use"

def make_ordered(modeladmin, request, queryset):
## Set marked ID_Numbers as Ordered
    queryset.update(in_use = 'ordered')
make_ordered.short_description = "Mark selected ID Numbers as Ordered"

def make_both_ordered(modeladmin, request, queryset):
# Mark selected files and CORRESPONDING ANTISENSE as Ordered
    for obj in queryset:     
        st = ""
        n = obj.number
        if n < 20000:#sense
            n = n + 10000
            st = "antisense"#opposite strand name
        else: #antisense
            n = n - 10000
            st = "sense"#opposite strand name
        ls = Id_Number.objects.filter(number = n)
        if len(ls)==0:
            modeladmin.message_user(request, "ERROR: corresponding "+st+" oligo ID Number "+str(n)+" does not exist",level=messages.ERROR)
        else:
            ls[0].setInUse('ordered')
            obj.setInUse('ordered')
make_both_ordered.short_description = "Mark selected ID Numbers and complementary ID Numbers as Ordered"
    

class IDAdmin(admin.ModelAdmin):
    
    search_fields = [ 
    'number',
    'in_use',
    ]
    list_display = (
    'number',
    'in_use',
    )
    list_filter = ( 
    OppInUseFilter,
    SenseFilter,
    'in_use',
    )
    
    
    
    actions = [make_ordered,make_both_ordered,make_in_use, make_both_in_use]
    
        
    # Make 'number','in_use', and 'opposite' fields readonly for all but usr4
    def get_readonly_fields(self, request, obj=None):
        if request.user.username == 'usr4':
            return self.readonly_fields
        else:
            if obj: # editing an existing object
                return self.readonly_fields + ('number','in_use','opposite')
    
    
    def has_add_permission(self, request):
    # disables Add Id_Number for all users except usr4
    # IMPORTANT: this cannot be disabled unless the get_readonly_fields definition is also disabled or else will get an error
    # when user tries to add an Id_Number
        if request.user.username == 'usr4':
            return True
        else:
            return False

    

    #Disable delete selected ID_Numbers for ALL users
    def get_actions(self, request):
        actions = super(IDAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        #Disable make_in_use and make_both_in_use actions for all but usr4
        if request.user.username == 'usr4':
            return actions
        elif 'make_in_use' in actions:
            del actions['make_in_use']
        if 'make_both_in_use' in actions:
            del actions['make_both_in_use']
        return actions
        
    

    
    
    

admin.site.register(Id_Number, IDAdmin)
#"""










from django.contrib.admin.sites import AdminSite
AdminSite.site_url = None






