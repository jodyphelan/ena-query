from logging import root
from unittest import result

import requests
import csv
from io import StringIO
import xml.etree.ElementTree as ET
from typing import Optional

from ena_query.dates import clean_date
from .country import clean_country, country2iso3

COLUMN_MAPPING = {
    'geographic location (country and/or sea)': 'country',
    'geo_loc_name': 'country',
    'country': 'country',
    'collection_date': 'collection_year',
    'collection date': 'collection_year',
}
ISOLATE_COLUMN_NAMES = [
    'isolate',
    'sample_name',
    'strain',
    'SUBJECT_ID'
]

def get_sample_accession(wgs_id: str) -> str:
    """
    Get the sample accession for a given WGS accession.
    
    Parameters
    ----------
    wgs_id : str
        The WGS accession ID.
    
    Returns
    -------
    sample_accession : str
        The sample accession ID
    """
    if 'RR' in wgs_id:
        url = f'https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=run_accession={wgs_id}&fields=sample_accession'
        response = requests.get(url)
        for row in csv.DictReader(StringIO(response.text), delimiter='\t'):
            sample_accession = row.get('sample_accession')
    else:
        sample_accession = wgs_id

    if sample_accession is None:
        raise ValueError(f'No sample accession found for {wgs_id}')
    
    return sample_accession

def get_ena_metadata(wgs_id: str) -> Optional[dict]:
    """
    Get the metadata for a given ENA accession.

    Parameters
    ----------
    wgs_id : str
        The WGS accession ID.

    Returns
    -------
    dict
        A dictionary containing the metadata for the given accession, including 'accession', 'country', 'iso3', and 'collection_date' if available.
    """
    sample_accession = get_sample_accession(wgs_id)

    url = f'https://www.ebi.ac.uk/ena/browser/api/xml/{sample_accession}'
    response = requests.get(url)
    if response.status_code == 400:
        raise ValueError(f'No data found on ENA for {wgs_id}')
    root = ET.fromstring(response.text)

    result = {
        'accession': sample_accession, 
        'isolate_names': {},
        'organism_name': None,
        'taxon_id': None,
        'centre_name': None,
        'collected_by': None,
        'collection_year': None,
        'country': None,
        'iso3': None,
    }
    


    for sattr in root.findall('.//SAMPLE_ATTRIBUTE'):
        if sattr[0].text in COLUMN_MAPPING.keys():
            key = COLUMN_MAPPING[sattr[0].text]
            

            if key == 'country':
                cleaned_country = clean_country(sattr[1].text)
                result['country'] = cleaned_country
                result['iso3'] = country2iso3(cleaned_country)
            elif key == 'collection_year':
                result['collection_year'] = clean_date(sattr[1].text)
            else:
                result[key] = sattr[1].text
        if sattr[0].text in ISOLATE_COLUMN_NAMES:
            result['isolate_names'][sattr[0].text.lower()] = sattr[1].text


    if root.find('.//TITLE') is not None:
        result['isolate_names']['sample_title'] = root.find('.//TITLE').text


    #         <SAMPLE_NAME>
    # <TAXON_ID>1773</TAXON_ID>
    # <SCIENTIFIC_NAME>Mycobacterium tuberculosis</SCIENTIFIC_NAME>
    # </SAMPLE_NAME>
    
    organism = root.find('.//SAMPLE_NAME/SCIENTIFIC_NAME')
    result['organism_name'] = organism.text if organism is not None else None
    taxon_id = root.find('.//SAMPLE_NAME/TAXON_ID')
    result['taxon_id'] = taxon_id.text if taxon_id is not None else None

# <SAMPLE accession="SAMD00589883" alias="SAMD00589883" center_name="Department of Pathophysiology and Host Defense, The Research Institute of Tuberculosis, Japan Anti-Tuberculosis Association" broker_name="DDBJ">
    sample = root.find('.//SAMPLE')
    result['centre_name'] = sample.attrib.get('center_name')
    result['centre_name'] = result['centre_name'] if result['centre_name'] is not None else None
    return result

