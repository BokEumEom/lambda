import os
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')
    if webhook_url is None:
        raise ValueError('TEAMS_WEBHOOK_URL must be defined')
    
    # 이벤트 데이터 파싱
    # event_detail = event.get('detail', {})
    
    print(json.dumps(event))
    
    event_categories = event['detail']['EventCategories']
    message = event['detail']['Message']
    event_id = event['detail']['EventID']
    identifier = event['detail']['SourceIdentifier']
    source_type = event['detail']['SourceType']
    region = event['region']
    time = event['time']
    account = event['account']
    resources = event['resources'][0].split(':')
    cluster_name = resources[-1]
    
    logger.info("Event        : " + str(event))
    
    # MS Teams 웹훅 URL
    # teams_webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')

    # MS Teams로 보낼 메시지 생성
    # message = {
    #     "@type": "MessageCard",
    #     "@context": "http://schema.org/extensions",
    #     "themeColor": "0072C6",
    #     "title": "Aurora RDS Event",
    #     "text": f"Aurora RDS Cluster Event: {event_detail.get('Message')}\n{event_detail.get('EventCategories')}"
    # }
    
    emoji = '🔔'
        
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
                                    'text': f'{emoji} {message}',
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
                                    'text': f'Identifier: {identifier}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Event Name: {message}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'Event ID: {event_id}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'EventCategories: {event_categories}',
                                    'wrap': True,
                                },
                                {
                                    'type': 'TextBlock',
                                    'text': f'SourceType: {source_type}',
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
                                                    'text': 'DB identifier',
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
                                                    'text': 'Region',
                                                    'wrap': 'true',
                                                    'isSubtle': 'true',
                                                    'weight': 'Bolder',
                                                },
                                                {
                                                    'type': 'TextBlock',
                                                    'wrap': 'true',
                                                    'spacing': 'Small',
                                                    'text': f'{region}',
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

    # MS Teams로 메시지 전송
    send_teams_webhook(webhook_url, card_message)

def send_teams_webhook(webhook_url, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, headers=headers, json=payload)

    if response.status_code != 200:
        print('Failed to send Teams webhook:', response.text)
