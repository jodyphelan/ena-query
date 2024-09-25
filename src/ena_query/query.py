import requests
import xml.etree.ElementTree as ET
from typing import Optional
from .country import country2iso3

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
        url = f'https://www.ebi.ac.uk/ena/browser/api/xml/{wgs_id}'
        response = requests.get(url)
        root = ET.fromstring(response.text)
        # find tag: DB
        sample_accession = None
        for xref in root.findall('.//XREF_LINK'):
            pass
            if xref[0].text=='ENA-SAMPLE':
                sample_accession = xref[1].text
                break
    else:
        sample_accession = wgs_id

    if sample_accession is None:
        raise ValueError(f'No sample accession found for {wgs_id}')
    
    return sample_accession

def get_ena_country(wgs_id: str) -> Optional[str]:
    """
    Get the country of origin for a given ENA accession.

    Parameters
    ----------
    wgs_id : str
        The WGS accession ID.

    Returns
    -------
    country : str
        The country of origin for the given accession.
    """
    sample_accession = get_sample_accession(wgs_id)

    url = f'https://www.ebi.ac.uk/ena/browser/api/xml/{sample_accession}'
    response = requests.get(url)
    root = ET.fromstring(response.text)

    for sattr in root.findall('.//SAMPLE_ATTRIBUTE'):
        if sattr[0].text == 'geographic location (country and/or sea)':
            return {
                'accession':sample_accession,
                'iso3':country2iso3(sattr[1].text)
            }
    
    return {
        'accession':sample_accession,
        'iso3':None
    }

