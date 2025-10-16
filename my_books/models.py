from django.db import models

# Create your models here.

class Catigory(models.Model):
    name =  models.CharField(max_length = 100)
    
    class Meta :
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.name}"


class Book (models.Model):
    book_status =[
        ('availble','availble'),
        ('rental','rental'),
        ('solid','solid'),
    ]
    title           =models.CharField(max_length=100)
    auther          =models.CharField(max_length=100)
    book_image      =models.ImageField(upload_to='photos %Y %m %d ',null=True,blank=True)
    auther_image    =models.ImageField(upload_to='photos2 %Y %m %d',null=True,blank=True)
    price           =models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    status          =models.CharField(max_length = 100,choices=book_status,null=True,blank=True)
    pages           =models.IntegerField()
    active          =models.BooleanField(default=True)
    retal_price_day =models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    retal_proid     =models.IntegerField(null=True,blank=True)
    total_rental    =models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    discription     =models.CharField(max_length = 100)
    catigery        =models.ForeignKey(Catigory,on_delete=models.PROTECT)
    class Meta :
        ordering = ['-id']