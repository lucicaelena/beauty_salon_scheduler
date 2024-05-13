from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('salon/<int:salon_id>', views.salon, name='salon'),
    path('salon/<int:salon_id>/service/<int:service_id>/', views.select_employee, name='select_employee'),
    path('salon/<int:salon_id>/service/<int:service_id>/employee/<int:employee_id>', views.select_date,name='select_date'),
    path('salon/<int:salon_id>/service/<int:service_id>/employee/<int:employee_id>/date/<str:date>',views.select_hour,name='select_hour'),
    path('salon/<int:salon_id>/service/<int:service_id>/employee/<int:employee_id>/date/<str:date>/hour/<str:hour>',
         views.add_appointment, name='add-appointment'),
    path('appointments', views.my_appointments, name='appointments'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('cancel_appointment/<int:appointment_id>/',views.cancel_appointment,name='cancel_appointment'),
    path('review/<int:appointment_id>/', views.review, name='review')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)