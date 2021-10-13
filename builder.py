from github3 import login, GitHub
import os
import sys
import time
import json

# fixme: to be changed to a decred repo
DECRED_REPO_OWNER = "decred"
BUILD_REPO_OWNER = "matheusd"
BUILD_REPO_REPO = "decred-weekly-builds"

README_TEMPLATE = """
# Decred Development Binaries

![build status](https://github.com/matheusd/decred-weekly-builds/actions/workflows/decrediton.yml/badge.svg)


**DO NOT USE IN PRODUCTION**

These are binaries for the decred project built from unstable, under development
code. Do not use in production. You will not receive support for them.

**MIGHT NOT ALLOW DOWNGRADE**

Sometimes dcrd/dcrwallet changes include migrations which cannot be downgraded.
Since these builds are made from code that is under development (usually from
the master branch of the respective repos), this means that they may include such
migrations. Therefore after running these builds, you might be unable to go back
to older versions of the software without deleting the blockchain or wallet
files.

**YOU HAVE BEEN WARNED**

[Latest Release](https://github.com/{BUILD_REPO_OWNER}/{BUILD_REPO_REPO}/releases/latest)

## Version Information

<pre>
version id = <a href="https://github.com/{BUILD_REPO_OWNER}/{BUILD_REPO_REPO}/releases/tag/{tagName}">{version}</a>
      dcrd = <a href="https://github.com/{dcrdRepoOwner}/dcrd/commits/{shaDcrd}">{shaDcrd}</a>
    dcrctl = <a href="https://github.com/{dcrctlRepoOwner}/dcrctl/commits/{shaDcrctl}">{shaDcrctl}</a>
 dcrwallet = <a href="https://github.com/{dcrwRepoOwner}/dcrwallet/commits/{shaDcrwallet}">{shaDcrwallet}</a>
    dcrlnd = <a href="https://github.com/{dcrlndRepoOwner}/dcrlnd/commits/{shaDcrlnd}">{shaDcrlnd}</a>
decrediton = <a href="https://github.com/{decreditonRepoOwner}/decrediton/commits/{shaDecrediton}">{shaDecrediton}</a>
</pre>

## Repository Information

- **dcrd** = [{dcrdRepoOwner}/{dcrdBranch}](https://github.com/{dcrdRepoOwner}/dcrd)
- **dcrctl** = [{dcrctlRepoOwner}/{dcrctlBranch}](https://github.com/{dcrctlRepoOwner}/dcrctl)
- **dcrwallet** = [{dcrwRepoOwner}/{dcrwBranch}](https://github.com/{dcrwRepoOwner}/dcrwallet)
- **dcrlnd** = [{dcrlndRepoOwner}/{dcrlndBranch}](https://github.com/{dcrlndRepoOwner}/dcrlnd)
- **decrediton** = [{decreditonRepoOwner}/{decreditonBranch}](https://github.com/{decreditonRepoOwner}/decrediton)


"""

def envVarOrDef(varName, default):
    if varName in os.environ:
        return os.environ[varName]
    return default

def getRepoMasterCommit(g, repoOwner, repoName, repoBranch):
    repo = g.repository(repoOwner, repoName)
    branchName = repoBranch if repoBranch != None else repo.default_branch
    master = repo.branch(branchName)
    if not master:
        raise "Branch %s not found in repo %s/%s" % (repoBranch, repoOwner, repoName)
    return master.commit.sha

