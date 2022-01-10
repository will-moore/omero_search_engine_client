from jsonschema import validate, ValidationError, SchemaError, RefResolver
import json
from os.path import abspath
import sys
from pathlib import Path
import logging
from app_client_scripts.organism_validation.jsonschema.utils.utils import add_local_schemas_to

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

organism_schema = "../schema/organism_schema.json"
valid_json_fn ="../test_data/valid_organism_2.json"#"valid_organism.json"
base_uri = 'file:' + abspath('') + '/'
with open(organism_schema, 'r') as schema_f:
    schema = json.loads(schema_f.read())

print ("Loading the json data ...")
with open(valid_json_fn, 'r') as valid_json_f:
    org_json = json.loads(valid_json_f.read())

resolver = RefResolver(referrer=schema, base_uri=base_uri)
schema_folder = Path('../schema')
add_local_schemas_to(resolver, schema_folder, base_uri)
schema_filename = schema_folder / 'root.schema.json'

try:
    validate(org_json, schema, resolver=resolver)
    logging.info("Data is valid")
except SchemaError as e :
    logging.info("there is a schema error")
    logging.info(e.message)
except ValidationError as e :
    logging.info("there is a validation error")
    logging.info(e.message)

