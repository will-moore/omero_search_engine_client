from pydantic_model_genrated_from_schema_ import Model

import sys
import logging
import json
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''
Check the organism collection for the idr project 501 which has been imported using search engine (import_idr_project.py) using the developed schema'''

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

valid_json_fn ="../test_data/orags_collections_project_501.json"

logging.info ("Loading the json for 501")
with open(valid_json_fn, 'r') as valid_json_f:
    org_501_json = json.loads(valid_json_f.read())
counter=0
for image_id, organism_data in org_501_json.items():
    counter+=1
    logging.info("%s/%s, checking image id: %s" % (counter, len(org_501_json), image_id))
    try:
        organism = Model(**organism_data)
        logging.info("Data is valid ")               
        #logging.info(organism.Organism)
        #logging.info(repr(organism.Organism_Part.Organism_Part_Identifier))
        #logging.info(organism.Organism_Part)
        #logging.info(organism.dict())
    except ValueError as e:
        logging.info(organism.Organism) (e)
        logging.info(organism.dict())
        sys.exit()
