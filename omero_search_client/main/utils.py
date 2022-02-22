import requests
import json
import os

from omero_search_client import omero_client_app

mapping_names={"project":{"Name (IDR number)":"name"}}

def divide_filter(filters):
    filters_resources={}
    for filer in filters:
        if filer["resource"] not in filters_resources:
            filters_resources[filer["resource"]] = []
        res_and_filter = filters_resources[filer["resource"]]
        res_and_filter.append(filer)
    return filters_resources

def analyize_query(query):
    all_main_attributes={}
    and_filters=query.get("query_details").get("and_filters")
    or_filters = query.get("query_details").get("or_filters")
    and_filters_resources= {}
    or_filters_resources= {}
    if and_filters and  len(and_filters)>0:
        and_filters_resources = divide_filter(and_filters)
    if or_filters and len(or_filters)>0:
        or_filters_resources = divide_filter(or_filters)
    queries_to_send={}
    or_aded=[]
    for key, item in and_filters_resources.items():
        qu={"and_filters":item}
        queries_to_send[key]=qu
        if key in or_filters_resources:
            or_aded.append(key)
            qu["or_filters"]=or_filters_resources[key]

    if len(or_aded) !=or_filters_resources and len(or_filters_resources)>0:
        for key, item in or_filters_resources.items()   :
            if key in or_aded:
                continue
            queries_to_send[key]={"or_filters":item}
    main_attributes={}
    for k, qu in queries_to_send.items():
        if qu.get("and_filters") and len(qu.get("and_filters")):
            and_main_filter=check_filter_for_main_attributes(qu.get("and_filters"))
            if len(and_main_filter)>0:
                main_attributes["and_main_attributes"]=and_main_filter

        if qu.get("or_filters") and len(qu.get("or_filters")):
            or_main_filter=check_filter_for_main_attributes(qu.get("or_filters"))
            if len(or_main_filter)>0:
                main_attributes["or_main_attributes"] = or_main_filter
        if len(main_attributes)>0:
            all_main_attributes[k]=main_attributes
    return queries_to_send, all_main_attributes

def check_filter_for_main_attributes(filters):
    '''
    check for main attributes e.g. name
    Args:
        filters:
    Returns:
        main attributes and modify the filters accordingly

    '''
    main_filter=[]
    for filter in filters:
        resource=filter["resource"]
        if resource in mapping_names :
            if mapping_names[resource].get(filter["name"]):
                main_filter.append(filter)
                filter["name"]=mapping_names[resource].get(filter["name"])
    for s_filter in main_filter:
        filters.remove(s_filter)
    return main_filter

def seracrh_query(query,resource,bookmark,raw_elasticsearch_query, main_attributes=None):
    omero_client_app.logger.info(("%s, %s") % (resource, query))
    if not main_attributes:
        q_data = {"query": {'query_details': query}}
    elif resource=="image":
        q_data = {"query": {'query_details': query,"main_attributes":   main_attributes}}
    else:
        q_data = {"query": {'query_details': query, "main_attributes": main_attributes}}
    try:
        if bookmark:
            q_data["bookmark"] =bookmark
            q_data["raw_elasticsearch_query"] = raw_elasticsearch_query
            resource_ext = "{base_url}api/v2/resources/{res_table}/searchannotation_page/".format(
                base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), res_table=resource)
        else:
            resource_ext = "{base_url}api/v2/resources/{res_table}/searchannotation/".format(
                base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), res_table=resource)
        aa = json.dumps(q_data)
        resp = requests.get(resource_ext, data=aa)
        res = resp.text
        ress = json.loads(res)
        ress["Error"] = "none"
        return ress
    except Exception as ex:
        omero_client_app.logger.info("Error: " + str(ex))
        return {"Error": "Something went wrong, please try later"}


def get_ids(results, resource):
    ids=[]
    for item in results["results"]["results"]:
        qur_item={}
        ids.append(qur_item)
        qur_item["name"]="{resource}_id".format(resource=resource)
        qur_item["value"]=item["id"]
        qur_item["operator"]="equals"
    return ids

