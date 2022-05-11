from . import views
from django.conf.urls import url

urlpatterns = [

    # index 'home page' of the app
    url(r'^$', views.index, name='omero_search_engine_client'),
]
