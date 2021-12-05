from typing import List, Optional
import re
from pydantic import BaseModel,ValidationError, validator, Field
from enum import Enum
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Organism_Part(BaseModel):
    Organism_Part: str
    Organism_Part_Identifier: Optional [str]


class Organism(BaseModel):
    Organism: str
    Organism_Part: List [Organism_Part]

#The json can be loaded also from a file
organism_data={
  "Organism": "Homo sapiens",
  "Organism_Part": [{"Organism_Part":"Kidney",
  "Organism_Part_Identifier": "T-71000"},
                    {"Organism_Part": "Kidney"
                     }
                    ]
}
try:
    organism = Organism(**organism_data)
    #logging.info(organism.Organism)
    #logging.info(repr(organism.Organism_Part.Organism_Part_Identifier))
    #logging.info(organism.Organism_Part)
    logging.info(organism.dict())
except ValueError as e:
    print (e)

