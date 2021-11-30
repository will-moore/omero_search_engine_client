from jsonschema import validate, ValidationError, SchemaError, RefResolver
import json
from os.path import abspath
import logging
from pathlib import Path
import sys
from app_client_scripts.organism_validation.jsonschema.utils.utils import add_local_schemas_to

'''
Check the organism collection for the idr project 501 which has been imported using search engine (import_idr_project.py) using the developed schema'''

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

organism_schema = "../schema/organism_schema.json"
valid_json_fn ="../test_data/orags_collections_project_501.json"
base_uri = 'file:' + abspath('') + '/'
logging.info ("BASE URL: %s"%base_uri)

with open(organism_schema, 'r') as schema_f:
    schema = json.loads(schema_f.read())

logging.info ("Loading the json for 501")
with open(valid_json_fn, 'r') as valid_json_f:
    org_501_json = json.loads(valid_json_f.read())

counter=0

resolver = RefResolver(referrer=schema, base_uri=base_uri)
schema_folder = Path('../schema')
add_local_schemas_to(resolver, schema_folder, base_uri)

no_errors=0
ids=[]
import sys
for image_id, org_json in org_501_json.items():
    if image_id not in ids:
        ids.append(image_id)
    else:
        logging.info ("Errors, the image is here twice, please check")
        sys.exit()
    counter+=1
    logging.info ("%s/%s, Checking image id: %s"%(counter,len(org_501_json),image_id))
    try :
        validate(org_json, schema, resolver=resolver)
        logging.info("Data is valid")
    except SchemaError as e :
        no_errors+=1
        logging.info("there is a schema error")
        logging.info(e.message)
    except ValidationError as e :
        no_errors += 1
        logging.info("there is a validation error")
        logging.info(e.message)

logging.info ("number of errors: %s"%no_errors)