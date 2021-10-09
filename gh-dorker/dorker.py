import logging
import argparse
from os import getenv
from ghapi.all import GhApi
from ghapi.page import paged
from helpers import RateLimiter
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()
GH_TOKEN = getenv('GH_TOKEN', None)


def get_client() -> GhApi:
  """Return the GitHub Client"""
  return GhApi(token=GH_TOKEN)


def search_results(query: str, client: GhApi):
  """Yeilds results pages"""
  search_gen = paged(client.search.code, per_page=100, q=query)
  rate_limits = RateLimiter(client)

  for results in search_gen:
    rate_limits.check_safety("search")
    yield results


def file_parse(file_path: str) -> str:
  """Parse the dorkfile"""
  with open(file_path, 'r') as f:
    return [line.strip() for line in f.readlines()]


def main(dorks, scope, search):
  dork_list = file_parse(dorks)
  query_list = [f"{dork} {scope}:{search}" for dork in dork_list]
  client = get_client()

  for query in query_list:
    print(query)
    print("\n")
    for result in search_results(query, client):
      print(result)
      print("\n")

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
    '--dorks',
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
    help='The GitHub object you would like to search (eg. repo or username)')

  args = parser.parse_args()
  pprint(args)
  main(dorks=args.dorks, search=args.search, scope=args.scope)