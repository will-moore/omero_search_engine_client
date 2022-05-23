
from django.http import HttpResponse
from django.shortcuts import render
import json

from .app_data import get_help_file_contenets
from . import search_engine_settings as settings

operator_choices=[("equals", "equals"), ("not_equals", "not equals"), ("contains", "contains")
        , ("not_contains", "not contains")]


def index(request, **kwargs):
    """
    Home page shows a list of groups OR a set of 'categories' from
    user-configured queries.
    """
    search_url = settings.SEARCH_ENGINE_URL
    if search_url is None:
        return HttpResponse("Need to set omero.web.searchengine.url")
    context = {
        "search_engine_url": settings.SEARCH_ENGINE_URL,
        "operator_choices": operator_choices,
        "task_id": "None",
        "help_contents": get_help_file_contenets(),
        "mode": "usesearchterms"
    }
    
    return render(request, "omero_search_engine_client/main_page.html", context)
