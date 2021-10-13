#######
# Script to delete old releases from GH for cleanup
#######

from github3 import login, GitHub
import sys
import os

from github3.repos import release

# fixme: to be changed to a decred repo
DECRED_REPO_OWNER = "decred"
BUILD_REPO_OWNER = "matheusd"
BUILD_REPO_REPO = "decred-weekly-builds"
KEEP_LAST = 5

def main():
    if (not ("GITHUB_OATH_TOKEN" in os.environ)):
        print("Please define the env variable GITHUB_OATH_TOKEN with the github token")
        sys.exit(1)

    g = login(token=os.environ["GITHUB_OATH_TOKEN"])
    destRepo = g.repository(BUILD_REPO_OWNER, BUILD_REPO_REPO)

    releases = destRepo.releases()
    i = 0
    for r in releases:
        i += 1
        if (i <= KEEP_LAST):
            continue
        print("deleteing %s from %s" % (r.name, r.created_at))
        r.delete()

if __name__ == "__main__":
    main()
