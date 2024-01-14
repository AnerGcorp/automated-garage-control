from distutils.command import upload
from secrets import choice
from django.db import models
from django.forms import ModelForm, Textarea # for changing forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Soldier(models.Model):
    military_title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="soldier/", blank=True, null=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    birthday = models.CharField(max_length=255, blank=True)
    birth_place = models.TextField(blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    knowledge = models.TextField(blank=True)
    marriage_status = models.CharField(max_length=50, blank=True)
    invited_hw = models.TextField(blank=True)
    being_abroad = models.TextField(blank=True)
    last_job = models.TextField(blank=True)
    last_illness = models.TextField(blank=True)
    harby_kasam_date = models.CharField(max_length=255, blank=True)
    being_in_prison = models.TextField(blank=True)
    home_address = models.TextField(blank=True)
    specific_notes = models.TextField(blank=True)
    def __str__(self):
        return "{0} {1} {2}".format(self.military_title, self.name, self.surname)

class BeenMilitaryBase(models.Model):
    military_base = models.CharField(max_length=50)
    military_acc_pos = models.CharField(max_length=100, blank=True) # harby hasap hunari
    military_base_enter_date = models.CharField(max_length=255, blank=True) # h/b sanawyna giren senesi
    military_base_exit_date = models.CharField(max_length=255, blank=True) # h/b sanawyna chykan senesi
    belongs_to = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name="soldier_base")

    def __str__(self):
        return "Harby Gullugy Geçmegi"

class CloseRelative(models.Model):
    relative_degree = models.CharField(max_length=50)
    birth_year = models.PositiveIntegerField(default=1900,
        validators=[
            MaxValueValidator(timezone.now().year),
            MinValueValidator(1900)
        ])
    aaa_field = models.TextField()
    work_place_and_position = models.TextField(max_length=5000)
    belongs_to = models.ForeignKey(Soldier, on_delete=models.CASCADE, related_name="soldier_relative")

    def __str__(self):
        return "Ýakyn Garyndaşlary"

class Officer(models.Model):
    military_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    position = models.TextField(blank=True)
    photo = models.ImageField(upload_to="officier/", blank=True, null=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.military_title, self.name, self.surname)

class CarModel(models.Model):
    rfid = models.CharField(max_length=255, null=True)
    model_car = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)
    patron = models.ForeignKey(Officer, on_delete=models.CASCADE, blank=True)
    driver = models.ForeignKey(Soldier, on_delete=models.CASCADE, blank=True)
    corr_principal = models.TextField(blank=True)
    belongs_building = models.TextField(blank=True)
    car_photo = models.ImageField(upload_to="cars/", blank=True, null=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return "{0} {1}".format(self.model_car, self.license_number)

class Duty(models.Model):
    place = models.TextField(blank=True)
    position = models.TextField(blank=True)
    on_duty = models.ForeignKey(Soldier, on_delete=models.CASCADE, blank=True)
    date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return "{0} {1}".format(self.place, self.on_duty)

class CarMovement(models.Model):
    move_side = [
        ("Girdi", "Girdi"),
        ("Çykdy", "Chykdy")
    ]
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    movement = models.CharField(max_length=7, choices=move_side, default="Girdi")
    screenshot = models.ImageField(upload_to="movement/", blank=True, null=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.car, self.time, self.movement)
