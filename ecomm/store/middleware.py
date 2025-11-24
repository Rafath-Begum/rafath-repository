import time
import logging

logger = logging.getLogger('shop')

class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        logger.debug(f"Request to {request.path} took {duration:.2f} seconds")
        return response