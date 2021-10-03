from os import getenv
import logging
import GhAPI
import argparse

gh_token = os.getenv('GH_TOKEN', None)

def get_client() -> GhAPI:
  """Return the GitHub Client"""
  return GhApi(token=GH_TOKEN)


def search_results(query: str):
  client = get_client()
  client.search.code(dork)
  pass


def file_parse(file_path: str) -> str:
  """Parse the dorkfile"""
  with open(file_path, 'r') as f:
    return [line.strip() for line in f.readlines()]


def main(*args, **kwargs):
  dork_list = file_parse(gh_dorks_file)
  query_list = [f"{dork} {type}:{scope}" for dork in dork_list]


if __name__=='__main__':
  parser = argparse.ArgumentParser(
    description='Search github for github dorks',
    epilog='Use responsibly, Enjoy pentesting')

  parser.add_argument(
    '-v', 
    '--version', 
    action='version', 
    version='%(prog)s 0.0.0')

  parser.add_argument(
    '-s',
    '--scope',
    choices=['repo', 'user'],
    help='The type of GitHub object you would like to search')

  parser.add_argument(
    '-d',
    '--dork',
    dest='gh_dorks_file',
    action='store',
    default='github-dorks.txt',
    help='Github dorks file. Eg: github-dorks.txt')

  parser.add_argument(
    '-o',
    '--outputFile',
    dest='output_filename',
    action='store',
    help='CSV File to write results to. This overwrites the file provided! Eg: out.csv')

  parser.add_argument(
    'search',
    required=True,
    help='The GitHub object you would like to search (eg. repo or username)')

  args = parser.parse_args()

  main(args)