from django.db import models

# Create your models here.

class resumetemplates(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    doc_template=models.FileField(upload_to='resume_templates/',max_length=600)
    
    def __str__(self):
        return self.name

class coverletter(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    letter_template=models.FileField(upload_to='coverletter_templates/',max_length=600)
    
    def __str__(self):
        return self.name


class mergeddocs(models.Model):
    name=models.CharField(max_length=100)
    com_doc=models.FileField(upload_to='merged_templates/',max_length=600)
    
    def __str__(self):
        return self.name

class cv(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    cv_file=models.FileField(upload_to='cv_templates/',max_length=600)
    
    def __str__(self):
        return self.name


class email(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    doc_template=models.FileField(upload_to='email_templates/',max_length=600)
    
    def __str__(self):
        return self.name
    
class created_resumes(models.Model):
    name=models.CharField(max_length=100)
    document=models.FileField(upload_to='created_resumes/',max_length=600)
    def __str__(self):
        return self.name

class created_coverletters(models.Model):
    name=models.CharField(max_length=100)
    document=models.FileField(upload_to='created_coverletters/',max_length=600)
    def __str__(self):
        return self.name
    

class sent_application(models.Model):
    company_name=models.CharField(max_length=100 ,default='GDG')
    company_email=models.CharField(max_length=100,default='GDG',)
    coverletter=models.CharField(max_length=300)
    resume=models.CharField(max_length=300)
    subject=models.CharField(max_length=100 ,default='Test')
    mergedoc=models.CharField(max_length=300)
    date=models.DateTimeField(auto_now_add=True)
    
