import requests
import json
import os
from omero_search_client import omero_client_app
import operator

mapping_names={"project":{"Name (IDR number)":"name"},"screen":{"Name (IDR number)":"name"}}

def get_resourcse_names_from_search_engine(resource, ):
    search_engine_url="{base_url}api/v1/resources/{resource}".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource)
    url = search_engine_url + "/names/"
    resp = requests.get(url=url)
    results = resp.text
    try:
        values = json.loads(results)
    except Exception as e:
        omero_client_app.logger.info("Request text: %s, Error: %s" % (results, e))
        return {"error":"Something went wrong, please try again later"}

    return values

def set_returned_results_for_all(results_,return_attribute_value):
    '''
    Used in case of searching all resources using value to find attributes, and values
    the search engine returns dict contains the close matching attributes for the provided values for each resourse
    Args:
        results_: the returned results from the searchengine
        return_attribute_value:

    Returns:

    '''
    if "notice" in results_:
        if results_["notice"].get("Error"):
            return {"Error": results_["notice"].get("Error")}
    if (return_attribute_value):
        for ress,results__ in results_.items():
            results = results__.get("data")
            results.sort(key=operator.itemgetter('Number of %s'%ress+'s'), reverse=True)
            returned_values = []
            co = 0
            added_attrs=[]
            for res in results:
                co += 1
                if res["Attribute"]  in added_attrs:
                    continue
                added_attrs.append(["Attribute"])
                atr_val = "Attribute: " + res["Attribute"] + ", Value:" + res["Value"]
                returned_values.append((atr_val))
        return returned_values
    col_def=[]
    all_results=[]
    total_number_results=0
    no_buckets=0
    for ress, results__ in results_.items():
        total_number = results__.get("total_number")
        results = results__.get("data")
        if total_number==0:
            continue
        for res in results:
            res["Resource"]=ress
        all_results += results
        no_buckets+=len(results)
        total_number_results+=total_number
        results.sort(key=operator.itemgetter('Number of %s' % ress + 's'), reverse=True)
        if len(results)>0 and len (col_def)==0:
            last_colm=''
            for item in results [0]:
                if "Number of" in item:
                    last_colm=item
                    continue
                col={}
                col_def.append(col)
                if item == "Key":
                    col["field"] = "Attribute"
                else:
                    col["field"]=item
                col["sortable"]= True
            if last_colm:
                col={}
                col_def.append(col)
                col["field"] = last_colm
                col["sortable"] = True
        for res in results:
            res["Attribute"] = res["Key"]
    return {"columnDefs": col_def, "results": all_results, "total_number":total_number_results, "no_buckets":no_buckets}

def search_values(resource, value,return_attribute_value=False):
    url="{base_url}api/v1/resources/{resource}/searchvalues/?value={value}".format( base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource, value=value)


    resp = requests.get(url=url)
    results_ = resp.text
    try:
        all_results = json.loads(results_)
    except Exception as e:
        omero_client_app.logger.info("Request text: %s, Error: %s"%(results_,e))
        return {"error": "Something went wrong, please try again later"}
    if resource=="all":
        return set_returned_results_for_all(all_results,return_attribute_value)
    results = all_results.get("data")
    for re in results:
        if "Number of images" not in re:
            print ("Error: ", re)
    results.sort(key=operator.itemgetter('Number of images'), reverse=True)
    total_number = all_results.get("total_number")
    if return_attribute_value:
        returned_values=[]
        co=0
        for res in results:
            co+=1
            atr_val="Attribute: "+res["Attribute"]+", Value:"+res["Value"]
            returned_values.append((atr_val))
        return returned_values
    col_def = []
    if len(results)>0:
        last_colm=''
        for item in results [0]:
            if "Number of" in item:
                last_colm = item
                continue
            col={}
            col_def.append(col)
            if item=="Key":
                col["field"] = "Attribute"
            else:
                col["field"]=item
            col["sortable"]= True
        if last_colm:
            col = {}
            col_def.append(col)
            col["field"] = last_colm
            col["sortable"] = True
        for res in results:
            res["Attribute"]=res["Key"]
    return {"columnDefs": col_def, "results": results, "total_number":total_number, "no_buckets":len(results)}

def search_key(resource, key):
    url = "{base_url}api/v1/resources/{resource}/searchvaluesusingkey/?key={key}".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource, key=key)
    resp = requests.get(url=url)
    results_ = resp.text
    try:
        all_results = json.loads(results_)
    except Exception as e:
        omero_client_app.logger.info("Request text: %s, Error: %s" % (results_, e))
        return {"error":"Something went wrong, please try again later"}
    results=all_results.get("data")
    total_number=all_results.get("total_number")
    total_number_of_images=all_results.get("total_items")
    total_number_of_buckets=all_results.get("total_number_of_buckets")
    col_def = []
    if results and len(results) > 0:
        last_colm = ''
        for item in results[0]:
            if "Number of" in item:
                last_colm = item
                continue
            col = {}
            col_def.append(col)

            if item=="Key":
                col["field"] = "Attribute"
            else:
                col["field"] = item
            col["sortable"] = True
        if last_colm:
            col = {}
            col_def.append(col)
            col["field"] = last_colm
            col["sortable"] = True
    for res in results:
        res["Attribute"]=res["Key"]

    return {"columnDefs": col_def, "results": results, "total_number": total_number,  "no_buckets":len(results),"total_number_of_images":total_number_of_images, "total_number_of_buckets":total_number_of_buckets}

