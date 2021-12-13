import logging
import requests
import json
from datetime import datetime
import collections

# url to send the query
image_ext = "/resources/image/searchannotation/"
# url to get the next page for a query, bookmark is needed
image_page_ext = "/resources/image/searchannotation_page/"
# search engine url
base_url = "http://127.0.0.1:5577/api/v2/"
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''
This script imports the organism metadata for idr project 501 (using the search engine) and save them into a text file as a json 
'''


def query_the_search_ending(query, main_attributes):
    # create a dict whihc contains the query details
    query_data = {"query": {'query_details': query, "main_attributes": main_attributes}}
    query_data_json = json.dumps(query_data)
    res=None
    try:
        resp = requests.get(url="%s%s" % (base_url, image_ext), data=query_data_json)
        res = resp.text
        returned_results = json.loads(res)
    except Exception as ex:
        logging.info("Error: ", ex)
        logging.info("Error: ", res)
        return None, None

    server_query_time = returned_results["server_query_time"]

    if not returned_results.get("results"):
        logging.info("no results, servre respond: %s" % returned_results)
        return None, server_query_time

    elif len(returned_results["results"]) == 0:
        logging.info("Your query returns no results")
        return [], server_query_time

    logging.info("Query results:")
    total_results = returned_results["results"]["size"]
    logging.info("Total no of result records %s" % total_results)

    logging.info("Server query time: %s seconds" % server_query_time)
    logging.info("Included results in the current page %s" % len(returned_results["results"]["results"]))

    recieved_results_data = []
    for res in returned_results["results"]["results"]:
        recieved_results_data.append(res)

    recieved_results = len(returned_results["results"]["results"])

    bookmark = returned_results["results"]["bookmark"]
    # print ("Bookmark for the next page, if any %s"%bookmark)
    total_pages = returned_results["results"]["total_pages"]
    page = 1
    logging.info("bookmark: %s, page: %s, received results: %s" % (
        bookmark, (str(page) + "/" + str(total_pages)), (str(recieved_results) + "/" + str(total_results))))
    # in case of the results in more than one page, it will iterate to fetch all the results.
    # return recieved_results_data, server_query_time

    while recieved_results < total_results:
        page += 1
        query_data = {"query": {'query_details': returned_results["query_details"]}, "bookmark": bookmark}
        query_data_json = json.dumps(query_data)
        resp = requests.get(url="%s%s" % (base_url, image_page_ext), data=query_data_json)
        res = resp.text
        returned_results = json.loads(res)
        bookmark = returned_results["results"]["bookmark"]
        recieved_results = recieved_results + len(returned_results["results"]["results"])
        for res in returned_results["results"]["results"]:
            recieved_results_data.append(res)

        logging.info("bookmark: %s, page: %s, received results: %s" % (
            bookmark, (str(page) + "/" + str(total_pages)), (str(recieved_results) + "/" + str(total_results))))

    logging.info("Total received results: %s" % len(recieved_results_data))
    return recieved_results_data, server_query_time


images_metadata_collection = {}

start = datetime.now()
meta_data_query = {"or_filters": [], "and_filters": []}

# Limit the search to search only the project which its id is 1104
main_attributes_query = {"and_main_attributes":[{"name": "project_id", "value": 501, "operator": "equals"}]}

logging.info("Sending the query:")
search_results, server_query_time = query_the_search_ending(meta_data_query, main_attributes_query)
projects_ids = []
organisms = {}
organism = "Organism"
organism_part = "Organism Part"
organism_part_identifier = "Organism Part Identifier"
orgs_grp = [organism, organism_part, organism_part_identifier]
counter = 0


def get_organism(key_values, image_id):
    counter = +1
    logging.info("Process: %s" % counter)

    image_org = {}
    orgs_dict = {}
    # organism[image_id] = orgs
    for k in key_values:
        if k["name"] in orgs_grp:
            orgs_dict[k['index']] = k
    orgs_dict = collections.OrderedDict(sorted(orgs_dict.items()))
    index = list(orgs_dict.keys())
    no_parts = int((len(orgs_dict) - 1) / 2)
    print("Number of parts: ", no_parts)
    if no_parts == 0:
        return
    image_org[organism] = orgs_dict[index[0]]['value']
    orgs_parts = []
    image_org[organism_part] = orgs_parts
    for i in range(1, len(index) - no_parts):
        single_part = {}
        single_part[organism_part] = orgs_dict[index[i]]["value"]
        single_part[organism_part_identifier] = orgs_dict[index[i + no_parts]]["value"]
        orgs_parts.append(single_part)
    images_metadata_collection[image_id] = image_org


if search_results:
    logging.info(search_results[0].keys())
    logging.info("Total processing time %s seconds" % (datetime.now() - start).total_seconds())
    logging.info("server query time in second %s (Actual search time at the search engine side) " % server_query_time)
    server_query_time
    logging.info(len(projects_ids))
    logging.info("organisms: %s" % organisms)

    with open("test_data/orags_collections_project_501.txt", 'w') as outfile:
        json.dump(images_metadata_collection, outfile)



