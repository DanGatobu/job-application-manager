from django.http import FileResponse,HttpResponse
import win32com.client
import pythoncom
from .models import coverletter,created_coverletters,created_resumes,resumetemplates,cv,mergeddocs
from django.shortcuts import render,redirect
import os
from django.conf import settings
import PyPDF2
import tempfile
from datetime import datetime
from django.core.files import File
from io import BytesIO




def create_cover_letter(companyname):
    pythoncom.CoInitialize()
    company=companyname
    templateid=1
    resumetemplate = coverletter.objects.get(id=int(templateid))
    file_url = resumetemplate.letter_template.url
    print(file_url)
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
    return  new_cover.pk,pdf_path

def create_a_resume(title):
    title=title
    pythoncom.CoInitialize()
    templateid=1
    resumetemplate = resumetemplates.objects.get(id=int(templateid))
    file_url = resumetemplate.doc_template.url

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
    return new_resume.pk,pdf_path



def mergepdff(firstlink, secondlink, companyname):
    pdf_merger = PyPDF2.PdfMerger()
    pdf_merger.append(firstlink)
    pdf_merger.append(secondlink)
    
    # Create a BytesIO buffer to store the merged PDF
    merged_pdf_path = os.path.join(settings.BASE_DIR, 'media', 'merged_templates', f'{companyname}_merged.pdf')
    
    # Create a merged PDF file in the 'merged_templates/' directory
    with open(merged_pdf_path, 'wb') as merged_pdf_file:
        pdf_merger.write(merged_pdf_file)

    # Return the link to the merged PDF
    merged_pdf_link = os.path.join('media', 'merged_templates', f'{companyname}_merged.pdf')
    return merged_pdf_link

def get_coverlink(idd):
    record=created_coverletters.objects.get(id=idd)
    link=record.document.url
    return link

def get_resumelink(idd):
    record=created_resumes.objects.get(id=idd)
    link=record.document.url
    return link

def get_mergelink(idd):
    record = mergeddocs.objects.get(id=idd)
    document_relative_path = record.com_doc.name

    # Construct the full path
    full_path = full_path.replace('\\', '\\')

    # Convert the full path to a raw string
    full_path_raw = rf"{full_path}"

    return full_path_raw
    
