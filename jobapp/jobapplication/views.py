from django.shortcuts import render,redirect,get_object_or_404
from .models import resumetemplates,coverletter,cv,mergeddocs,email,created_resumes,created_coverletters,sent_application
import win32com.client
import pythoncom
from django.conf import settings
from django.contrib import messages
import os
from docx2pdf import convert 
from io import BytesIO
from django.core.files import File
from django.http import FileResponse,HttpResponse
import tempfile
from datetime import datetime
import PyPDF2
import datetime as datetim
from django.core.mail import EmailMessage
from .functions import create_cover_letter,create_a_resume,mergepdff,get_coverlink,get_resumelink,get_mergelink
import textwrap

# Create your views here.

#This is a django application to help make job appplication simpler by making template customization simpler ,company applicatins sents and dates,




# create view to homepage
def home(request):
    
    return render(request,'home.html')


def manage_sentapplications(request):
    appl=sent_application.objects.all()
    context={'app':appl}
    return render(request,'managesent.html',context)


def index(request):
    return render(request,'index.html')

def resumes(request):
    return render(request,'resume.html')


def addtemplate(request):
    if request.method == "POST" or request.method == "FILES":
        name = request.POST.get('name')  #add a way to add csv file to uplod items
        description=request.POST.get('description')
        image = request.FILES.get('image')
        document = request.FILES.get('doc')
        if document and image:
            resumetemplates.objects.create(name=name,description=description,image=image,doc_template=document)
            return redirect('mresume_templates')
        else:
            messages.error(request, 'provide image/document')
    return render(request,'addtemplate.html')

def add_cv(request):
    if request.method == "POST" or request.method == "FILES":
        name = request.POST.get('name')  #add a way to add csv file to uplod items
        description=request.POST.get('description')
        image = request.FILES.get('image')
        document = request.FILES.get('doc')
        if document and image:
            cv.objects.create(name=name,description=description,image=image,cv_file=document)
            return redirect('mcv')
        else:
            messages.error(request, 'provide image/document')
    return render(request,'addcv.html')

def add_coverletter(request):
    if request.method == "POST" or request.method == "FILES":
        name = request.POST.get('name')  #add a way to add csv file to uplod items
        description=request.POST.get('description')
        image = request.FILES.get('image')
        document = request.FILES.get('doc')
        if document and image:
            coverletter.objects.create(name=name,description=description,image=image,letter_template=document)
            return redirect('mcover_template')
        else:
            messages.error(request, 'provide image/document')
    
    return render(request,'addcoverletter.html')

def add_email(request):
    if request.method == "POST" or request.method == "FILES":
        name = request.POST.get('name')  #add a way to add csv file to uplod items
        description=request.POST.get('description')
        image = request.FILES.get('image')
        document = request.FILES.get('doc')
        if document and image:
            email.objects.create(name=name,description=description,image=image,doc_template=document)
        else:
            messages.error(request, 'provide image/document')
    return render(request,'addemail.html')

