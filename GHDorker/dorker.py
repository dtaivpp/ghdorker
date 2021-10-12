import logging
import json
import argparse
from os import getenv
from ghapi.all import GhApi
from GHDorker.helpers import RateLimiter
from GHDorker.helpers import paginator

from dotenv import load_dotenv
load_dotenv()
GH_TOKEN = getenv('GH_TOKEN', None)


def get_client() -> GhApi:
  """Return the GitHub Client"""
  return GhApi(token=GH_TOKEN)


def search_results(query: str, client: GhApi):
  """Yeilds results pages"""
  search_gen = paginator(client.search.code, q=query)
  rate_limits = RateLimiter(client)

  for results in search_gen:
    rate_limits.check_safety("search")
    yield results


def input_file_parse(file_path: str) -> str:
  """Parse the dorkfile"""
  with open(file_path, 'r') as f:
    return [line.strip() for line in f.readlines()]


def output_file(data, filename):
  """Writes the ouput to a file"""
  with open(filename, "+w") as f:
    for entry in data:
      json.dump(entry, f) 
      f.write("\n")


def format(results):
  """Formatter for data"""
  return [
    {
      "dork": item["dork"], 
      "repository": item["repository"]["full_name"], 
      "path": item["path"], 
      "score": item["score"]
    }
    for item in results
  ]


def main(dorks, scope, search, output_filename):
  dork_list = input_file_parse(dorks)
  query_list = [f"{dork} {scope}:{search}" for dork in dork_list]
  client = get_client()

  results = []

  for query in query_list:
    for result in search_results(query, client):
      results.extend([{"dork": query, **item} for item in result["items"]])
  
  formatted_results = format(results)
  output_file(formatted_results, output_filename)


def cli_entry():
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
    default='output.txt',
    help='File to write results to. This overwrites the file provided!')

  parser.add_argument(
    'search',
    help='The GitHub object you would like to search (eg. repo or username)')

  args = parser.parse_args()
  main(**vars(args))


if __name__=='__main__':
  cli_entry()