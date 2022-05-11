
from django.shortcuts import render

import json
# from . import main
from .app_data import get_help_file_contenets
# from omero_search_client import omero_client_app
operator_choices=[("equals", "equals"), ("not_equals", "not equals"), ("contains", "contains")
        , ("not_contains", "not contains")]

def index(request, **kwargs):
    """
    Home page shows a list of groups OR a set of 'categories' from
    user-configured queries.
    """
    context = {
        "search_engine_url": "https://idr-testing.openmicroscopy.org/searchengineapi/api/v1/resources",
        "operator_choices": json.dumps(operator_choices),
        "task_id": "None",
        "help_contents": get_help_file_contenets(),
        "mode": "usesearchterms"
    }
    
    return render(request, "omero_search_engine_client/main_page.html", context)
