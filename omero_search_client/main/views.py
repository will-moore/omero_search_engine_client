from . import main
from .forms import SearchFrom
from flask import render_template, request, jsonify
import requests
import json
from urllib.parse import quote
from omero_search_client.app_data import get_help_file_contenets
from omero_search_client import omero_client_app
from .utils import get_query_results, get_resources, get_resourcse_names_from_search_engine, determine_search_results_,search_values, search_key, get_restircted_search_terms
operator_choices=[("equals", "equals"), ("not_equals", "not equals"), ("contains", "contains")
        , ("not_contains", "not contains")]
                                        #("gt", ">"),("gte", ">="), ("lt", "<"),
                                        #         ("lte", "<=")]


@main.route('/builder',methods=['POST', 'GET'])
def use_builder_mode():
    #resources=get_resources("all")
    return render_template('query_builder.html')#, resources_data=resources,  operator_choices=operator_choices,task_id="None", mode="advanced")#container)

@main.route('/advanced',methods=['POST', 'GET'])
def use_advanced_mode():
    resources=get_resources("all")
    return render_template('main_page.html', resources_data=resources,  operator_choices=operator_choices,task_id="None", mode="advanced")#container)

@main.route('/',methods=['POST', 'GET'])
def index ():
    '''
    this uses the same template for the main mode
    may be it is needed to the main template to be more user friendly
    Returns:
    '''
    help_contents=get_help_file_contenets()
    resources=get_resources("searchterms")
    return render_template('main_page.html', resources_data=resources, search_engine_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_API"),  operator_choices=operator_choices,task_id="None", help_contents=help_contents,mode="usesearchterms")#container)

@main.route('/searchterms',methods=['POST', 'GET'])
def get_search_items():
    return jsonify(get_restircted_search_terms())

@main.route('/<resource>/getresourcenames/',methods=['POST', 'GET'])
def get_resourcse_names(resource):
    return jsonify(get_resourcse_names_from_search_engine(resource))

@main.route('/get_resources_keys/',methods=['POST', 'GET'])
def get_resourcses_keys():
    mode= request.args.get("mode")
    resources = get_resources(mode)
    return jsonify(resources)

@main.route('/get_values/',methods=['POST', 'GET'])
def get_resourcse_key():
    key = request.args.get("key")
    resource = request.args.get("resource")
    if not key:
        return jsonify([])
    if resource=="project" and key=="Name (IDR number)":
        project_names=get_resourcse_names_from_search_engine ("project")
        screen_names = get_resourcse_names_from_search_engine("screen")
        return jsonify (screen_names+project_names)
    else:
        search_engine_url="{base_url}api/v1/resources/{resource}".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource)
        url = search_engine_url + "/getannotationvalueskey/?key={key}".format(key=quote(key))
        resp = requests.get(url=url)
        results = resp.text
        values = json.loads(results)
        return jsonify(values)

@main.route('/submitquery/',methods=['POST', 'GET'])
def submit_query():
    query =json.loads(request.data)
    return jsonify(determine_search_results_(query))#

@main.route('/queryresults/',methods=['POST', 'GET'])
def queryresults():
    urls={"image":omero_client_app.config.get("IMAGE_URL"),
          "project":omero_client_app.config.get("PROJECT_ID")}

    task_id = request.args.get("task_id")
    resource=request.args.get("resource")
    return jsonify(get_query_results(task_id, resource))

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


@main.route('/searchusingvaluesonly/',methods=['POST', 'GET'])
def get_resourcse_using_values_only():
    value = request.args.get("value")
    return_attribute_value = request.args.get("return_attribute_value")
    resource = request.args.get("resource")
    if not value or not resource:
         return jsonify({"Error": "No value is provided"})
    return jsonify(search_values(resource,value,return_attribute_value))

@main.route('/searchforvaluesusingkey/',methods=['POST', 'GET'])
def get_values_using_values_using_key():
    key = request.args.get("key")
    resource = request.args.get("resource")
    return jsonify(search_key(resource, key))