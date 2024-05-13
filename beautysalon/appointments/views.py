from django.shortcuts import render, redirect
from .models import Salon, Service, Employee, Appointment, Review
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import ReviewForm
from django.urls import reverse

def homepage(request):
    salons = Salon.objects.all()
    return render(request, 'homepage.html', {'salons': salons})


def salon(request, salon_id):
    salon_info = Salon.objects.get(pk=salon_id)
    services = Service.objects.filter(salon=salon_id).all()
    reviews = Review.objects.filter(appointment__salon_id=salon_id).order_by('-id')
    return render(request, "salon.html",
                  {'salon': salon_info, 'services': services,'reviews':reviews})


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


    time_slots = range(10, 18)

    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)

    existing_appointments = Appointment.objects.filter(employee=employee, date=date).values_list('hour', flat=True)
    available_time_slots = [time_slot for time_slot in time_slots if
                            time_slot not in [appointment.hour for appointment in existing_appointments]]


    return render(request, "select_hour.html",
                  {'salon': salon_info, 'service': service, 'employee': employee,
                   'time_slots':available_time_slots, 'date': date})


def add_appointment(request, salon_id, service_id, employee_id, date, hour):

    salon_info = Salon.objects.get(pk=salon_id)
    service = Service.objects.get(pk=service_id)
    employee = Employee.objects.get(pk=employee_id)
    client = User.objects.get(pk=request.user.id)


    appointment = Appointment(date=date, hour=hour,
                              employee=employee,
                              salon=salon_info,
                              service=service,
                              client=client)

    appointment.save()


    return render(request, 'appointment_success.html', {
        'salon': salon_info, 'service': service, 'employee': employee,
        'date': date, 'hour': hour
    })


def my_appointments(request):

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
            review.save()
            return redirect(reverse('salon', kwargs={'salon_id': appointment.salon.id}))
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form, 'appointment': appointment})

