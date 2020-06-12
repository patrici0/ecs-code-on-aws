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
    UserParameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
    parameters = {
        'ecs_cluster': UserParameters.split()[0],
        'ecs_service': UserParameters.split()[1],
        'ecs_service_desired_count': UserParameters.split()[2]
    }

    ecs_cluster = ""
    
    if ('ecs_cluster' not in parameters):
        logger.error("ERROR: Unexpected error: Could not find parameters['ecs_cluster']")
        sys.exit()
    else:
        ecs_cluster = parameters['ecs_cluster']
        logger.info(ecs_cluster)

    ecs_service = ""
    
    if ('ecs_service' not in parameters):
        logger.error("ERROR: Unexpected error: Could not find parameters['ecs_service']")
        sys.exit()
    else:
        ecs_service = parameters['ecs_service']
        logger.info(ecs_service)

    ecs_service_desired_count = ""
    
    if ('ecs_service_desired_count' not in parameters):
        logger.error("ERROR: Unexpected error: Could not find parameters['ecs_service_desired_count']")
        sys.exit()
    else:
        ecs_service_desired_count = int(parameters['ecs_service_desired_count'])
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