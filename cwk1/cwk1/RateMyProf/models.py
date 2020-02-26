from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.

class Prof(models.Model):
    professorName = models.CharField(max_length = 50)
    professorCode = models.CharField(max_length = 3, unique = True)

    def __str__(self):
        return self.professorName

class Module(models.Model):
    moduleTitle = models.CharField(max_length = 50)
    moduleCode = models.CharField(max_length = 3, unique = True)
    def __str__(self):
        return self.moduleTitle

class Student(models.Model):
    studentName = models.CharField(max_length = 50)
    def __str__(self):
        return self.studentName

class ModuleInstance(models.Model):
    ModuleTitle = models.ForeignKey(Module,on_delete=models.CASCADE)
    Semester = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    Year = models.IntegerField(default = datetime.date.today().year, validators = [MinValueValidator(1904), MaxValueValidator(datetime.date.today().year)])
    Professor = models.ForeignKey(Prof, on_delete=models.CASCADE)


class Rating(models.Model):
    studentName = models.ForeignKey(Student,on_delete=models.CASCADE)
    rating = models.IntegerField(default = None, validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return self.rating

