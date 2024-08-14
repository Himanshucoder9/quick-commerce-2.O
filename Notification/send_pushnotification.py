import google
import requests
from django.conf import settings
from google.oauth2 import service_account
import google.auth.transport.requests


def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
    credentials = service_account.Credentials.from_service_account_file(
        'quickecommerce-a7b00-firebase-adminsdk-mglu2-1064ca47b2.json', scopes=[
            "https://www.googleapis.com/auth/firebase.messaging",
        ]
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token


print(_get_access_token())


def send_push_notification(device_tokens, title, message, image, order_number):
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

    headers = {
        'Content-Type': 'application/json; UTF-8',
        'Authorization': 'Bearer ' + _get_access_token(),
    }
    responses = []

    for token_value in device_tokens:
        payload = {

            "message": {
                "notification": {
                    "title": title,
                    "body": message,
                    "image": image,
                },
                "token": token_value,
                "data": {
                    "type": "order",
                    "order_number": order_number,
                    "order": "Thank You",
                    "order_id": "Bla Bla Bla",
                    "status": "Delivered",

                }
            },

        }

        response = requests.post(server_url, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to send notification to token {token_value}: {response.text}")

        responses.append(response.json())

    return responses