def main():
    if (not ("GITHUB_OATH_TOKEN" in os.environ)):
        print("Please define the env variable GITHUB_OATH_TOKEN with the github token")
        sys.exit(1)

    # You may override this by using an appropriate environment variable
    dcrdRepoOwner = envVarOrDef("DCRD_REPO_OWNER", DECRED_REPO_OWNER)
    dcrwRepoOwner = envVarOrDef("DCRW_REPO_OWNER", DECRED_REPO_OWNER)
    dcrctlRepoOwner = envVarOrDef("DCRCTL_REPO_OWNER", DECRED_REPO_OWNER)
    dcrlndRepoOwner = envVarOrDef("DCRLND_REPO_OWNER", DECRED_REPO_OWNER)
    decreditonRepoOwner = envVarOrDef("DECREDITON_REPO_OWNER", DECRED_REPO_OWNER)
    dcrdBranch = envVarOrDef("DCRD_BRANCH", None)
    dcrctlBranch = envVarOrDef("DCRCTL_BRANCH", None)
    dcrwBranch = envVarOrDef("DCRW_BRANCH", None)
    dcrlndBranch = envVarOrDef("DCRLND_BRANCH", None)
    decreditonBranch = envVarOrDef("DECREDITON_BRANCH", None)

    g = login(token=os.environ["GITHUB_OATH_TOKEN"])
    versionInfo = {
        "shaDcrd": getRepoMasterCommit(g, dcrdRepoOwner, "dcrd", dcrdBranch),
        "shaDcrctl": getRepoMasterCommit(g, dcrctlRepoOwner, "dcrctl", dcrctlBranch),
        "shaDcrwallet": getRepoMasterCommit(g, dcrwRepoOwner, "dcrwallet", dcrwBranch),
        "shaDcrlnd": getRepoMasterCommit(g, dcrlndRepoOwner, "dcrlnd", dcrlndBranch),
        "shaDecrediton": getRepoMasterCommit(g, decreditonRepoOwner, "decrediton", decreditonBranch),
        "version": time.strftime("%Y%m%d%H%M%S", time.gmtime()),
        "DECRED_REPO_OWNER": DECRED_REPO_OWNER,
        "BUILD_REPO_OWNER": BUILD_REPO_OWNER,
        "BUILD_REPO_REPO": BUILD_REPO_REPO,
        "dcrdRepoOwner": dcrdRepoOwner,
        "dcrctlRepoOwner": dcrctlRepoOwner,
        "dcrwRepoOwner": dcrwRepoOwner,
        "dcrlndRepoOwner": dcrlndRepoOwner,
        "decreditonRepoOwner": decreditonRepoOwner,
        "dcrdBranch": dcrdBranch,
        "dcrctlBranch": dcrctlBranch,
        "dcrwBranch": dcrwBranch,
        "dcrlndBranch": dcrlndBranch,
        "decreditonBranch": decreditonBranch,
    }

    print("Using dcrd version %s" % versionInfo["shaDcrd"])
    print("Using dcrctl version %s" % versionInfo["shaDcrctl"])
    print("Using dcrwallet version %s" % versionInfo["shaDcrwallet"])
    print("Using dcrlnd version %s" % versionInfo["shaDcrlnd"])
    print("Using decrediton version %s" % versionInfo["shaDecrediton"])
    print("Generating as version %s" % versionInfo["version"])


    tagName = "v" + versionInfo["version"]
    versionInfo["tagName"] = tagName
    message = "Development release  %s" % versionInfo["version"]
    versionsFile = json.dumps(versionInfo, sort_keys=True, indent=2)
    readme = README_TEMPLATE.format(**versionInfo)

    destRepo = g.repository(BUILD_REPO_OWNER, BUILD_REPO_REPO)
    #destRepo.contents('/versions.json').update(message, versionsFile.encode('utf-8'))
    #destRepo.contents('/README.md').update(message, readme.encode('utf-8'))

    master = destRepo.branch(destRepo.default_branch)
    oldTree = destRepo.tree(master.commit.sha)
    print("Current master: %s" % master.commit.sha)

    blobVersions = destRepo.create_blob(versionsFile, encoding='utf-8')
    blobReadme = destRepo.create_blob(readme, encoding='utf-8')

    newTree = destRepo.create_tree([
        {'path': 'versions.json', 'mode': '100644', 'type': 'blob', 'sha': blobVersions},
        {'path': 'README.md', 'mode': '100644', 'type': 'blob', 'sha': blobReadme},
    ], oldTree.sha);
    print("Uploaded new tree %s" % newTree.sha)

    author = {'name': 'Automated Builder', 'email': 'automated-builder@decred.org'}

    commit = destRepo.create_commit(message, tree=newTree.sha,
        parents=[master.commit.sha], author=author, committer=author)
    print("Created commit %s" % commit.sha)

    ref = destRepo.ref('heads/%s' % destRepo.default_branch)
    ref.update(commit.sha)
    print("Updated master branch to new commit")

    destRepo.create_release(tagName, body=readme)
    print("Created Release %s" % tagName)


if __name__ == "__main__":
    main()
