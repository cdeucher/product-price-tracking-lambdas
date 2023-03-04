import boto3
import logging
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_REGION = "us-east-1"
sns_client = boto3.client("sns", region_name=AWS_REGION)

def subscription(authorization, topic):
    logger.info(f'Event: {topic}')

    decodedToken = jwt.decode(authorization, algorithms=["RS256"], options={"verify_signature": False})
    email = decodedToken["email"]
    logger.info("decodedToken: %s %s", email, decodedToken)

    request_create_subscription(topic, email)
    return { 'message': 'subscription ok' }, 200


def request_create_topic(event):
    try:
        topic = create_topic(event.get('id'))
        logger.info("topic: %s", topic)
        return { 'message': 'create topic ok' }, 200
    except Exception as e:
        logger.exception(f'Could not create SNS topic.')

def request_create_subscription(topic, email):
    try:
        new_topic = create_topic(topic.get('id'))
        subscription = create_subscription(new_topic.get('TopicArn'), email)
        logger.info("subscription: %s", subscription)
    except Exception as e:
        logger.exception(f'Could not create subscription.')

def create_subscription(topic_arn, email):
    try:
        response = sns_client.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
        subscription_arn = response.get('SubscriptionArn')
        logger.info(f'Created SNS subscription {email} for topic {subscription_arn}.')
    except Exception as e:
        logger.exception(f'Could not create SNS subscription {email} for topic {subscription_arn}.')
        raise

    return response

def create_topic(name):
    topic = 'Could not create SNS topic '+name
    try:
        topic = sns_client.create_topic(Name=name)
        logger.info(f'Created SNS topic {name}.')
    except Exception as e:
        logger.exception(f'Could not create SNS topic {name}.')

    return topic