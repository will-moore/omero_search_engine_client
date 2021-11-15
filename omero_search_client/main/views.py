from . import main
from .forms import SearchFrom
from flask import render_template, request
import requests
import json
from omero_search_client import omero_client_app
from .utils import get_query_results, get_resources,get_search_results

@main.route('/',methods=['POST', 'GET'])
def index():
    resources=get_resources()
    form = SearchFrom()
    options = []
    for resource in resources.keys():
        options.append((resource, resource.capitalize()))
    form.resourcseFields.choices=options
    return render_template('main_page.html', resources_data=resources, form=form, task_id="None")#container)

@main.route('/<resource>/get_values/',methods=['POST', 'GET'])
def get_resourcse_key(resource):
    key = request.args.get("key")
    if not key:
        return json.dumps([])
    search_engine_url="{base_url}api/v1/resources/{resource}".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource)
    url = search_engine_url + "/getannotationvalueskey/?key={key}".format(key=key)
    resp = requests.get(url=url)
    results = resp.text
    values = json.loads(results)
    return json.dumps(values)

@main.route('/submitquery/',methods=['POST', 'GET'])
def submit_query():
    query =json.loads(request.data)
    omero_client_app.logger.info (query.get("query_details"))
    q_data = {"query": {'query_details': query.get("query_details")}}

    try:
        if query.get("bookmark"):
            q_data["bookmark"]=query["bookmark"]
            resource_ext = "{base_url}api/v2/resources/{res_table}/searchannotation_page/".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"),res_table=query.get("resource"))
        else:
            resource_ext = "{base_url}api/v2/resources/{res_table}/searchannotation/".format(
                base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), res_table=query.get("resource"))
        aa = json.dumps(q_data)
        resp = requests.get(resource_ext, data=aa)
        res = resp.text
        ress = json.loads(res)
        ress["Error"]= "none"
        columns_def= query.get("columns_def")
        return json.dumps(get_search_results(ress,query.get("resource"),columns_def))
    except Exception as ex:
        omero_client_app.logger.info ("Error: "+ str(ex))
        return json.dumps({"Error": "Something went wrong, please try later" })

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

