from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Salon(models.Model):
    name = models.TextField()
    address = models.TextField()
    photo = models.ImageField(upload_to='salons/')

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.TextField()
    photo = models.ImageField(upload_to="employees/")

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.salon.name}] {self.name}"


class Service(models.Model):
    name = models.TextField()
    time = models.IntegerField()
    price = models.IntegerField()

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.salon}] {self.name} - {self.time} min - {self.price} RON"


class Appointment(models.Model):
    date = models.DateTimeField()

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.salon}] {self.service.name} - {self.employee.name} - {self.date}"


class Review(models.Model):

    description = models.TextField()
    score = models.IntegerField()

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)