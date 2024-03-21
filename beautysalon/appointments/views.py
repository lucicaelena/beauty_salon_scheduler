from django.shortcuts import render
from .models import Salon, Service, Employee, Appointment


# Create your views here.

def homepage(request):
    salons = Salon.objects.all()
    return render(request, 'homepage.html', {'salons': salons})

def salon(request,salon_id):
    salon_info = Salon.objects.get(pk=salon_id)
    services = Service.objects.filter(salon=salon_id).all()
    return render(request, 'salon.html', {'salon':salon_info,'services':services})

def select_employee(request,salon_id,service_id):
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employees = Employee.objects.filter(salon=salon_id).all()
    return render(request,'select_employee.html', {'salon': salon_info,'service': service,'employees': employees})

def select_date(request,salon_id,service_id,employee_id):
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)
    return render(request,'select_date.html',{'salon': salon_info,'service': service,'employee':employee})

def select_hour(request,salon_id,service_id,employee_id,date):
    time_slots = range(10,18)
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)
    # appointments = Appointment.objects.filter(salon=salon_id,employee=employee_id)
    return render(request,'select_hour.html',{'salon':salon_info,'service':service,'employee':employee,'time_slots':time_slots,'date':date})


