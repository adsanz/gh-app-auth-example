# Demo Example GH APP Auth set-up with Python & GH actions

This is an example of a GH App, a pretty basic one that sets-up .git-credentials with a token that authenticates as the GH App, then the action sets-up the git config to use the credentials and change URL formats from ssh to https so that the token is used. 

This is useful in situations that require you to download other repositories on actions that require authentication. On the case that inspired this demo it was private terraform modules that required authentication so terraform init could work, we used SSH keys but this proof to be quite risky, as even being a secret it was still a key that could be used to access the repo, so we decided to use a GH App instead with least permissions and temporary tokens generated on each run. 

Code is pretty basic, check action.yml to see how we handle execution of the CLI and git config commands, as well as the inputs. Read ops.py to understand how we get the token and set credentials, and finally check the .github/workflows/test-ops.yml to understand how we are calling and testing the action.

## Notes

- The repo on the workflow is a private repository of mine which is being used as a test clone of private repo which the GH App has read-only access
- There is 3 secrets set-up on the repo, which are mandatory so the CLI can get the token and authenticate as the GH App

## Article
This demo is part of an article on medium: 