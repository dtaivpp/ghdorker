import logging
import json
import argparse
from os import getenv
from dotenv import load_dotenv
from ghapi.all import GhApi
from GHDorker.helpers import RateLimiter
from GHDorker.helpers import paginator

load_dotenv()
GH_TOKEN = getenv('GH_TOKEN', None)

#### Logging config
console_out = logging.getLogger("ghdorker")
consoleOutHandle = logging.StreamHandler()
consoleOutHandle.setLevel(logging.INFO)
consoleOutFormatter = logging.Formatter('%(asctime)s - %(message)s')
consoleOutHandle.setFormatter(consoleOutFormatter)
console_out.addHandler(consoleOutHandle)
console_out.setLevel(logging.INFO)

logger = logging.getLogger("debug")
consoleHandle = logging.StreamHandler()
consoleHandle.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandle.setFormatter(formatter)
logger.addHandler(consoleHandle)
logger.setLevel(logging.ERROR)


def get_client() -> GhApi:
  """Return the GitHub Client"""
  logger.debug("Creating GitHub API Object %s GitHub Token",
               'with' if GH_TOKEN is not None else 'without')

  return GhApi(token=GH_TOKEN)


def search_results(query: str, client: GhApi):
  """Yeilds results pages"""
  search_gen = paginator(client.search.code, q=query)
  rate_limits = RateLimiter(client)

  for results in search_gen:
    logger.debug("Current Rate Limits: %s",
                 rate_limits.get_rate_limits('search'))
    rate_limits.check_safety("search")
    yield results


def input_file_parse(file_path: str) -> str:
  """Parse the dorkfile"""
  logger.debug("Opening %s", file_path)

  with open(file_path, 'r', encoding="UTF-8") as infile:
    logger.debug("Reading %s", file_path)
    return [line.strip() for line in infile.readlines()]


def output_json_file(data, filename):
  """Output the data as a JSON File"""
  if len(data) == 0:
    return

  with open(filename, "+w", encoding="UTF-8") as outfile:
    for entry in data:
      json.dump(entry, outfile)
      outfile.write("\n")


def output_csv_file(data, filename):
  """Output the data as a CSV File"""
  if len(data) == 0:
    return

  logger.debug("Writing CSV File: %s", filename)
  with open(filename, "+w", encoding="UTF-8") as outfile:
    outfile.write("dork, repository, path, score\n")
    for entry in data:
      outfile.write(f"{entry['dork']}, {entry['repository']}, {entry['path']}, {entry['score']}\n")


def output_format(results):
  """Formatter for data"""
  logger.debug("Formatting Results")
  return [
    {
      "dork": item["dork"],
      "repository": item["repository"]["full_name"],
      "path": item["path"],
      "score": item["score"]
    }
    for item in results
  ]


def console_log_ouput(item):
  """Function for logging results to console"""
  console_out.info(f"dork: {item['dork']}, "
                   f"repository: {item['repository']['full_name']}, "
                   f"path: {item['path']}, "
                   f"score: {item['score']}")


def main(dorks, scope, search, output_filename, debug):
  """Main logic of the program"""
  if debug:
    logger.setLevel(logging.DEBUG)

  dork_list = input_file_parse(dorks)
  query_list = [f"{dork} {scope}:{search}" for dork in dork_list]
  client = get_client()

  results = []

  for query in query_list:
    for result in search_results(query, client):
      updated_results = [{"dork": query, **item} for item in result["items"]]

      map(console_log_ouput, updated_results)

      results.extend(updated_results)

  formatted_results = output_format(results)

  if output_filename.endswith('.json'):
    output_json_file(formatted_results, output_filename)
  elif output_filename.endswith('.csv'):
    output_csv_file(formatted_results, output_filename)


def cli_entry():
  """Parse arguments and kickoff the process"""
  parser = argparse.ArgumentParser(
    description='Search github for github dorks',
    epilog='Use responsibly, Enjoy pentesting')

  parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s 0.2.0')

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
    '--debug',
    action='store_true',
    help='Set this if you would like to see verbose logging.')


  parser.add_argument(
    '-o',
    '--outputFile',
    dest='output_filename',
    action='store',
    help="""File to write results to. This overwrites the file provided!\n
            Accepts .json or .csv as output file types.""")

  parser.add_argument(
    'search',
    help='The GitHub object you would like to search (eg. repo or username)')

  args = parser.parse_args()
  main(**vars(args))


if __name__=='__main__':
  cli_entry()
