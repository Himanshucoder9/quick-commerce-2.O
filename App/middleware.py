import logging
from datetime import datetime
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class AutoLogout(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_datetime = datetime.now()
        last_activity = request.session.get('last_activity', current_datetime)

        session_timeout = settings.SESSION_COOKIE_AGE
        session_inactive_time = (current_datetime - last_activity).total_seconds()

        logger.info(f"User: {request.user}, Last Activity: {last_activity}, Inactive Time: {session_inactive_time}s")

        if session_inactive_time > session_timeout:
            logout(request)
            return

        request.session['last_activity'] = current_datetime
