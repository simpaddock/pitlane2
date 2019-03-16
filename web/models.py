from django.db import models
from django.db.models import *
from web.utils import importResultFile

# Create your models here.

class Country(models.Model):
  Name = CharField(max_length=100)
  def __str__(self):
    return self.Name

class Track(models.Model):
  Name = CharField(max_length=100)
  Longitude = FloatField()
  Latitude = FloatField()
  def __str__(self):
    return self.Name

class Session(models.Model):
  Name = CharField(max_length=100)
  StartDateTime = DateTimeField()
  EndDateTime = DateTimeField()
  def __str__(self):
    return self.Name

class Season(models.Model):
  Name = CharField(max_length=100)
  def __str__(self):
    return self.Name

class Race(models.Model):
  Name = CharField(max_length=100)
  IsDriverOfTheDayVoteActive = BooleanField(default=False)
  Session = ManyToManyField(Session)
  Season = ForeignKey(Season, on_delete=CASCADE,null=False)
  def __str__(self):
    return self.Name

class Driver(models.Model):
  FirstName = CharField(max_length=100)
  LastName = CharField(max_length=100)
  def __str__(self):
    return "{0}, {1}".format(self.LastName, self.FirstName)

class TeamEntry(models.Model):
  Name = CharField(max_length=100)
  Identifier = CharField(max_length=100)
  Email = EmailField()
  Drivers = ManyToManyField(Driver)
  Season = ForeignKey(Season,on_delete=CASCADE)
  def __str__(self):
    return self.Name

class Livery(models.Model):
  File = FileField()
  Identifier = CharField(max_length=100)

class DriverOfTheDayVote(models.Model):
  Race = ForeignKey(Race,on_delete=CASCADE,null=False)
  Driver = ForeignKey(Driver, on_delete=CASCADE,null=False)

class VehicleClass(models.Model):
  Name = CharField(max_length=100)
  def __str__(self):
    return self.Name

class FinishStatus(models.Model):
  Name = CharField(max_length=100)
  def __str__(self):
    return self.Name

class Lap(models.Model):
  Position = IntegerField()
  Duration = FloatField()
  Number = IntegerField()

class DriverResult(models.Model):
  Position = IntegerField()
  GridPosition = IntegerField()
  Points = FloatField()
  AverageSpeed = FloatField()
  Stops = IntegerField()
  CarNumber = IntegerField()
  ArePointsScoring = BooleanField()
  ArePointsScoringForTeam = BooleanField()
  VehicleClass = ForeignKey(VehicleClass, on_delete=CASCADE,null=False)
  FinishStatus = ForeignKey(FinishStatus, on_delete=CASCADE,null=False)
  RaceResult = ForeignKey("RaceResult", on_delete=CASCADE,null=False)
  Driver = ForeignKey(Driver, on_delete=CASCADE,null=False)
  Laps  = ManyToManyField(Lap,null=True)
  def __str__(self):
    return "{0}: {1}".format(self.Driver, self.Position)

class RaceResult(models.Model):
  File = FileField()
  Race = ForeignKey(Race, on_delete=CASCADE,null=False)
  DriverResults = ManyToManyField(DriverResult,null=True,blank=True)
  def save(self, *args, **kwargs):
    super(RaceResult, self).save(*args, **kwargs)
    importResultFile(self)

  def __str__(self):
    return self.Race.Name
class Category(models.Model):
  Name = CharField(max_length=300)
  def __str__(self):
    return self.Name

class TextBlock(models.Model):
  Name = CharField(max_length=300)
  Content = TextField()
  DateTime = DateTimeField()
  IsDraft = BooleanField()
  Categories = ManyToManyField(Category)
  def __str__(self):
    return self.Name

class Upload(models.Model):
  Name = CharField(max_length=300)
  File = FileField()
  def __str__(self):
    return self.Name
