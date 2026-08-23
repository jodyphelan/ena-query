import toml
import os

def country2iso3(country):
    # get location of the current file
    current_dir = os.path.dirname(__file__)
    # load the toml file
    country2iso3_lookup = toml.load(f'{current_dir}/country2iso3.toml')
    return country2iso3_lookup.get(country, None)

def clean_country(country):
    """
    Clean the country name by removing any text after a comma or semicolon.
    
    Parameters
    ----------
    country : str
        The country name to clean.
    
    Returns
    -------
    str
        The cleaned country name.
    """
    if country is None:
        return None
    return country.split(':')[0].strip()