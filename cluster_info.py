from kubernetes import client
from kubernetes.client import ApiClient
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration
import getpass


pod_search = input("Enter the name of the pod to retrieve: ") or ["alertmanager-main-0", "prometheus-k8s-0", "console-cbd6c889b-226dc"]
project_search = input("Enter the name of the project': ") or ["openshift-monitoring", "openshift-console"]  

def __get_kubernetes_client(cluster_details):
    try:
        print("Collecting credentials for " + cluster_details["api_server_endpoint"])
        username = input("Enter your username: ") or "default_name"
        password = getpass.getpass("Enter your password: ")
        
        kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
        kubeConfig.host = cluster_details["api_server_endpoint"]
        kubeConfig.verify_ssl = True
        kubeConfig.ssl_ca_cert = cluster_details["ca_cert"] # use a certificate bundle for the TLS validation
        # Retrieve the auth token
        kubeConfig.get_token() 
        k8s_client = client.ApiClient(kubeConfig)      
        dyn_client = DynamicClient(k8s_client)
        return dyn_client
    
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None


def get_pods():
    print("%s\t\t%s\t\t\t%s\t\t\t%s" % 
    ("POD IP", "PROJECT", "NAME", "CLUSTER"))

    for cluster in all_clusters:   
        v1_pods = cluster["client"].resources.get(api_version='v1', kind='Pod')
        pod_list = v1_pods.get()       
        for pod in pod_list.items:
            if pod.metadata.name in pod_search:
                print("%s\t%s\t%s\t%s" %
                (pod.status.podIP, pod.metadata.namespace, pod.metadata.name, cluster["api_server_endpoint"]))  


if __name__  ==  "__main__":
    cluster1_details = {
        "ca_cert":"./certificates/cluster1.crt",
        "api_server_endpoint":"https://api.cluster1.openshift.com:6443",
        "client":OCPLoginConfiguration(ocp_username=None, ocp_password=None)
    } 
    cluster2_details = {
        "ca_cert":"./certificates/cluster2.crt",
        "api_server_endpoint":"https://api.cluster2.openshift.com:6443",
        "client":OCPLoginConfiguration(ocp_username=None, ocp_password=None)
    } 
    all_clusters = [cluster1_details, cluster2_details]

for cluster in all_clusters:   
    cluster["client"] = __get_kubernetes_client(cluster)

get_pods()
