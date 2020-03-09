from django.db import models
from django.contrib.auth import models as md

# Create your models here.

class Teacher(models.Model):
    t_ID = models.CharField('Teacher ID', max_length=3, unique= True)
    t_name = models.CharField('Teacher First Name', max_length=120)
    t_last_Name = models.CharField('Teacher Last Name', max_length=120)

    def __str__(self):
        return u'%s %s' % (self.t_name, self.t_last_Name)

class Module(models.Model):
    Semesters = [('1',1),('2',2)]
    module_ID = models.CharField('Module ID', max_length=3, default = "")
    name = models.CharField('Module Name', max_length=120, default = "")
    semester = models.CharField('Semester', max_length=1, choices = Semesters, default = 1)
    year = models.CharField('Year', max_length=4, default = "2020")
    teachers = models.ManyToManyField(Teacher)

    class Meta:
        unique_together = ('module_ID','name', 'semester', 'year')

    def __str__(self):
        return u'%s %s' % (self.name,self.year)

class Rating(models.Model):
    module = models.ForeignKey(Module,on_delete=models.PROTECT, default = "")
    teacher = models.ForeignKey(Teacher,on_delete=models.PROTECT, default = "")
    Rating = models.FloatField(default = 0)

    def __str__(self):
        return u'%s,    %s,  Score : %d' % (self.module,self.teacher, self.Rating)
