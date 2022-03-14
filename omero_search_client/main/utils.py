import copy

import requests
import json
import os

from omero_search_client import omero_client_app

mapping_names={"project":{"Name (IDR number)":"name"},"screen":{"Name (IDR number)":"name"}}


def get_resourcse_names_from_search_engine(resource):
    search_engine_url="{base_url}api/v1/resources/{resource}".format(base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource)
    url = search_engine_url + "/getresourcenames/"
    resp = requests.get(url=url)
    results = resp.text
    values = json.loads(results)
    return values

def search_values(resource, value):
    url="{base_url}api/v2/resources/{resource}/searchvalues/?value={value}".format( base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource, value=value)
    resp = requests.get(url=url)
    results_ = resp.text
    all_results = json.loads(results_)
    results = all_results.get("returnted_results")
    total_number = all_results.get("total_number")

    col_def = []
    if len(results)>0:
        for item in results [0]:
            col={}
            col_def.append(col)
            col["field"]=item
            col["sortable"]= True
    return {"columnDefs": col_def, "results": results, "total_number":total_number, "no_buckets":len(results)}

def search_key(resource, key):
    url = "{base_url}api/v2/resources/{resource}/searchvaluesusingkey/?key={key}".format(
        base_url=omero_client_app.config.get("OMERO_SEARCH_ENGINE_BASE_URL"), resource=resource, key=key)
    resp = requests.get(url=url)
    results_ = resp.text
    all_results = json.loads(results_)
    results=all_results.get("returnted_results")
    total_number=all_results.get("total_number")

    col_def = []
    if results and len(results) > 0:
        for item in results[0]:
            col = {}
            col_def.append(col)
            col["field"] = item
            col["sortable"] = True
    return {"columnDefs": col_def, "results": results, "total_number": total_number,  "no_buckets":len(results)}

class QueryItem (object):
    def __init__ (self, filter):
        '''
        define query and adjust resource if it is needed
        Args:
            resource:
            attribute_name:
            attribute_value:
            operator:
        '''
        self.resource=filter.get("resource")
        self.name=filter.get("name")
        self.value=filter.get("value")
        self.operator=filter.get("operator")
        self.query_type="keyvalue"
        self.adjust_resource()
        #it will be used when buildingthe query

    def adjust_resource(self):
        if self.resource in mapping_names :
            if mapping_names[self.resource].get(self.name):
                pr_names=get_resourcse_names_from_search_engine(self.resource)
                if not self.value in pr_names:
                    ##Assuming that the names is either project or screen
                    self.resource="screen"
                self.name=mapping_names[self.resource].get(self.name)
                self.query_type="main_attribute"

class QueryGroup(object):
    '''
    check query list and check it is has  multiple resource queries
    '''
    def __init__ (self, group_type):
        self.query_list=[]
        self.group_type = group_type
        self.resourses_query = {}
        self.main_attribute={}
        self.resource=[]

    def add_query(self,query):
        self.query_list.append(query)

    def divide_filter(self):
        for filter in self.query_list:
            if not filter.resource in self.resourses_query:
                flist=[]
                self.resourses_query[filter.resource]=flist
            else:
                flist=self.resourses_query[filter.resource]
            flist.append(filter)
            self.resource=self.resourses_query.keys()

    def adjust_query_main_attributes(self):
        to_be_removed=[]
        for resource, queries in self.resourses_query.items():
            for query in queries:
                if query.query_type=="main_attribute":
                    if not resource in self.main_attribute:
                        self.main_attribute[resource]={"and_main_attributes":query}
                    else:
                        self.main_attribute[resource]["and_main_attributes"].append(query)
                    to_be_removed.append(query)
            for qu in to_be_removed:
                queries.remove(qu)

