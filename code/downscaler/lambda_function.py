import boto3
import datetime
import os


ecs = boto3.client('ecs')
environment_tag = os.environ['environment']

def lambda_handler(event, context):
    main()
    

def downscale_service(service_name, cluster_name):
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Downscaling service {service_name} in cluster {cluster_name}...")
    
    response = ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=0
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        ecs.untag_resource(
            resourceArn=response['service']['serviceArn'],
            tagKeys=[
               'Lifecycle'
               
            ]
            )
        print(f"Service {service_name} downscaled successfully.")


def get_cluster_name():
    print(f"Fetching cluster with environment={environment_tag} tag...")

    cluster_arns = []
    response = ecs.list_clusters()
    while 'nextToken' in response:
        cluster_arns += response['clusterArns']
        response = ecs.list_clusters(nextToken=response['nextToken'])
    cluster_arns += response['clusterArns']

    filtered_cluster_arns = []
    filtered_clusters = []
    for arn in cluster_arns:
        response = ecs.list_tags_for_resource(resourceArn=arn)
        tags = response['tags']
        tag_dict = {tag['key']: tag['value'] for tag in tags}
        if 'environment' in tag_dict and tag_dict['environment'] == environment_tag:
            print(f"Cluster found with environment={environment_tag} tag.")
            filtered_cluster_arns.append(arn)
            filtered_clusters.append(arn.split('/')[-1])

    print(filtered_clusters)
    return filtered_clusters        
    
    
    print(f"No clusters found with environment={environment_tag} tag.")
    return None  
    
    
def main():
    
    cluster_name = get_cluster_name()
    if not cluster_name:
        return
    
    # for cluster in cluster
    for cluster in cluster_name:
        print(f"Listing services in cluster {cluster}...")
        response = ecs.list_services(
            cluster=cluster,
            maxResults=100
        )
    
        for service_arn in response['serviceArns']:
            service_name = service_arn.split('/')[-1]
            print(f"Checking service {service_name}...")
            response = ecs.list_tags_for_resource(
                resourceArn=service_arn
            )
            # print(response)
            tags = response['tags']
            env_tag = next((tag for tag in tags if tag['key'] == 'environment'), None)
            if env_tag and env_tag['value'] == environment_tag:
                downscale_service(service_name, cluster)        