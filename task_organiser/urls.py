"""
URL configuration for task_organiser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import include, handler404, handler500, handler400
from django.http import HttpResponse, HttpResponseNotFound
from django.conf.urls import include
import json
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('maiora/', include('task_app.urls')),
]

def page_not_found(request, *args, **kwargs):
    # logging.error("within page_not found method request of sahyadri_oms api:{}".format(request))
    return HttpResponseNotFound(json.dumps({'error': 'Not Found',"message": "Requested path not available",'path':request.get_full_path()}),content_type='application/json', status=404)

def server_error(request, *args, **kwargs):
    # logging.error("within server_error method request of sahyadri_oms api:{}".format(request))
    return HttpResponse(json.dumps({'error': 'Some Error Occured in Processing',"message": "Please try again after some time"}),content_type='application/json',status=500)

def bad_request(request, *args, **kwargs):
    # logging.error("within bad_request method request of sahyadri_oms api:{}".format(request))
    return HttpResponseNotFound(json.dumps({'error': 'Bad request',"message": "The request was not well formatted or you are sending wrong data",'path':request.get_full_path()}),content_type='application/json', status=400)

handler404 = page_not_found
handler500 = server_error
handler400 = bad_request