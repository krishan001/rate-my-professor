from django.db import models
from django.contrib.auth import models as md
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# Create your models here.

class Professor(models.Model):
    t_ID = models.CharField('Professor ID', max_length=3, unique= True)
    t_name = models.CharField('Professor First Name', max_length=120)
    t_last_Name = models.CharField('Professor Last Name', max_length=120)

    def __str__(self):
        return u'%s %s' % (self.t_name, self.t_last_Name)

class ModuleInstance(models.Model):
    Semesters = [('1',1),('2',2)]
    module_ID = models.CharField('Module ID', max_length=3, default = "")
    name = models.CharField('Module Name', max_length=120, default = "")
    semester = models.CharField('Semester', max_length=1, choices = Semesters, default = 1)
    year = models.IntegerField(default = datetime.date.today().year, validators = [MinValueValidator(1904), MaxValueValidator(datetime.date.today().year)])
    profs = models.ManyToManyField(Professor)

    class Meta:
        unique_together = ('module_ID','name', 'semester', 'year')

    def __str__(self):
        return u'%s %s' % (self.name,self.year)

class Rating(models.Model):
    module = models.ForeignKey(ModuleInstance,on_delete=models.PROTECT, default = "")
    prof = models.ForeignKey(Professor,on_delete=models.PROTECT, default = "")
    Rating = models.FloatField(default = 1)

    def __str__(self):
        return u'%s,    %s,  Score : %d' % (self.module,self.prof, self.Rating)
