import requests
import json
import logging
import os

from base64 import b64decode

# Get values from Environment variables
# TEAMS_WEBHOOK_URL = os.environ['TEAMS_WEBHOOK_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# def send_message(message):
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = requests.post(TEAMS_WEBHOOK_URL, data=json.dumps(message), headers=headers)
#     if response.status_code == 200:
#         logger.info("Message posted to MS Teams")
#     else:
#         logger.error("Failed to send message to MS Teams: %s", response.text)

def lambda_handler(event, context):
    webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')
    if webhook_url is None:
        raise ValueError('TEAMS_WEBHOOK_URL must be defined')

    print(json.dumps(event))
    
    event_time = event['detail']['updatedAt']
    event_name = event['detail']['eventName']
    deployment_id = event['detail']['deploymentId']
    event_reason = event['detail']['reason']
    account = event['account']
    region = event['region']
    time = event['time']
    resources = event['resources'][0].split(':')
    
    cluster_name = resources[5].split('/')[-2]
    service_name = resources[5].split('/')[-1]

    logger.info("Event        : " + str(event))
    # logger.info("TEAMS Webhook URL: " + TEAMS_WEBHOOK_URL)

    # state_emoji = {
    #     'SERVICE_DEPLOYMENT_FAILED': '❌',
    #     'SERVICE_DEPLOYMENT_COMPLETED': '✅',
    #     'SERVICE_DEPLOYMENT_IN_PROGRESS': '🚀'
    # }

    # if "FAILED" in event_name:
    #     color = "#ff4d4f"
    # elif "PROGRESS" in event_name:
    #     color = "#faad14"
    # elif "COMPLETED" in event_name:
    #     color = "#52c41a"
    # else:
    #     color = "#1890ff"
        
    # Customize the message based on the deployment status
    emoji, heading_color = None, None
    if event_name == 'SERVICE_DEPLOYMENT_FAILED':
        # title = 'SERVICE_DEPLOYMENT_FAILED'
        emoji = '❌'
        heading_color = 'Attention'
    elif event_name == 'SERVICE_DEPLOYMENT_IN_PROGRESS':
        # title = 'SERVICE_DEPLOYMENT_IN_PROGRESS'
        emoji = '🚀'
        heading_color = 'Good'
    elif event_name == 'SERVICE_DEPLOYMENT_COMPLETED':
        # title = 'SERVICE_DEPLOYMENT_COMPLETED'
        emoji = '✅'
        heading_color = 'Good'
    else:
        print('Unknown deployment status:', event_name)
        # continue

    # Create the adaptive card message
    card_message = {
        'type': 'message',
        'attachments': [
            {
                'contentType': 'application/vnd.microsoft.card.adaptive',
                'contentUrl': None,
                'content': {
                    '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
                    'type': 'AdaptiveCard',
                    'version': '1.3',
                    'body': [
                        {
                            'type': 'Container',
                            'padding': 'None',
                            'items': [
                                {
                                    'type': 'TextBlock',
                                    'wrap': True,
                                    'size': 'Large',
                                    'color': heading_color,
                                    'text': f'{emoji} {event_name}',
                                },
                            ],
                        },
                        {
                            'type': 'Container',
                            'items': [
                                {
                                    'type': 'TextBlock',
                                    'text': f'Account: {account}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Time: {time}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Region: {region}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Cluster: {cluster_name}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Service: {service_name}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Event Name: {event_name}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Deployment ID: {deployment_id}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Updated At: {event_time}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Reason: {event_reason}',
                                    'wrap': True,
                                },
                            ],
                            'isVisible': False,
                            'id': 'deployment-details',
                        },
                        {
                            'type': 'Container',
                            'padding': 'None',
                            'items': [
                                {
                                    'type': 'ColumnSet',
                                    'columns': [
                                        {
                                            'type': 'Column',
                                            'width': 'stretch',
                                            'items': [
                                                {
                                                    'type': 'TextBlock',
                                                    'text': 'Cluster',
                                                    'wrap': 'true',
                                                    'isSubtle': 'true',
                                                    'weight': 'Bolder',
                                                },
                                                {
                                                    'type': 'TextBlock',
                                                    'wrap': 'true',
                                                    'spacing': 'Small',
                                                    'text': f'{cluster_name}',
                                                },
                                            ],
                                        },
                                        {
                                            'type': 'Column',
                                            'width': 'stretch',
                                            'items': [
                                                {
                                                    'type': 'TextBlock',
                                                    'text': 'Service',
                                                    'wrap': 'true',
                                                    'isSubtle': 'true',
                                                    'weight': 'Bolder',
                                                },
                                                {
                                                    'type': 'TextBlock',
                                                    'wrap': 'true',
                                                    'spacing': 'Small',
                                                    'text': f'{service_name}',
                                                },
                                            ],
                                        },
                                        {
                                            'type': 'Column',
                                            'width': 'stretch',
                                            'items': [
                                                {
                                                    'type': 'TextBlock',
                                                    'text': 'Time',
                                                    'wrap': 'true',
                                                    'isSubtle': 'true',
                                                    'weight': 'Bolder',
                                                },
                                                {
                                                    'type': 'TextBlock',
                                                    'wrap': 'true',
                                                    'spacing': 'Small',
                                                    'text': f'{time}',
                                                },
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                    'padding': 'None',
                    'actions': [
                        {
                            'type': 'Action.ToggleVisibility',
                            'title': 'Show Details',
                            'targetElements': ['deployment-details'],
                        },
                    ],
                },
            },
        ],
    }

    send_teams_webhook(webhook_url, card_message)

def send_teams_webhook(webhook_url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, json=payload)

    if response.status_code != 200:
        print('Failed to send Teams webhook:', response.text)
