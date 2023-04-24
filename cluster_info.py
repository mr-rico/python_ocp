from kubernetes import client
from kubernetes.client import ApiClient

pod_name = input("Enter the name of the pod to retrieve [default=alertmanager-main-0]: ") or "alertmanager-main-0"
project_name = input("Enter the name of the project [default=oneview-nextgen-dev]: ") or "openshift-monitoring"

def __get_kubernetes_client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.CoreV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def get_pods(cluster_details, namespace=project_name,all_namespaces=False):
        client_api= __get_kubernetes_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        for i in client_api.list_namespaced_pod(namespace = project_name).items:
            if i.metadata.name == pod_name:
                print("%s\t%s\t%s" %
                (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

if __name__ == "__main__":
    cluster1_details={
        "bearer_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6ImtMR21iVTYtSjE3TU10OWdNMl9zVVVaYmEtNWhjZ2kzX1JhWmIxQldtYWsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJvcGVuc2hpZnQtbW9uaXRvcmluZyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyaWNvLXNhLXRva2VuLWRjNjRqIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6InJpY28tc2EiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI3ODBmYzk3MS0xMGQ3LTRiMGUtYWFlZS0zMDY2NjBjOWJjYjIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6b3BlbnNoaWZ0LW1vbml0b3Jpbmc6cmljby1zYSJ9.P145rC1cyeFYOjMeH4w0oU7WWf5eXZgyAISy3gETug7BVqbF746_sc7EMSozVuQm4lfoOvqxp6IiLa2aJx1XIBNg83eXNGryOuXDKvDEsxsjlznmW2YlRtjjFus_0wRKEV80S9nbOro_ILKnpAC0CBVIkyrbjEP44_hwI7o7drKfIhUduyh_HNDv9ohCPxMlkU7MqI6S0m3JNi_Y54HSLUyHeAnpabpJPgrOaFUjdDxAlnHTi3UXBCV1WHGTD4MbVlwPKtW9eoZUYR8mLDei3OEKHP4Nem-vGNUPrTy84-vOUMLBvd4qvE9PvK6918PFECk3XH4mEs6gXPMN6Oj2kPudBSijclfZ5aWtiTs7QgtwlvehFvGwME8bhfJ9iJvAtfPN0RlHtayKWwe49MfgEat6OlJNX6FCAySqEBDcmscXntQslELLpRjtdov4x6NK4pQ_ErPyzckYFBDQ89HYuzwhhXVqz4d0QZEVFXdxGnSupva3ykkvku0dulV4fje95YkbEInVjxXkdrw7jaCl7oiz0gOnpqvveDp0wKlFcdnVrCp_Frb_4qEI4-KYk6Pb1rHRKeC3BbFgKRELJcyCmdUpl3UcgnIdX-EBJ-m2QFuyM-u3IIGEujQ3rW_d_1x4q_Onp8pAELA-A1Pik8TehUnnzn02xzojvPaIcr4r5Mo",
        "api_server_endpoint":"https://api.ricocluster.lab.upshift.rdu2.redhat.com:6443"

    }      

print("CLUSTER 1 OUTPUT")
get_pods(cluster1_details)
