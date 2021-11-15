import requests
import json
from omero_search_client import omero_client_app


def get_search_results(results, resource,columns_def):
    returned_results={}
    if len(results["results"])==0:
        returned_results["Error"]="Your query returns no results"
        return returned_results

    cols=["Id","Name"]
    values=[]

    urls = {"image": omero_client_app.config.get("IMAGE_URL"),
            "project": omero_client_app.config.get("PROJECT_ID")}
    extend_url=urls.get(resource)
    for item in results["results"]["results"]:
        value = {}
        values.append(value)
        value["Id"] = item["id"]
        if not extend_url:
            url_ = omero_client_app.config.get("RESOURCE_URL")
        else:
            url_ = extend_url + str(item["id"])
        value["url"] = url_

        value["Name"]=item.get("name")
        for k in item["key_values"]:
            if k['name'] not in cols:
                cols.append(k['name'])
            value[k["name"]]=k["value"]
    columns=[]
    for col in cols:
        columns.append({
            "id": col,
            "name": col,
            "field": col,
            "sortable": True
        })
    if not columns_def:
        columns_def = []
        for col in cols:
            columns_def.append({
                "field": col,
                "sortable": True,
                "width": 150,
            })

        columns_def.append({
            "field": "url",
            "sortable": True,
            "width": 150,
            "formatter": "urlFormatter",

        })
    else:
        for col_def in columns_def:
            if col_def["field"] not in cols:
                cols.append(col_def["field"])

    for val in values:
        if len(val)!=len(cols):
            for col in cols:
                if not val.get(col):
                    val[col]="NA"
    returned_results["columns"]=columns
    returned_results["columns_def"]=columns_def
    returned_results["values"]=values
    returned_results["server_query_time"]=results["server_query_time"]
    returned_results["query_details"]=results["query_details"]
    returned_results["bookmark"]=results["results"]["bookmark"]
    returned_results["page"] = results["results"]["page"]
    returned_results["size"] = results["results"]["size"]
    returned_results["total_pages"] = results["results"]["total_pages"]
    if len(values)<=results["results"]["size"]:
        returned_results["contains_all_results"]=True
    else:
        returned_results["contains_all_results"] = False
    returned_results["Error"]=results["Error"]

    return returned_results


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
        results = json.loads(res)
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
    return {"Status": status, "Results": mod_results, "filters": filters, "resource": resource, "error":Error,"server_query_time":server_query_time, "notice": notice}


def get_resources():
    url = "{base_url}api/v1/resources/all/getannotationkeys".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"))
    resources={}
    try:
        resp = requests.get(url=url)
        results = resp.text
        resources = json.loads(results)
        to_be_deleted = []
        for k, val in resources.items():
            if val:
                if len(val) == 0:
                    to_be_deleted.append(k)
                elif len(val) == 1:
                    if not val[0]:
                        to_be_deleted.append(k)
        for item in to_be_deleted:
            del resources[item]
    except Exception as e:
        omero_client_app.logger.info ("Error: "+ str(e))
    return resources