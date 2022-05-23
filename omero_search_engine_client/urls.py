from django.conf.urls import url

from . import views

urlpatterns = [
    # index 'home page' of the omero_search_ening_client app
    url(r'^$', views.index, name='omero_search_ening_client'),
]
