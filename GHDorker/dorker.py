import logging
import argparse
from os import getenv
from dotenv import load_dotenv
from ghapi.all import GhApi
from GHDorker.file_parsing import input_parse, output_parse
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


def main(dorks, scope, search, output_filename, debug, input_option='all'):
  """Main logic of the program"""
  if debug:
    logger.setLevel(logging.DEBUG)

  dork_list = input_parse(dorks, input_option[0])
  query_list = [f"{dork} {scope}:{search}" for dork in dork_list]
  client = get_client()

  results = []

  for query in query_list:
    logger.debug("Running against dork: %s", query)
    for result in search_results(query, client):
      updated_results = [{"dork": query, **item} for item in result["items"]]
      for entry in updated_results: console_log_ouput(entry)
      results.extend(updated_results)

  formatted_results = output_format(results)

  if output_filename is not None:
    output_parse(output_filename, formatted_results)


def cli_entry():
  """Parse arguments and kickoff the process"""
  parser = argparse.ArgumentParser(
    description='Search github for github dorks',
    epilog='Use responsibly, Enjoy pentesting')

  parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s 0.3.1')

  parser.add_argument(
    '-s',
    '--scope',
    choices=['repo', 'user', 'org'],
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
    '--options',
    dest='input_option',
    action='append',
    nargs='+',
    help="""YAML Options to target for dorking for example: all.cloud.aws"""
  )

  parser.add_argument(
    'search',
    help='What you would like to search (eg. repo, username, or organization)')

  args = parser.parse_args()
  main(**vars(args))


if __name__=='__main__':
  cli_entry()
