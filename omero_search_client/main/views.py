from . import main
from .forms import SearchFrom
from flask import render_template, request
import requests
import json
from urllib.parse import quote
from omero_search_client import omero_client_app
from .utils import get_query_results, get_resources, process_search_results, determine_search_results

operator_choices=[("equals", "equals"), ("not_equals", "not equals"), ("contains", "contains")
        , ("not_contains", "not contains"),
                                        ("gt", ">"),("gte", ">="), ("lt", "<"),
                                                 ("lte", "<=")]

@main.route('/',methods=['POST', 'GET'])
def index():
    resources=get_resources()

    return render_template('main_page.html', resources_data=resources,  operator_choices=operator_choices,task_id="None")#container)

@main.route('/<resource>/get_values/',methods=['POST', 'GET'])
def get_resourcse_key(resource):
    key = request.args.get("key")
    if not key:
        return json.dumps([])
    search_engine_url="{base_url}api/v1/resources/{resource}".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource)
    url = search_engine_url + "/getannotationvalueskey/?key={key}".format(key=quote(key))
    resp = requests.get(url=url)
    results = resp.text
    values = json.loads(results)
    return json.dumps(values)

@main.route('/submitquery/',methods=['POST', 'GET'])
def submit_query():
    query =json.loads(request.data)
    return determine_search_results(query)


@main.route('/queryresults/',methods=['POST', 'GET'])
def queryresults():
    urls={"iamge":omero_client_app.config.get("IMAGE_URL"),
          "project":omero_client_app.config.get("PROJECT_ID")}

    task_id = request.args.get("task_id")
    resource=request.args.get("resource")
    return json.dumps(get_query_results(task_id, resource))

@main.route('/getqueryresult/',methods=['POST', 'GET'])
def get_query_results_withGUI():
    task_id = request.args.get("task_id")
    resources = get_resources()
    form = SearchFrom()
    options = []
    for resource in resources.keys():
        options.append((resource, resource.capitalize()))
    form.resourcseFields.choices = options
    return render_template('main_page.html', resources_data=resources, form=form, task_id=task_id)#container)

