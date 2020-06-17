import logging
import os
import boto3
import sys
import json

# Extremely useful for debugging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CodePipeline related functions
def comes_from_code_pipeline(event):
    if 'CodePipeline.job' in event:
        return True
    else:
        return False

def put_job_success_result(job_id):
    client = boto3.client('codepipeline')
    response = client.put_job_success_result(
        jobId=job_id,
        executionDetails={
            'summary': 'Lambda execution succeded'
        }
    )
    return response

def put_job_failure_result(job_id):
    client = boto3.client('codepipeline')
    response = client.put_job_failure_result(
        jobId=job_id,
        failureDetails={
            'type': 'JobFailed',
            'message': 'Lambda execution failed - review Cloudwatch logs'
        }
    )
    return response


# handler is like the void main() in Java
# We hate java, java kills people, don't do java
def lambda_handler(event, context):

    # What's triggering my function
    logger.info('got event: {}'.format(event))
    logger.info('got context: {}'.format(context))

    # Parameters validation
    # Check input comes from CodePipeline
    from_code_pipeline = comes_from_code_pipeline(event)
    if from_code_pipeline:
        UserParameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
        if len(UserParameters.split()) != 3:
            logger.error("ERROR: Number of parameters is not 3")
            sys.exit()
        else:
            parameters = {
                'ecs_cluster': UserParameters.split()[0],
                'ecs_service': UserParameters.split()[1],
                'ecs_service_desired_count': int(UserParameters.split()[2])
            }
    else:
        parameters = event['parameters']

    #logger.info('got parameters: {}'.format(parameters))

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
        ecs_service_desired_count = parameters['ecs_service_desired_count']
        logger.info(ecs_service_desired_count)
    
    # Set up ECS Client
    ecs = boto3.client('ecs')

    response = ecs.update_service(
        cluster=ecs_cluster,
        service=ecs_service,
        desiredCount=ecs_service_desired_count
    )
    logger.info('ecs.update_service got: {}'.format(response))

    if response['service']['desiredCount'] == ecs_service_desired_count and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        if from_code_pipeline:
            job_id = event['CodePipeline.job']['id']
            update_job_response = put_job_success_result(job_id)
            logger.info('put_job_success_result got: {}'.format(update_job_response))
        logger.info('ECS Service desired count is {} AND HTTPStatusCode is 200: SUCCESS'.format(ecs_service_desired_count))
    else:
        if from_code_pipeline:
            job_id = event['CodePipeline.job']['id']
            update_job_response = put_job_failure_result(job_id)
            logger.info('put_job_failure_result got: {}'.format(update_job_response))
        logger.error('ECS Service desired count is not {} OR HTTPStatusCode is not 200: FAIL'.format(ecs_service_desired_count))
        
    return json.dumps(response, indent=4, sort_keys=True, default=str)