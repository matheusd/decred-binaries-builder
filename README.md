# Decred Timed Binaries Builder

This repo has a single script (`builder.py`) that gets executed periodically and triggers a full decred binaries rebuild.

These builds are meant to be testing binaries, to be used by designers, testers, translators and other parties interested in previewing the next version of [Decrediton](https://github.com/decred/decrediton).

The build binaries are currently available at the github repo [decred-weekly-builds](https://github.com/matheusd/decred-weekly-builds).


## Configuing for Automatic Build

To configure weekly/daily/whatever builds, you need to add this repo into travis and configure the (protected) travis environment variable `GITHUB_OATH_TOKEN` with the github token that has access to the destination repository.

After that, you can configure the travis project to run a build on this repo daily/weekly and the binaries will be built periodically.

## How it Works

The `builder.py` script creates a new commit and corresponding release in the destination repo, modifying the `versions.json` with the commit hash for each relevant source repo (dcrd/dcrwallet/decrediton). This automatically triggers a travis/appveyor build for the relevant platforms.

As the builds finish, the artifacts are uploaded to the release.
