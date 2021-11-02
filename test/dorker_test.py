from GHDorker import dorker, file_parsing
from ghapi.all import GhApi


def test_get_client():
  client = dorker.get_client()
  assert isinstance(client, GhApi)


def test_file_parse():
  test_query_list = [
    "filename:.dockercfg auth",
    "extension:md",
    "filename:.npmrc _auth",
    "datafilename:.dockercfg auth",
    "dataextension:pem private",
    "extension:ppk private",
    "filename:id_rsa or filename:id_dsa",
    "extension:sql mysql dumpmysql dump"
  ]
  querylist = file_parsing.input_file_parse("samples/dorks.txt")

  # Check that there are no differences between lists
  diff = set(querylist) ^ set(test_query_list)
  assert not diff


def test_formatter():
  results = [
    {
      "dork": "extension:md repo:dtaivpp/NewsTicker",
      **gh_result['items'][0]
    }
  ]

  ouput = dorker.output_format(results)
  assert "dork" in ouput[0]
  assert "repository" in ouput[0]
  assert "path" in ouput[0]
  assert "score" in ouput[0]



gh_result = {
        'total_count': 1,
        'incomplete_results': False,
        'items': [
          {
            "name": "ReadMe.md",
            "path": "ReadMe.md",
            "sha": "dbaa81253c6440a0893152493301c7b380922a03", #pragma: allowlist secret
            "url": "https://api.github.com/repositories/246320627/contents/ReadMe.md?ref=25a30e453bd1f50d9c4f92aef8cade85908d768d",
            "git_url": "https://api.github.com/repositories/246320627/git/blobs/dbaa81253c6440a0893152493301c7b380922a03",
            "html_url": "https://github.com/dtaivpp/NewsTicker/blob/25a30e453bd1f50d9c4f92aef8cade85908d768d/ReadMe.md",
            "repository": {
              "id": 246320627,
              "node_id": "MDEwOlJlcG9zaXRvcnkyNDYzMjA2Mjc=",
              "name": "NewsTicker",
              "full_name": "dtaivpp/NewsTicker",
              "private": False,
              "owner": {
                "login": "dtaivpp",
                "id": 17506770,
                "node_id": "MDQ6VXNlcjE3NTA2Nzcw",
                "avatar_url": "https://avatars.githubusercontent.com/u/17506770?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/dtaivpp",
                "html_url": "https://github.com/dtaivpp",
                "followers_url": "https://api.github.com/users/dtaivpp/followers",
                "following_url": "https://api.github.com/users/dtaivpp/following{/other_user}",
                "gists_url": "https://api.github.com/users/dtaivpp/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/dtaivpp/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/dtaivpp/subscriptions",
                "organizations_url": "https://api.github.com/users/dtaivpp/orgs",
                "repos_url": "https://api.github.com/users/dtaivpp/repos",
                "events_url": "https://api.github.com/users/dtaivpp/events{/privacy}",
                "received_events_url": "https://api.github.com/users/dtaivpp/received_events",
                "type": "User",
                "site_admin": False,
              },
              "html_url": "https://github.com/dtaivpp/NewsTicker",
              "description": "This project scrapes web pages and creates a public opinion ticker for stock symbols",
              "fork": "False",
              "url": "https://api.github.com/repos/dtaivpp/NewsTicker",
              "forks_url": "https://api.github.com/repos/dtaivpp/NewsTicker/forks",
              "keys_url": "https://api.github.com/repos/dtaivpp/NewsTicker/keys{/key_id}",
              "collaborators_url": "https://api.github.com/repos/dtaivpp/NewsTicker/collaborators{/collaborator}",
              "teams_url": "https://api.github.com/repos/dtaivpp/NewsTicker/teams",
              "hooks_url": "https://api.github.com/repos/dtaivpp/NewsTicker/hooks",
              "issue_events_url": "https://api.github.com/repos/dtaivpp/NewsTicker/issues/events{/number}",
              "events_url": "https://api.github.com/repos/dtaivpp/NewsTicker/events",
              "assignees_url": "https://api.github.com/repos/dtaivpp/NewsTicker/assignees{/user}",
              "branches_url": "https://api.github.com/repos/dtaivpp/NewsTicker/branches{/branch}",
              "tags_url": "https://api.github.com/repos/dtaivpp/NewsTicker/tags",
              "blobs_url": "https://api.github.com/repos/dtaivpp/NewsTicker/git/blobs{/sha}",
              "git_tags_url": "https://api.github.com/repos/dtaivpp/NewsTicker/git/tags{/sha}",
              "git_refs_url": "https://api.github.com/repos/dtaivpp/NewsTicker/git/refs{/sha}",
              "trees_url": "https://api.github.com/repos/dtaivpp/NewsTicker/git/trees{/sha}",
              "statuses_url": "https://api.github.com/repos/dtaivpp/NewsTicker/statuses/{sha}",
              "languages_url": "https://api.github.com/repos/dtaivpp/NewsTicker/languages",
              "stargazers_url": "https://api.github.com/repos/dtaivpp/NewsTicker/stargazers",
              "contributors_url": "https://api.github.com/repos/dtaivpp/NewsTicker/contributors",
              "subscribers_url": "https://api.github.com/repos/dtaivpp/NewsTicker/subscribers",
              "subscription_url": "https://api.github.com/repos/dtaivpp/NewsTicker/subscription",
              "commits_url": "https://api.github.com/repos/dtaivpp/NewsTicker/commits{/sha}",
              "git_commits_url": "https://api.github.com/repos/dtaivpp/NewsTicker/git/commits{/sha}",
              "comments_url": "https://api.github.com/repos/dtaivpp/NewsTicker/comments{/number}",
              "issue_comment_url": "https://api.github.com/repos/dtaivpp/NewsTicker/issues/comments{/number}",
              "contents_url": "https://api.github.com/repos/dtaivpp/NewsTicker/contents/{+path}",
              "compare_url": "https://api.github.com/repos/dtaivpp/NewsTicker/compare/{base}...{head}",
              "merges_url": "https://api.github.com/repos/dtaivpp/NewsTicker/merges",
              "archive_url": "https://api.github.com/repos/dtaivpp/NewsTicker/{archive_format}{/ref}",
              "downloads_url": "https://api.github.com/repos/dtaivpp/NewsTicker/downloads",
              "issues_url": "https://api.github.com/repos/dtaivpp/NewsTicker/issues{/number}",
              "pulls_url": "https://api.github.com/repos/dtaivpp/NewsTicker/pulls{/number}",
              "milestones_url": "https://api.github.com/repos/dtaivpp/NewsTicker/milestones{/number}",
              "notifications_url": "https://api.github.com/repos/dtaivpp/NewsTicker/notifications{?since,all,participating}",
              "labels_url": "https://api.github.com/repos/dtaivpp/NewsTicker/labels{/name}",
              "releases_url": "https://api.github.com/repos/dtaivpp/NewsTicker/releases{/id}",
              "deployments_url": "https://api.github.com/repos/dtaivpp/NewsTicker/deployments",
              },
            "score": 1.0
            }
        ]
      }
