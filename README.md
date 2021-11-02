# GH Dorker

GH Dorker is picking up where several GitHub dorking tools leave off. Many of these dorkers grow stale and old becuase the code is very tangled and intertwined. GH-Dorker is building on the work of several other dorkers and creating a more modular approach.

## Usage

1. Install with pip `pip install ghdorker`
2. (Optional) you can either export an environment variable named "GH_TOKEN" or include it in a local .env file to ensure you can make the most requests. See ["Creating a personal access token"](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for more information on how to do so.

```
usage: ghdorker [-h] [-v] [-s {repo,user,org}] [-d DORKS] [--debug] [-o OUTPUT_FILENAME] [--options INPUT_OPTION [INPUT_OPTION ...]] search

Search github for github dorks

positional arguments:
  search                What you would like to search (eg. repo, username, or organization)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s {repo,user,org}, --scope {repo,user,org}
                        The type of GitHub object you would like to search
  -d DORKS, --dorks DORKS
                        Github dorks file. Eg: github-dorks.txt
  --debug               Set this if you would like to see verbose logging.
  -o OUTPUT_FILENAME, --outputFile OUTPUT_FILENAME
                        File to write results to. This overwrites the file provided! Accepts .json or .csv as output file types.
  --options INPUT_OPTION [INPUT_OPTION ...]
                        YAML Options to target for dorking for example: all.cloud.aws

Use responsibly, Enjoy pentesting
```

Here is a simple example:
```
# The source is a repo and it is running against the gh_dorks_test.txt file
ghdorker -s repo -d samples/dorks.txt dtaivpp/NewsTicker
```

Additionally you can create a yaml config file like so for using only specific dorks on repos.
```yaml
all:
  identity:
    - filename:.dockercfg auth
    - filename:id_rsa or filename:id_dsa
    - filename:.npmrc _auth
    - datafilename:.dockercfg auth
    - dataextension:pem private
    - extension:ppk private
  cloud:
    aws:
      - rds.amazonaws.com password
      - filename:.bash_profile aws
    google:
      - extension:json googleusercontent client_secret
```

This would run all the dorks that fall under the cloud section of the YAML.
```
ghdorker -s repo dtaivpp/NewsTicker -d samples/dorks.yaml --options all.cloud
```

This would run all the dorks that fall under the aws and the identity sections. It's okay to duplicate entries under different sections as on the backend it is checking each entry for uniqueness.
```
ghdorker -s repo dtaivpp/NewsTicker -d samples/dorks.yaml --options all.cloud.aws all.identiy
```

And finally here is an example of how you could output the results to either a json or csv file.
```
ghdorker -s repo dtaivpp/NewsTicker -d samples/dorks.yaml --options all.cloud -o output.json
```

As an aside, rate limiting is already built into the codebase. It will not allow you to make more requests than allowable. GH-Dorker grabs your real rate limits live from GitHub so it will make the maximim amount of requests permittable in a given timeframe.

## Contributing

For how to contribute please see [CONTRIBUTING.md]("CONTRIBUTING.md").


## Credits
Reference points for creating GitDorker and compiling dorks lists

- [@techgaun](https://github.com/techgaun/github-dorks) - This was the primary repo I was looking to for inspiration when writing this dorker
- [@obheda12](https://github.com/obheda12/GitDorker) - You have one of the cleanest README's ive read in a while and if you couldn't tell has inspired much of this project's structure
