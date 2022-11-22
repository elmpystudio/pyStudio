# jupyterhub_config.py file
c = get_config()

import os
pjoin = os.path.join

runtime_dir = os.path.join('/srv/jupyterhub')
ssl_dir = pjoin(runtime_dir, 'ssl')
if not os.path.exists(ssl_dir):
    os.makedirs(ssl_dir)

# put the JupyterHub cookie secret and state db
# in /var/run/jupyterhub
c.JupyterHub.cookie_secret_file = pjoin(runtime_dir, 'cookie_secret')
c.JupyterHub.db_url = pjoin(runtime_dir, 'jupyterhub.sqlite')

from oauthenticator.generic import GenericOAuthenticator
c.JupyterHub.authenticator_class = GenericOAuthenticator

import os

if not 'ANALYTICS_APP_ENV' in os.environ:
    print("ANALYTICS_APP_ENV is not set, defaulting to local")
    os.environ['ANALYTICS_APP_ENV'] = 'local'

if os.environ['ANALYTICS_APP_ENV'] == 'prod':
    domain = 'analytics-platform.ml'
    c.GenericOAuthenticator.client_id = '5hICA5iNiBhBuROGzxGJqGQ7Ur7yH8dHi53aPLB5'
    c.GenericOAuthenticator.client_secret = 'aOgpRtpMtcsOEnZrAqmAyxYlNnZ7StRoH21qGcOcZ25IAvjqEz5zcyje9Kle361PFl1qWNS9xyyqrdU2KKoL8AjRsLmkxVxNIWl7CaQoD0sjSrlX51Gg9uXMk5YB2aH4'

elif os.environ['ANALYTICS_APP_ENV'] == 'local':
    domain = 'localhost'
    c.GenericOAuthenticator.client_id = 'oWFq6aYUAn0fUC5H4TzpEkceMRT7RRmLHaSk7OO2'
    c.GenericOAuthenticator.client_secret = '3FAZA24XW4hPBxS92vvhRhMgsMMcpf3OYsy0JLJu215EF7pIynFim2uA2uFybJfB6ZZNeeUwOA9dSZvmmwL5BAx66NFZaFLbYRxFWkhoBw7Q24ouZYsbhk9tYoEmzF7h'


c.GenericOAuthenticator.oauth_callback_url = 'http://%s/hub/oauth_callback' % domain
c.GenericOAuthenticator.userdata_url = 'http://%s/api/whoami' % domain
c.GenericOAuthenticator.token_url = 'http://%s/oauth/token/' % domain
os.environ["OAUTH2_AUTHORIZE_URL"] = "http://%s/oauth/authorize/" % domain 
os.environ["OAUTH2_TOKEN_URL"] = c.GenericOAuthenticator.token_url # the same as token_url paramhhh

c.Authenticator.admin_users = {'admin'}

c.JupyterHub.base_url = "/hub/"
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.port = 8010

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = 'jupyter/datascience-notebook:latest'

c.DockerSpawner.remove_containers = True
c.DockerSpawner.debug = True

c.Spawner.args = ['--NotebookApp.allow_origin=*']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner

c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': '/home/jovyan' }

#c.Spawner.default_url = '/lab'
# import sys
# c.JupyterHub.services = [
#         {
#             'name': 'announcement',
#             'command': [sys.executable, "-m", "announcement"],
#         }
# ]
