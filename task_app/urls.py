from django.urls import path 
from .views import *
from .managers import *
from task_organiser.settings import STATIC_URL
from django.conf.urls.static import static

urlpatterns = [
    path('task_organiser', task_organiser),
    path('company_details',company_details)


]



