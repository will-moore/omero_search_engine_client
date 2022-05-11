
from django.shortcuts import render

from omeroweb.webclient.decorators import login_required

@login_required()
def index(request, **kwargs):

    return render(request, "omero_search_engine_client/main_page.html", {})
