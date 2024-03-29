from django.shortcuts import render, redirect
from .models import Salon, Service, Employee, Appointment, Review
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import ReviewForm
from datetime import datetime


def homepage(request):
    salons = Salon.objects.all()
    return render(request, 'homepage.html', {'salons': salons})


def salon(request, salon_id):
    salon_info = Salon.objects.get(pk=salon_id)
    services = Service.objects.filter(salon=salon_id).all()

    return render(request, "salon.html",
                  {'salon': salon_info, 'services': services})


def select_employee(request, salon_id, service_id):
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employees = Employee.objects.filter(salon=salon_id).all()

    return render(request, "select_employee.html",
                  {'salon': salon_info, 'service': service, 'employees': employees})


def select_date(request, salon_id, service_id, employee_id):
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)

    return render(request, "select_date.html",
                  {"salon": salon_info, "service": service, "employee": employee})


def select_hour(request, salon_id, service_id, employee_id, date):
    # All employees work from 10:00 AM to 18:00 PM

    time_slots = range(10, 18)

    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)

    # TODO: Get all the appointments for this employee this day
    #  and compile a list of available timeslots
    appointments = Appointment.objects.filter(salon=salon_id, service_id=service_id, employee=employee_id, date=date)
    appointments_hours = list(time_slots)
    available_slots = [slot for slot in appointments_hours if
                       slot not in [appointment.hour for appointment in appointments]]
    print(available_slots)

    return render(request, "select_hour.html",
                  {'salon': salon_info, 'service': service, 'employee': employee,
                   'time_slots': available_slots, 'date': date})


def add_appointment(request, salon_id, service_id, employee_id, date, hour):
    # Fetched the data from database so give it to the
    # template to render
    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)
    client = User.objects.get(pk=request.user.id)

    # Create an Appointment object based on the arguments
    appointment = Appointment(date=date, hour=hour,
                              employee=employee,
                              salon=salon_info,
                              service=service,
                              client=client)
    # Save the Appointment object into the database
    appointment.save()

    # Render the appointment success template
    return render(request, 'appointment_success.html', {
        'salon': salon_info, 'service': service, 'employee': employee,
        'date': date, 'hour': hour
    })


def my_appointments(request):
    # Fetch all the appointments from the database
    # where the client is the user that is requesting it
    appointments = Appointment.objects.filter(client=request.user.id).all()

    return render(request, 'my_appointments.html', {'appointments': appointments})


def logout_page(request):
    logout(request)
    return redirect('homepage')


def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})


def review(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.appointment = appointment
            review.client = request.user
            return redirect('salon', pk=appointment.salon.id)
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form, 'appointment': appointment})
