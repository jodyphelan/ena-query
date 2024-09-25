from .country import country2iso3
from .query import get_ena_country
import argparse

def get_accestion_country(args: argparse.Namespace) -> None:
    """
    Get the country of origin for a given ENA accession.
    """

    country = get_ena_country(args.accession)

    # If the country is not found, return None
    if country is None:
        print("Country not found")

    # Return the country
    print(country)


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='command')

    subparser = subparsers.add_parser('country', help='Get the country of origin for a given ENA accession.')
    subparser.add_argument('accession', help='The ENA accession ID.')
    subparser.set_defaults(func=get_accestion_country)

    args = argparser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        argparser.print_help()


