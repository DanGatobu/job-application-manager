from django.urls import path

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('index',views.index,name='index'),
    path('resume',views.resumes,name='resume'),
    path('addtemplate',views.addtemplate,name='addtemplate'),
    path('add_coverletter',views.add_coverletter,name='add_coverletter'),
    path('addcv',views.add_cv,name='addcv'),
    path('addemail',views.add_email,name='addemail'),
    path('email',views.e_mail,name='email'),
    path('merge',views.merge_doc,name='merge'),
    path('coverletter',views.cover_letter,name='coverletter'),
    path('cv',views.c_v,name='cv'),
    path('cemail',views.cemail,name='cemail'),
    path('cresume',views.cresume,name='cresume'),
    path('cletter',views.cletter,name='cletter'),
    path('mresume_templates',views.mresume_templates,name='mresume_templates'),
    path('dresumet/<str:tempid>',views.delete_resumet,name='dresumet'),
    path('dresume/<str:tempid>',views.delete_resumes,name='dresume'),
    path('mresume',views.mresume,name='mresume'),
    path('mcv',views.mcv,name='mcv'),
    path('dcv/<str:tempid>',views.delete_resumes,name='dcv'),
    path('dcover_letters/<str:tempid>',views.dcover_letters,name='dcover_letters'),
    path('mcover_letters',views.mcover_letters,name='mcover_letters'),
    path('dcover_template/<str:tempid>',views.dcover_template,name='dcover_template'),
    path('mcover_template',views.mcover_template,name='mcover_template'),
    path('mergedoc',views.merge_doc,name='mergedoc'),
    path('sendapp',views.send_application,name='sendapp'),
    path('managesent',views.manage_sentapplications,name='managesent'),
    path('resend',views.resend,name='resend'),
    path('resend_info',views.resend_info,name='resend_info'),
    path('test',views.send_rebuild,name='test')
    
    
    
    
    
    ]