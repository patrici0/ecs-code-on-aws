import logging
import os
import boto3
import sys
import json

# Extremely useful for debugging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# handler is like the void main() in Java
# We hate java, java kills people, don't do java
def lambda_handler(event, context):

    # What's triggering my function
    logger.info('got event: {}'.format(event))
    logger.info('got context: {}'.format(context))

    # Parameters validation
    ecs_cluster = ""
    
    if ('ecs_cluster' not in event):
        logger.error("ERROR: Unexpected error: Could not find event['ecs_cluster']")
        sys.exit()
    else:
        ecs_cluster = event['ecs_cluster']
        logger.info(ecs_cluster)

    ecs_service = ""
    
    if ('ecs_service' not in event):
        logger.error("ERROR: Unexpected error: Could not find event['ecs_service']")
        sys.exit()
    else:
        ecs_service = event['ecs_service']
        logger.info(ecs_service)

    ecs_service_desired_count = ""
    
    if ('ecs_service_desired_count' not in event):
        logger.error("ERROR: Unexpected error: Could not find event['ecs_service_desired_count']")
        sys.exit()
    else:
        ecs_service_desired_count = event['ecs_service_desired_count']
        logger.info(ecs_service_desired_count)
    
    # Set up ECS Client
    ecs = boto3.client('ecs')

    response = ecs.update_service(
        cluster=ecs_cluster,
        service=ecs_service,
        desiredCount=ecs_service_desired_count
    )
    logger.info('ecs.update_service got: {}'.format(response))

    return json.dumps(response, indent=4, sort_keys=True, default=str)