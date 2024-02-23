import argparse
import boto3
import os
from datetime import datetime, timedelta
import pytz

ecs = boto3.client('ecs')
ENV = os.getenv('ENV')
Created_By = os.getenv('GITHUB_TRIGGERING_ACTOR')
Created_At_UTC = os.getenv('UTC_DATE')
upscale_time_duration = os.getenv('upscale_time_duration')

utc = pytz.timezone('UTC')
now_utc = datetime.now(utc)

added_time_utc = now_utc + timedelta(hours=int(upscale_time_duration))

active_time_utc = added_time_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

def upscale_service(service_name, cluster_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Upscaling service {service_name} in cluster {cluster_name}...")
    
    response = ecs.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=1
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        ecs.tag_resource(
            resourceArn=response['service']['serviceArn'],
            tags=[
                {
                    'key': 'Lifecycle',
                    'value': 'true'
                },
                {
                    'key': 'Started_At_UTC',
                    'value': Created_At_UTC
                },
                {
                    'key': 'Started_By',
                    'value': Created_By
                },
               
                {
                    'key': 'Active_till_UTC',
                    'value': active_time_utc
                },
                {
                    'key': 'Active_duration',
                    'value': upscale_time_duration
                }
                
            ]
        )
        print(f"Service {service_name} upscaled successfully.")

def get_cluster_name():
    print(f"Fetching cluster with ENV={ENV} tag...")

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
        if 'environment' in tag_dict and tag_dict['environment'] == ENV:
            print(f"Cluster found with environment={ENV} tag.")
            filtered_cluster_arns.append(arn)
            filtered_clusters.append(arn.split('/')[-1])

    print(filtered_clusters)
    return filtered_clusters        
    
    
    print(f"No clusters found with environment={ENV} tag.")
    return None

def main(action):
    
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
            lifecycle_tag = next((tag for tag in tags if tag['key'] == 'Lifecycle'), None)
            if not lifecycle_tag:
                if env_tag and env_tag['value'] == ENV:
                    if action == 'upscale':
                        upscale_service(service_name, cluster)
            elif lifecycle_tag:
                print(f"{ENV} infra is already up")
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upscale or downscale ECS services.')
    parser.add_argument('action', choices=['upscale', 'downscale'], help='Action to perform (upscale or downscale)')
    args = parser.parse_args()
    
    main(args.action)
