from django.shortcuts import render

# Create your views here.

#This is a django application to help make job appplication simpler by making template customization simpler ,company applicatins sents and dates

# create view to homepage
def home(request):
    return render(request,'home.html')