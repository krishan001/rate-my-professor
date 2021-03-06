from django.db import models
from django.contrib.auth import models as md
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# Create your models here.

class Teacher(models.Model):
    profID = models.CharField('Teacher ID', max_length=3, unique= True)
    profName = models.CharField('Teacher First Name', max_length=120)
    profLastName = models.CharField('Teacher Last Name', max_length=120)

    def __str__(self):
        return u'%s %s' % (self.profName, self.profLastName)

class Module(models.Model):
    Semesters = [('1',1),('2',2)]
    module_ID = models.CharField('Module ID', max_length=3, default = "")
    name = models.CharField('Module Name', max_length=120, default = "")
    semester = models.CharField('Semester', max_length=1, choices = Semesters, default = 1)
    year = models.IntegerField(default = datetime.date.today().year, validators = [MinValueValidator(1904), MaxValueValidator(datetime.date.today().year)])
    teachers = models.ManyToManyField(Teacher)

    class Meta:
        unique_together = ('module_ID','name', 'semester', 'year')

    def __str__(self):
        return u'%s %s' % (self.name,self.year)

class Rating(models.Model):
    module = models.ForeignKey(Module,on_delete=models.PROTECT, default = "")
    teacher = models.ForeignKey(Teacher,on_delete=models.PROTECT, default = "")
    Rating = models.IntegerField(default = 1, validators = [MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return u'%s,    %s,  Score : %d' % (self.module,self.teacher, self.Rating)