def merge_doc(request):
    cv_list = cv.objects.all()
    coverletter_list = created_coverletters.objects.all()
    resume_list = created_resumes.objects.all()

    # Initialize variables to store PDF paths
    cv_pdf_path = None
    coverletter_pdf_path = None
    resume_pdf_path = None

    if request.method == 'POST':
        selected_cv_id = request.POST.get('selected_cv_id', None)
        selected_coverletter_id = request.POST.get('selected_coverletter_id', None)
        selected_resume_id = request.POST.get('selected_resume_id', None)
        title = request.POST.get('title', '')

        # Check if at least one of cover letter or resume IDs exist and fetch their file paths
        if selected_coverletter_id:
            coverletterdoc = created_coverletters.objects.get(id=selected_coverletter_id)
            coverletter_pdf_path = coverletterdoc.document.path
        if selected_resume_id:
            resdoc = created_resumes.objects.get(id=selected_resume_id)
            resume_pdf_path = resdoc.document.path

        # Check if at least one of cover letter or resume PDFs is selected for merging
        if coverletter_pdf_path or resume_pdf_path:
            pdf_merger = PyPDF2.PdfMerger()

            # Add the CV PDF (if selected)
            if selected_cv_id:
                cvdoc = cv.objects.get(id=selected_cv_id)
                cv_pdf_path = cvdoc.cv_file.path
                pdf_merger.append(cv_pdf_path)

            # Add the selected cover letter PDF (if available)
            if coverletter_pdf_path:
                pdf_merger.append(coverletter_pdf_path)

            # Add the selected resume PDF (if available)
            if resume_pdf_path:
                pdf_merger.append(resume_pdf_path)

            # Create a temporary file to store the merged PDF
            with tempfile.NamedTemporaryFile(delete=False) as merged_pdf_file:
                pdf_merger.write(merged_pdf_file)

            # Create a response with the merged PDF
            with open(merged_pdf_file.name, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            merged_doc = mergeddocs(name=title)
            merged_doc.com_doc.save(f'{title}.pdf', File(open(merged_pdf_file.name, 'rb')))
            merged_doc.save()
            # Set the Content-Disposition header for downloading
            response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'

            # Return the response
            return response

    context = {
        'cv_list': cv_list,
        'coverletter_list': coverletter_list,
        'resume_list': resume_list,
    }

    return render(request, 'merged.html', context)

def cover_letter(request):
    return render(request,'coverletter.html')

def e_mail(request):
    return render(request,'email.html')

def c_v(request):
    return render(request,'cv.html')

#creating routes for creatting cv,resume,email,coverletter by selecting templates and entering data.cemail representing create email....

def cemail(request):
    return render(request,'cemail.html')



def cresume(request):
    pythoncom.CoInitialize()
    rtemplate = resumetemplates.objects.all()
    content = {'templates': rtemplate}
    
    if request.method == 'POST':
        templateid = request.POST.get('selected_template_id', None)
        title = request.POST.get('title', '')
        resumetemplate = resumetemplates.objects.get(id=int(templateid))
        file_url = resumetemplate.doc_template.url

        if file_url.startswith('/'):
            file_url = file_url[1:]
        
        if file_url.startswith('/'):
            file_url = file_url[1:]
        
        file_path = os.path.join(settings.MEDIA_ROOT, file_url[6:])
        
        # Define the path for the PDF within the cpdf directory
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'cpdf')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        pdf_path = os.path.join(pdf_dir, f'{title}.pdf')
        
        word = win32com.client.Dispatch("Word.Application")

        # Open the Word document
        doc = word.Documents.Open(file_path)

        # Iterate through Content Controls and set their values
        for cc in doc.ContentControls:
            if cc.Title == "Jobtitle":
                cc.Range.Text = title
        
        # Save the Word document as a PDF in the cpdf directory
        doc.SaveAs(pdf_path, FileFormat=17)  # FileFormat 17 is for PDF
        doc.Close()
        word.Quit()

        # Save the generated PDF in the created_resumes model
        new_resume = created_resumes(name=title)
        new_resume.document.save(f'{title}.pdf', open(pdf_path, 'rb'))
        new_resume.save()

        # Provide a download link to the user
        response = FileResponse(open(pdf_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'

        success_message = 'PDF saved successfully.'

        # Render the cresume.html template with the success message
        return render(request, 'cresume.html', {'content': content, 'success_message': success_message})

    return render(request, 'cresume.html', content)

def cletter(request):
    pythoncom.CoInitialize()
    rtemplate = coverletter.objects.all()
    content = {'templates': rtemplate}
    
    if request.method == 'POST':
        templateid = request.POST.get('selected_template_id', None)
        company = request.POST.get('title', '')
        resumetemplate = coverletter.objects.get(id=int(templateid))
        file_url = resumetemplate.letter_template.url

        if file_url.startswith('/'):
            file_url = file_url[1:]
        
        if file_url.startswith('/'):
            file_url = file_url[1:]
        
        file_path = os.path.join(settings.MEDIA_ROOT, file_url[6:])
        
        # Define the path for the PDF within the cpdf directory
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'cpdf')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        pdf_path = os.path.join(pdf_dir, f'{company}.pdf')
        
        word = win32com.client.Dispatch("Word.Application")
        today = datetime.today()

# Format the date as "day month year"
        fdate = today.strftime("%dth %B %Y")

        # Open the Word document
        doc = word.Documents.Open(file_path)
        # Iterate through Content Controls and set their values
        for cc in doc.ContentControls:
            if cc.Title == "company":
                cc.Range.Text = company
            if cc.Title=='date':
                cc.Range.Text=fdate
        
        # Save the Word document as a PDF in the cpdf directory
        doc.SaveAs(pdf_path, FileFormat=17)  # FileFormat 17 is for PDF
        doc.Close()
        word.Quit()

        # Save the generated PDF in the created_resumes model
        new_cover = created_coverletters(name=company)
        new_cover.document.save(f'{company}.pdf', open(pdf_path, 'rb'))
        new_cover.save()

        # Provide a download link to the user
        response = FileResponse(open(pdf_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{company}.pdf"'

        success_message = 'PDF saved successfully.'

        # Render the cresume.html template with the success message
        return render(request, 'cletter.html', {'content': content, 'success_message': success_message})

    return render(request, 'cletter.html', content)
    
    
# creating routes for managing templates and created files key for naming mresume rep managing resume

def mresume(request):
    templates=created_resumes.objects.all()
    content={'templates':templates}
    return render(request,'mresume.html',content)

def mresume_templates(request):
    templates=resumetemplates.objects.all()
    content={'templates':templates}
    return render(request,'mresume_templates.html',content)

def delete_resumet(request,tempid):
    id=tempid
    template=resumetemplates.objects.get(id=int(id))
    if template:
        template.delete
    else:
        messages.error(request, 'Template not deleted')
    return redirect('mresume_templates')

def delete_resumes(request,tempid):
    id=tempid
    template=created_resumes.objects.get(id=int(id))
    if template:
        template.delete
        # print('yes')
    else:
        messages.error(request, 'Template not deleted')
    return redirect('mresume')

def mcv(request):
    templates=cv.objects.all()
    content={'templates':templates}
    return render(request,'mcv.html',content)

def dcv(request,tempid):
    id=tempid
    template=cv.objects.get(id=int(id))
    if template:
        template.delete
        # print('yes')
    else:
        messages.error(request, 'Template not deleted')
    return redirect('mcv')
    
def mcover_letters(request):
    templates=created_coverletters.objects.all()
    content={'templates':templates}
    return render(request,'mcletter.html',content)

def dcover_letters(request,tempid):
    id=tempid
    template=created_coverletters.objects.get(id=int(id))
    if template:
        template.delete
        messages.success(request, 'Template deleted')
        # print('yes')
    else:
        messages.error(request, 'Template not deleted')
    return redirect('mcover_letters')

def mcover_template(request):
    templates=coverletter.objects.all()
    content={'templates':templates}
    return render(request,'mctemplate.html',content)

def dcover_template(request,tempid):
    id=tempid
    template=coverletter.objects.get(id=int(id))
    if template:
        template.delete
        messages.success(request, 'Template deleted')
        # print('yes')
    else:
        messages.error(request, 'Template not deleted')
    return redirect('mcover_template')
    
def send_application(request):
    cover_lt=coverletter.objects.all()
    resume_lt=resumetemplates.objects.all()
    content={'cover_lt':cover_lt,'resume_lt':resume_lt}
    if request.method=='POST':
        # get coverletter templates and resume templates
        companyname=request.POST['company_name']
        jobtitle=request.POST['title']
        companyemail=request.POST['company_email']
        title2=request.POST['title2']
        selected_coverletter_id = request.POST.get('selected_coverletter_id',None)
        selected_resume_id = request.POST.get('selected_resume_id',None)
        print(selected_coverletter_id)
        print(selected_resume_id)
        
        current_time = datetim.datetime.now().time()
        
        if selected_coverletter_id=='' or selected_coverletter_id==None:
            selected_coverletter_id=1
        if selected_resume_id==None or selected_resume_id=='':
            selected_resume_id=1
        
        
        
        s,coverletterlink=create_cover_letter(companyname,title2,int(selected_coverletter_id))
        j,resumelink=create_a_resume(jobtitle,int(selected_resume_id))
        
        current_time = datetim.datetime.now().time()
        
        
        if current_time < datetim.time(12, 0, 0):
           message = textwrap.dedent('''\
                Good morning,
                My name is Dan Newton Gatobu, a BSc software engineering student in my final year at Muranga University of Science and Technology. I am writing to request an internship placement in your company. Attached, please find my cover letter detailing the request and my Resume. Your positive response will be highly appreciated.
                Regards,
                Dan Newton Gatobu''')
        else:
            message = textwrap.dedent('''\
                Good afternoon,
                My name is Dan Newton Gatobu, a BSc software engineering student in my final year at Muranga University of Science and Technology. I am writing to request an internship placement in your company. Attached, please find my cover letter detailing the request,and my resume. Your positive response will be highly appreciated.
                Regards,
                Dan Newton Gatobu''')
        subject=request.POST['subject']
        from_email='rdan99848@gmail.com'
        recipient_list = [companyemail]
        mergedfilelinks=mergepdff(coverletterlink,resumelink,jobtitle) 
        
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach_file(coverletterlink)
        email.attach_file(resumelink)
        email.attach_file(mergedfilelinks)
        email.send()
        sent_application.objects.create(company_name=companyname,company_email=companyemail,coverletter=coverletterlink,resume=resumelink,mergedoc=mergedfilelinks,subject=subject)
        
        # remain on page but provide message on top saying sucessfully sent
        
        sucess_message='Email sent successfully'
        fail_message='Email not sent'
        
        
        
    return render(request,'sendapp.html',content)

def resend(request):
    if request.method=='POST':
        id=request.POST['id']
        #save the id in a session
        request.session['resend_id']=id
        
        return redirect('resend_info')

    return redirect('managesent')

def resend_info(request):
    id=request.session['resend_id']
    
    
    cover_lt=coverletter.objects.all()
    
    resume_lt=resumetemplates.objects.all()
    content={'cover_lt':cover_lt,'resume_lt':resume_lt}
    # get obeject with id 3 from sent_application
    # f=sent_application.objects.all()

    sent_app = get_object_or_404(sent_application, pk=id)
    #get company name,email,subject
    company_name=sent_app.company_name
    company_email=sent_app.company_email
    subject=sent_app.subject
    
    if request.method=='POST':
        # get coverletter templates and resume templates
        
        jobtitle=request.POST['title']
        title2=request.POST['title2']
       
        selected_coverletter_id = request.POST.get('selected_coverletter_id',None)
        if selected_coverletter_id=='' or selected_coverletter_id==None:
            selected_coverletter_id=2
        selected_resume_id = request.POST.get('selected_resume_id',None)
        if selected_resume_id=='' or selected_resume_id==None:
            selected_resume_id=2
        
        current_time = datetim.datetime.now().time()
        # print('hhhhh')
        
        
        if current_time < datetim.time(12, 0, 0):
           message = textwrap.dedent('''\
                Good morning,
                My name is Dan Newton Gatobu, a BSc software engineering student in my final year at Muranga University of Science and Technology. I am writing to request an internship placement in your company. Attached, please find my cover letter detailing the request and my Resume. Your positive response will be highly appreciated.
                Regards,
                Dan Newton Gatobu''')
        else:
            message = textwrap.dedent('''\
                Good afternoon,
                My name is Dan Newton Gatobu, a BSc software engineering student in my final year at Muranga University of Science and Technology. I am writing to request an internship placement in your company. Attached, please find my cover letter detailing the request,and my resume. Your positive response will be highly appreciated.
                Regards,
                Dan Newton Gatobu''')
            
        # print('hhhhh')
        if selected_coverletter_id=='' or selected_coverletter_id==None:
            mes='Please select a cover letter'
            print(selected_coverletter_id)
            return redirect('resend_info')
        if selected_resume_id==None or selected_resume_id=='':
            mes='Please select a resume'
            print(selected_resume_id)
            return redirect('resend_info')
        
        print('hhhhh')
        
        s,coverletterlink=create_cover_letter(company_name,title2,int(selected_coverletter_id))
        j,resumelink=create_a_resume(jobtitle,int(selected_resume_id))
        # print('hhhhh')
        
        from_email='rdan99848@gmail.com'
        recipient_list = [company_email]
        mergedfilelinks=mergepdff(coverletterlink,resumelink,jobtitle) 
        
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach_file(coverletterlink)
        email.attach_file(resumelink)
        email.attach_file(mergedfilelinks)
        email.send()
        
    # delete the resend session
        del request.session['resend_id']
        return redirect('managesent')
    
    
    return render(request,'resend_info.html',content)


def send_rebuild(request):
    id=request.session['resend_id']
    print(id)
    cover_lt=coverletter.objects.all()
    resume_lt=resumetemplates.objects.all()
    content={'cover_lt':cover_lt,'resume_lt':resume_lt}
    # get obeject with id 3 from sent_application
    # f=sent_application.objects.all()

    sent_app = get_object_or_404(sent_application, pk=id)
    # print('jjj')
    #get company name,email,subject
    company_name=sent_app.company_name
    company_email=sent_app.company_email
    subject=sent_app.subject
    print(company_email)
    
    if request.method=='POST':
        # get coverletter templates and resume templates
        jobtitle=request.POST['title']
        title2=request.POST['title2']
        selected_coverletter_id = request.POST.get('selected_coverletter_id',None)
        selected_resume_id = request.POST.get('selected_resume_id',None)
        
        
        message=0
        if selected_coverletter_id=='' or selected_coverletter_id==None:
            message='Please select a cover letter'
            messages.error(request, message)
            return render(request,'test.html')
        if selected_resume_id==None or selected_resume_id=='':
            message='Please select a resume'
            messages.error(request, message)
            return render(request,'test.html')
        
        
        
        s,coverletterlink=create_cover_letter(company_name,title2,int(selected_coverletter_id))
        j,resumelink=create_a_resume(jobtitle,int(selected_resume_id))
        
        from_email='rdan99848@gmail.com'
        recipient_list = [company_email]
        mergedfilelinks=mergepdff(coverletterlink,resumelink,jobtitle) 
        
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach_file(coverletterlink)
        email.attach_file(resumelink)
        email.attach_file(mergedfilelinks)
        email.send()
    
    
       

    return render(request,'test.html',content)