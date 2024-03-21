from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('salon/<int:salon_id>', views.salon, name='salon'),
    path('salon/<int:salon_id>/service/<int:service_id>/', views.select_employee, name='select_employee'),
    path('salon/<int:salon_id>/service/<int:service_id>/employee/<int:employee_id>', views.select_date,name='select_date'),
    path('salon/<int:salon_id>/service/<int:service_id>/employee/<int:employee_id>/date/<str:date>',views.select_hour,name='select_hour')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)