def determine_search_results(query_):
    '''
    Args:
        query_: a list contains quries to send to the database, each nelong to one resource
        if it is one query it will send the results back
        otherwise it will query non image resources and use the results to return the images whihc satisfy the query
        results an dthe image results
    Returns:

    '''
    if query_.get("query_details"):
        case_sensitive=query_.get("query_details").get("case_sensitive")
    else:
        case_sensitive =None
    mode=query_.get("mode")
    bookmark=query_.get("bookmark")
    raw_elasticsearch_query=query_.get("raw_elasticsearch_query")
    queries_to_send,all_main_attributes=analyize_query(query_)
    image_query= {}
    other_image_query=[]
    for resource, query in queries_to_send.items():
        if resource == "image" and len(queries_to_send)>1:
            image_query = query
            continue
        query["case_sensitive"]=case_sensitive
        res= seracrh_query(query, resource, bookmark ,raw_elasticsearch_query, all_main_attributes.get(resource))
        if res.get("error"):
            return json.dumps(res)
        if not res.get("results") or len(res["results"]) == 0:
            res["Error"] = "Your query returns no results"
            return res
        if len (queries_to_send)==1:
            columns_def = query.get("columns_def")
            return json.dumps(process_search_results(res, resource, columns_def, mode))
        else:

            other_image_query+=get_ids(res, resource)

    other_image_query={"or_main_attributes":other_image_query}
    image_query["case_sensitive"]=case_sensitive
    ress=seracrh_query(image_query, "image",bookmark, raw_elasticsearch_query,other_image_query)
    columns_def = image_query.get("columns_def")
    return json.dumps(process_search_results(ress, "image", columns_def,mode))

def process_search_results(results, resource, columns_def, mode):
    returned_results={}
    if not results.get("results") or len(results["results"])==0:
        returned_results["Error"] = "Your query returns no results"
        return returned_results

    cols=[]

    values=[]

    urls = {"image": omero_client_app.config.get("IMAGE_URL"),
            "project": omero_client_app.config.get("PROJECT_URL")}
    extend_url=urls.get(resource)
    if not extend_url:
        extend_url = omero_client_app.config.get("RESOURCE_URL")

    names_ids={}

    to_add = False

    for item in results["results"]["results"]:
        value = {}
        values.append(value)
        value["Id"] = item["id"]
        names_ids[value["Id"]]=item.get("name")
        #if not extend_url:
        #    url_ = omero_client_app.config.get("RESOURCE_URL")
        #else:
        #    url_ = extend_url + str(item["id"])
        #value["url"] = url_

        value["Name"]=item.get("name")
        value["Project name"] = item.get("project_name")
        if item.get("screen_name"):
            to_add=True
            value["Study name"] = item.get("screen_name")
        elif  item.get("project_name"):
            to_add=True
            value["Study name"] =  item.get("project_name")

        for k in item["key_values"]:
            if k['name'] not in cols:
                cols.append(k['name'])
            if value.get(k["name"]):
                value[k["name"]]=value[k["name"]]+"; "+ k["value"]
            else:
                value[k["name"]]=k["value"]

    columns=[]
    for col in cols:
        columns.append({
            "id": col,
            "name": col,
            "field": col,
            "sortable": True,
        })
    # to be used to rest
    searchtermcols = get_restircted_search_terms().get(resource)
    if not searchtermcols or len(searchtermcols)==0:
        mode="advanced"
    main_cols=[]
    if not columns_def:
        columns_def = []
        cols.sort()
        if resource == "image":
            cols.insert(0, "Study name")
            main_cols.append(("Study name"))
        cols.insert(0, "Name")
        main_cols.append(("Name"))
        cols.insert(0, "Id")
        main_cols.append(("Id"))

        for col in cols:
            if mode=="usesearchterms" and col not in main_cols:
                if col in searchtermcols:
                    columns_def.append({
                        "field": col,
                        "sortable": True,
                        #"width": 150,
                    })
            else:
                columns_def.append({
                    "field": col,
                    "sortable": True,
                    #"width": 150,
                })
    else:
        for col_def in columns_def:
            if col_def["field"] not in cols:
                if mode=="usesearchterms":
                    if col in searchtermcols:
                        cols.append(col_def["field"])
                else:
                    cols.append(col_def["field"])
    for val in values:
        if len(val)!=len(cols):
            for col in cols:
                if not val.get(col):
                    val[col]='""'
    returned_results["columns"]=columns
    returned_results["columns_def"]=columns_def
    returned_results["values"]=values
    returned_results["server_query_time"]=results["server_query_time"]
    returned_results["query_details"]=results["query_details"]
    returned_results["bookmark"]=results["results"]["bookmark"]
    returned_results["page"] = results["results"]["page"]
    returned_results["size"] = results["results"]["size"]
    returned_results["total_pages"] = results["results"]["total_pages"]
    returned_results["extend_url"]=extend_url
    returned_results["names_ids"]=names_ids
    returned_results["raw_elasticsearch_query"] = results["raw_elasticsearch_query"]
    if len(values)<=results["results"]["size"]:
        returned_results["contains_all_results"]=True
    else:
        returned_results["contains_all_results"] = False
    returned_results["Error"]=results["Error"]
    returned_results["resource"]=results["resource"]+"s"
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
    if mode == "searchterms":
        restricted_search_terms=get_restircted_search_terms()
        restircted_resources={}
    url = "{base_url}api/v1/resources/all/getannotationkeys".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"))
    resources={}
    try:
        resp = requests.get(url=url)
        results = resp.text
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

    if mode=="searchterms":
        return restircted_resources
    else:
        return resources