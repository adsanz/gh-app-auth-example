from github import Github, GithubIntegration, GithubException
import logging as log
import os

## logging 
log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = log.getLogger(__name__)


def get_secrets_from_env():
    """
    In order to authenticate with Github, we need to provide some secrets. We will use environment variables for that.

    Authenticating as an app: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
    :return: APP_ID, INSTALLATION_ID, PRIVATE_KEY
    
    """
    from os import environ
    import base64 as bs
    APP_ID = environ.get('APP_ID')
    INSTALLATION_ID = environ.get('INSTALLATION_ID')
    # For multiline secrets, use base64 encoding!! It will allow us to use multiline secrets
    try:
        PRIVATE_KEY = bs.b64decode(environ.get('PRIVATE_KEY')).decode('utf-8')
    except TypeError as e:
        raise Exception('Invalid PRIVATE_KEY format. Please use base64 encoding for multiline secrets') from e
    if not APP_ID or not INSTALLATION_ID or not PRIVATE_KEY:
        raise Exception('Missing secrets')
    return APP_ID, INSTALLATION_ID, PRIVATE_KEY

def get_access_token(app_id, installation_id, private_key):
    """
    Get access token for github app authenticated as an installation.
    Useful if you want to pass the token to another command.

    Token generation: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app
    Authenticating as an app: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
    :return: access_token
    """
    integration = GithubIntegration(app_id, private_key)
    access_token = integration.get_access_token(int(installation_id)).token
    current_app = integration.get_app()
    return access_token, current_app.slug

def delete_git_credentials(git_credential_file_paths):
    """
    Will set global git credentials with credential.helper store to the current token.
    """
    for git_config_file_path in git_credential_file_paths:
        if os.path.exists(git_config_file_path):
            os.remove(git_config_file_path)

def set_git_credentials(token, app_name, git_credential_file_path):
    """
    Will set global git credentials with credential.helper store to the current token.
    """
    log.info(f'Setting git credentials for app {app_name}')
    # clean up previous credentials
    delete_git_credentials(git_credential_file_path)
    credential_line = f'https://{app_name}:{token}@github.com/'
    for git_config_file_path in git_credential_file_path:
        with open(git_config_file_path, 'w') as f:
            f.write(credential_line)

def main():
    log.info('Getting secrets from environment variables')
    APP_ID, INSTALLATION_ID, PRIVATE_KEY = get_secrets_from_env()
    log.info('Getting access token')
    token, app_name = get_access_token(APP_ID, INSTALLATION_ID, PRIVATE_KEY)
    git_credential_file_path = [os.path.expanduser('~/.git-credentials')]
    log.info('Setting git credentials')
    set_git_credentials(token, app_name, git_credential_file_path)

if __name__ == '__main__':
    main()