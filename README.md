# GH Dorker

GH Dorker is picking up where several GitHub dorking tools leave off. Many of these dorkers grow stale and old becuase the code is very tangled and intertwined. GH-Dorker is building on the work of several other dorkers and creating a more modular approach. 

## Usage

1. Install with pip `pip install gh-dorker`
2. (Optional) you can either export an environment variable named "GH_TOKEN" or include it in a local .env file to ensure you can make the most requests. See ["Creating a personal access token"](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for more information on how to do so. 

```
usage: gh-dorker [-h] [-v] [-s {repo,user}] [-d DORKS] [-o OUTPUT_FILENAME] searchSearch github for github dorkspositional arguments:  search                The GitHub object you would like to search (eg. repo or username)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s {repo,user}, --scope {repo,user}
                        The type of GitHub object you would like to search
  -d DORKS, --dorks DORKS
                        Github dorks file. Eg: github-dorks.txt
  -o OUTPUT_FILENAME, --outputFile OUTPUT_FILENAME
                        File to write results to. This overwrites the file provided!

Use responsibly, Enjoy pentesting
```

Here is an example: 
```
# The source is a repo and it is running against the gh_dorks_test.txt file
gh-dorker -s repo -d gh_dorks_test.txt dtaivpp/NewsTicker
```

As an aside, rate limiting is already built into the codebase. It will not allow you to make more requests than allowable. GH-Dorker grabs your real rate limits live from GitHub so it will make the maximim amount of requests permittable in a given timeframe. 


## Credits 
Reference points for creating GitDorker and compiling dorks lists

- [@techgaun](https://github.com/techgaun) - This was the primary repo I was looking to for inspiration when writing this dorker
- [@obheda12](https://github.com/obheda12) - You have one of the cleanest README's ive read in a while and if you couldn't tell has inspired much of this project's structure

