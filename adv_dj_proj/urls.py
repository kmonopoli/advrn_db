from django.conf.urls import include, url
from django.contrib import admin
from dapp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'session_security/', include('session_security.urls')),
    
    url(r'^accounts/', include('django.contrib.auth.urls')),


    url(r'^admin/password_reset/$','django.contrib.auth.views.password_reset',name='admin_password_reset'), 
    url(r'^admin/password_reset/done/$','django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/','django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect': '/accounts/password/done/'}, name='password_reset_confirm'),

    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'), 
    url(r'^accounts/password/done/$','django.contrib.auth.views.password_reset_complete'), 
    url(r'^accounts/profile/', include(admin.site.urls)),
    url('', admin.site.urls),


    url(r'^home','dapp.views.home', name='home'),
    url(r'^acad','dapp.views.acad', name='acad'),


]

admin.site.site_header = 'Advirna Database'



