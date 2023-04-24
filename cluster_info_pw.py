from kubernetes import client
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration
import getpass

default_user = "quicklab"
default_password = "RedHat1!"
# v76Hc-Sv6ED-qUvQN-b2GrK

apihost = 'https://api.ricocluster.lab.upshift.rdu2.redhat.com:6443'
username = input("Enter your username: ") or default_user
password = getpass.getpass("Enter your password: ") or default_password

kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
kubeConfig.host = apihost
kubeConfig.verify_ssl = False
kubeConfig.ssl_ca_cert = './test-cluster.crt'

# Retrieve the auth token
kubeConfig.get_token()
print('Auth token: {0}'.format(kubeConfig.api_key))
print('Token expires: {0}'.format(kubeConfig.api_key_expires))

k8s_client = client.ApiClient(kubeConfig)
dyn_client = DynamicClient(k8s_client)
v1_projects = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')
project_list = v1_projects.get()

for project in project_list.items:
    print(project.metadata.name)

kubeConfig.get_token()
print('Auth token: {0}'.format(kubeConfig.api_key))
print('Token expires: {0}'.format(kubeConfig.api_key_expires))
