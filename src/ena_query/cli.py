import json
from .query import get_ena_metadata
import argparse
import logging

def run_query(args: argparse.Namespace) -> None:
    """
    Get the metadata for a given ENA accession.
    """

    metadata = get_ena_metadata(args.accession)

    if metadata is None:
        logging.error(f"No metadata found for accession {args.accession}")
        return

    print(json.dumps(metadata, indent=4))


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='command')

    subparser = subparsers.add_parser('metadata', help='Get the metadata for a given ENA accession.')
    subparser.add_argument('accession', help='The ENA accession ID.')
    subparser.set_defaults(func=run_query)

    args = argparser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        argparser.print_help()


