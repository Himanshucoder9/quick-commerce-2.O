import requests
from django.conf import settings


def send_push_notification(device_tokens, title, message):
    """
    Sends a push notification to the provided device tokens using Firebase Cloud Messaging (FCM).

    :param device_tokens: List of device tokens to send the notification to.
    :param title: Title of the notification.
    :param message: Message body of the notification.
    :return: Response from the push notification service.
    """
    if not device_tokens:
        raise ValueError("Device tokens are required")

    server_url = settings.PUSH_NOTIFICATION_URL

    payload = {
        'registration_ids': device_tokens,
        'notification': {
            'title': title,
            'body': message
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={settings.PUSH_NOTIFICATION_API_KEY}'
    }

    response = requests.post(server_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to send notification: {response.text}")

    return response