class QueryRunner(object, ):
    def __init__(self,and_query_group,  or_query_group, case_sensitive, mode, bookmark, raw_elasticsearch_query,columns_def):
        self.or_query_group=or_query_group
        self.and_query_group=and_query_group
        self.case_sensitive=case_sensitive
        self.mode=mode
        self.bookmark=bookmark
        self.raw_elasticsearch_query=raw_elasticsearch_query
        self.image_query={}
        self.additional_image_conds=[]
        self.columns_def=columns_def

    def get_iameg_non_image_query(self):
        res=None
        for resource, and_query in self.and_query_group.resourses_query.items():
            if resource=="image":
                or_queries=[]
                self.image_query["and_filters"]=and_query
                self.image_query["or_filters"] = or_queries
                if self.and_query_group.main_attribute.get(resource):
                    self.image_query["main_attribute"]=self.and_query_group.main_attribute.get(resource)
                else:
                    self.image_query["main_attribute"] =[]
                for or_grp in self.or_query_group:
                    if resource in or_grp.resourses_query:
                        or_queries.append(or_grp.resourses_query[resource])
            else:
                query={}
                query["and_filters"]=and_query
                or_queries = []
                query["or_filters"] = or_queries
                for or_grp in self.or_query_group:
                    if resource in or_grp:
                        or_queries.append(or_grp["image"])
                if self.and_query_group.main_attribute.get(resource):
                    query["main_attribute"]=self.and_query_group.main_attribute.get(resource)
                else:
                    query["main_attribute"]= {}
                res=self.run_query(query, resource)
                new_cond=get_ids(res, resource)
                if new_cond:
                    self.additional_image_conds+=new_cond

        self.image_query["main_attribute"]={"or_main_attributes": self.additional_image_conds}

        return  self.run_query(self.image_query, "image")

    def run_query(self, query_, resource):
        main_attributes= {}
        query={"and_filters":[],"or_filters":[]}

        if query_.get("and_filters"):
            for qu in query_.get("and_filters"):
                query.get("and_filters").append(qu.__dict__)

        if query_.get("or_filters"):
            for qu_ in query_.get("or_filters"):
                qq=[]
                query.get("or_filters").append(qq)
                for qu in qu_:
                    qq.append(qu.__dict__)

        if query_.get("main_attribute"):
            ss=[]
            #this should be checked again ........
            for key, qu in query_.get("main_attribute").items():
                if type(qu)!=list:
                    ss.append(qu.__dict__)
                else:
                    for qu_ in qu:
                        ss.append(qu_.__dict__)
            main_attributes[key]=ss
        res=seracrh_query(query, resource, self.bookmark, self.raw_elasticsearch_query, main_attributes)

        if resource!="image":
            return res

        return json.dumps(process_search_results(res, "image",self.columns_def, self.mode))




def determine_search_results_(query_):
    if query_.get("query_details"):
        case_sensitive = query_.get("query_details").get("case_sensitive")
    else:
        case_sensitive = None
    mode = query_.get("mode")
    bookmark = query_.get("bookmark")
    raw_elasticsearch_query = query_.get("raw_elasticsearch_query")
    and_filters = query_.get("query_details").get("and_filters")
    or_filters = query_.get("query_details").get("or_filters")
    columns_def=query_.get("columns_def")
    and_query_group = QueryGroup("and_filters")
    or_query_groups = []
    if and_filters and len(and_filters) > 0:
        for filter in and_filters:
            and_query_group.add_query(QueryItem(filter))
        and_query_group.divide_filter()
        and_query_group.adjust_query_main_attributes()
    if or_filters and len(or_filters) > 0:
        for filters_ in or_filters:
            or_query_group = QueryGroup("or_filters")
            or_query_groups.append(or_query_group)
            inside_or_filter=[]
            for filter in filters_:
                or_query_group.add_query((QueryItem(filter)))
            or_query_group.divide_filter()
            or_query_group.adjust_query_main_attributes()
    query_runner=QueryRunner(and_query_group, or_query_groups, case_sensitive, mode, bookmark, raw_elasticsearch_query, columns_def)
    return(query_runner.get_iameg_non_image_query())


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
    if results.get("results") and results.get("results").get("results"):
        for item in results["results"]["results"]:
            qur_item={}
            #ids.append(qur_item)
            qur_item["name"]="{resource}_id".format(resource=resource)
            qur_item["value"]=item["id"]
            qur_item["operator"]="equals"
            qur_item["resource"] = resource
            qur_item_=QueryItem(qur_item)
            ids.append(qur_item_)
        return ids
    return None


def process_search_results(results, resource, columns_def, mode):
    returned_results={}
    if not results.get("results") or len(results["results"])==0:
        returned_results["Error"] = "Your query returns no results"
        return returned_results
    cols=[]
    values=[]
    urls = {"image": omero_client_app.config.get("IMAGE_URL"),
            "project": omero_client_app.config.get("PROJECT_URL"),
            "screen": omero_client_app.config.get("SCREEN_URL")}
    extend_url=urls.get(resource)
    if not extend_url:
        extend_url = omero_client_app.config.get("RESOURCE_URL")
    names_ids={}

    for item in results["results"]["results"]:
        value = {}
        values.append(value)
        value["Id"] = item["id"]
        names_ids[value["Id"]]=item.get("name")

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


#https://idr.openmicroscopy.org/webclient/?show=screen-2151