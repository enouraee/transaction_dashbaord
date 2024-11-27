import json
import logging
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

# Set up the custom logger for request logging
request_logger = logging.getLogger("request_logger")


class RequestLogMiddleware(MiddlewareMixin):
    """
    Middleware to log details of each request and response.

    Attributes:
    ----------
    exclude_url_starts : list
        List of URL prefixes to exclude from logging.
    method_allowed : list
        List of HTTP methods to include in logging.
    """

    exclude_url_starts = []
    method_allowed = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def process_request(self, request):
        """
        Process the incoming request.

        Parameters:
        ----------
        request : HttpRequest
            The HTTP request object.
        """
        if request.method in self.method_allowed and not any(
            request.path.startswith(url) for url in self.exclude_url_starts
        ):
            request.request_time = datetime.now()
            if request.method in ["POST", "PUT", "PATCH"]:
                request.req_body = request.body

    def process_response(self, request, response):
        """
        Process the outgoing response.

        Parameters:
        ----------
        request : HttpRequest
            The HTTP request object.
        response : HttpResponse
            The HTTP response object.

        Returns:
        -------
        HttpResponse
            The HTTP response object.
        """
        if hasattr(request, "request_time"):
            request.response_time = datetime.now()
            log_data = self.extract_log_info(request=request, response=response)
            request_logger.info(json.dumps(log_data))
        return response

    def process_exception(self, request, exception):
        """
        Process any exceptions raised during request processing.

        Parameters:
        ----------
        request : HttpRequest
            The HTTP request object.
        exception : Exception
            The exception object.

        Returns:
        -------
        None
        """
        if hasattr(request, "request_time"):
            request.response_time = datetime.now()
            log_data = self.extract_log_info(request=request, exception=exception)
            request_logger.error(json.dumps(log_data))

    def extract_log_info(self, request, response=None, exception=None):
        """
        Extract log information from the request and response.

        Parameters:
        ----------
        request : HttpRequest
            The HTTP request object.
        response : HttpResponse, optional
            The HTTP response object (default is None).
        exception : Exception, optional
            The exception object (default is None).

        Returns:
        -------
        dict
            A dictionary containing log information.
        """
        log_data = {
            "remote_address": request.META.get(
                "HTTP_X_REAL_IP", request.META.get("REMOTE_ADDR", "unknown")
            ),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "request_datetime": str(request.request_time),
            "response_datetime": str(request.response_time),
            "process_time": str(request.response_time - request.request_time),
            "user": (
                request.user.phone_number
                if request.user.is_authenticated
                else "Anonymous"
            ),
        }

        # Log request body
        try:
            if request.method in ["POST", "PUT", "PATCH"]:
                log_data["request_body"] = json.loads(request.req_body.decode("utf-8"))
            else:
                log_data["request_body"] = None  # No body for GET or DELETE
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError, AttributeError):
            log_data["request_body"] = "Could not decode body; may not be JSON."
        except Exception as error:
            log_data["request_body"] = f"Could not decode body. Error: {error}"

        # Log response body
        if response:
            try:
                response_body = json.loads(response.content.decode("utf-8"))
                log_data["response_body"] = response_body
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
                log_data["response_body"] = "Could not decode body; may not be JSON."
            except AttributeError:
                log_data["response_body"] = "No body present."
            except Exception as error:
                log_data["response_body"] = f"Could not decode body. Error: {error}"

        # Log exception
        if exception:
            log_data["exception"] = str(exception)

        return log_data
