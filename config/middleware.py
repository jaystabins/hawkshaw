# https://github.com/bblanchon/django-htmx-messages-framework/blob/bootstrap5/htmx_messages/middleware.py
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.messages import get_messages


class HtmxMessageMiddleware(MiddlewareMixin):
    """
    Middleware that moves messages into the HX-Trigger header when request is made with HTMX
    """

    def process_response(self, request, response):

        # The HX-Request header indicates that the request was made with HTMX
        if "HX-Request" not in request.headers:
            return response

        # Extract the messages
        messages = [
            {"message": message.message, "tags": message.tags}
            for message in get_messages(request)
        ]
        if not messages:
            return response

        # Get the existing HX-Trigger that could have been defined by the view
        hx_trigger = response.headers.get("HX-Trigger")

        if hx_trigger is None:
            # If the HX-Trigger is not set, start with an empty object
            hx_trigger = {}
        elif hx_trigger.startswith("{"):
            # If the HX-Trigger uses the object syntax, parse the object
            hx_trigger = json.loads(hx_trigger)
        else:
            # If the HX-Trigger uses the string syntax, convert to the object syntax
            hx_trigger = {hx_trigger: True}

        # Add the messages array in the HX-Trigger object
        hx_trigger["messages"] = messages

        # Add or update the HX-Trigger
        response.headers["HX-Trigger"] = json.dumps(hx_trigger)

        # HTMX does not display trigger on non-2XX status_code's
        # This is very very bad
        response.status_code = 200
        return response