def determine_search_results_(query_):
    resource_ext = "{base_url}api/v1/resources/submitquery/?return_columns={return_columns}".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"),return_columns=True)
    aa = json.dumps(query_)
    res = requests.post(resource_ext, data=aa)
    mode = query_.get("mode")
    columns_def = query_.get("columns_def")
    res = res.text
    try:
        ress = json.loads(res)
    except Exception as e:
        omero_client_app.logger.info("Request text: %s, Error: %s" % (res, e))
        ress= {"Error": "Something went wrong, please try again later"}
    if ress.get("columns_def"):
        hide_column_not_in_searchterms(ress.get("columns_def"), mode)
    return ress

def hide_column_not_in_searchterms(columns_def, mode):
    main_cols=["Id", "Name", "Study name"]
    searchtermcols = get_restircted_search_terms().get("image")
    for column in columns_def:
        if column["field"] in searchtermcols or column["field"]  in main_cols:
            hide = False
        else:
            hide = True
        column["hide"]=hide

def get_query_results(task_id, resource=None):
    mod_results = []
    filters = []
    status="None"
    Error="None"
    server_query_time=0
    notice="None"
    try:
        urls={"image":omero_client_app.config.get("IMAGE_URL"),
              "project":omero_client_app.config.get("PROJECT_ID")}
        url_ = "{base_url}/searchresults/?task_id={task_id}".format(
            base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), task_id=task_id)
        resp = requests.get(url_)
        res = resp.text
        try:
            results = json.loads(res)
        except Exception as e:
            omero_client_app.logger.info("Request text: %s, Error: %s"%(results,e))
            return {"error ":"Something went wrong, please try again later"}


        omero_client_app.logger.info("keys is: "+ str( results.keys()))
        status = results.get("Status")
        omero_client_app.logger.info (status)
        res = results.get("Results")
        if status=="FAILURE":
            omero_client_app.logger.info ("RESP: "+ str(resp))
        if res and status!="FAILURE":
            omero_client_app.logger.info("RESULT LENGTH IS:"+ str( len(res)))
            omero_client_app.logger.info(res.get("query_details"))

        if res and status=="SUCCESS":
            filters = res.get("query_details")
            notice=res.get("notice")
            server_query_time=res.get("server_query_time")
            resource = res.get("resource")
            extend_url = urls.get(resource)
            for key, val in res.get("results").items():
                val["id"] = key
                if not extend_url:
                    url_=omero_client_app.config.get("RESOURCE_URL")
                else:
                    url_ = extend_url + str(val["id"])
                val["url"] = url_
                mod_results.append(val)
    except Exception as e:
        omero_client_app.logger.info("Error ..."+ str(e))  # , type(res["image"]), res.keys())
        Error="Something went wrong, please try again later"
    omero_client_app.logger.info("Modified RESULT LENGTH IS:"+ str(len(mod_results)))
    omero_client_app.logger.info("Ststus: "+ status)
    return {"Status": status, "Results": mod_results, "filters": filters, "resource": resource, "error":Error,"server_query_time":server_query_time, "extend_url":extend_url,"notice": notice}

def get_restircted_search_terms():
    '''
    The json file is saved in app data folder, it contains the search terms for each resource
    this allows the admin to add or remove item/s without changing the code
    Returns: a dict contains the search terms
    '''
    search_terms=os.path.join(omero_client_app.config.get("APP_DATA_FOLDER"),"restricted_search_terms.json")

    if not os.path.isfile(search_terms):
        return {}
    with open(search_terms) as json_file:
        restricted_search_terms = json.load(json_file)
    return restricted_search_terms

def get_resources(mode):
    restricted_search_terms=None
    if mode == "searchterms":
        restricted_search_terms=get_restircted_search_terms()
        restircted_resources={}
    url = "{base_url}api/v1/resources/all/keys/".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"))
    resources={}
    try:
        resp = requests.get(url=url)
        results = resp.text
        print (results)
        resources = json.loads(results)
        to_be_deleted = []


        for k, val in resources.items():
            if val and len(val)>0 :
                if len(val) == 0:
                    to_be_deleted.append(k)
                elif len(val) == 1:
                    if not val[0]:
                        to_be_deleted.append(k)
        for item in to_be_deleted:
            del resources[item]
        if not restricted_search_terms or len(restricted_search_terms)==0:
            mode="advanced"

        if mode == "searchterms":
            for k, val in resources.items():
                if k in restricted_search_terms:
                    search_terms = list(set(restricted_search_terms[k]) & set(val))
                    if len(search_terms) > 0:
                        restircted_resources[k] = search_terms
                resources=restircted_resources

        if "project" in resources:
            resources["project"].append("Name (IDR number)")
    except Exception as e:
        omero_client_app.logger.info ("Error: "+ str(e))
        resources["error"]="Something went wrong, please try again later"
        return (resources)

    if mode=="searchterms":
        return restircted_resources
    else:
        return resources


#https://idr.openmicroscopy.org/webclient/?show=screen-2151