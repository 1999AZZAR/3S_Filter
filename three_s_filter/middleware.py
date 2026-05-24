import functools
from typing import Any, Callable, Optional
from .engine import ThreeSFilter

class APIFilterMiddleware:
    """
    Middleware to intercept API calls and filter the responses.
    """
    def __init__(self, engine: Optional[ThreeSFilter] = None):
        self.engine = engine or ThreeSFilter()

    def wrap_openai(self, client: Any):
        """
        Wraps an OpenAI client to filter chat completion responses.
        Example: 
            client = OpenAI()
            middleware.wrap_openai(client)
        """
        original_create = client.chat.completions.create
        
        @functools.wraps(original_create)
        def filtered_create(*args, **kwargs):
            response = original_create(*args, **kwargs)
            # Extract text content
            content = response.choices[0].message.content
            
            decision, report = self.engine.evaluate(content)
            if decision == "BLOCK":
                raise PermissionError(f"3S_Filter BLOCKED OpenAI response: {report}")
            
            return response
            
        client.chat.completions.create = filtered_create
        return client

    def wrap_requests(self):
        """
        Monkey-patches the 'requests' library to filter all incoming JSON/text responses.
        Use with caution.
        """
        import requests
        original_get = requests.get
        original_post = requests.post
        
        def filter_response(response):
            try:
                text = response.text
                decision, report = self.engine.evaluate(text)
                if decision == "BLOCK":
                    raise PermissionError(f"3S_Filter BLOCKED HTTP response from {response.url}: {report}")
            except Exception:
                pass
            return response

        @functools.wraps(original_get)
        def filtered_get(*args, **kwargs):
            return filter_response(original_get(*args, **kwargs))

        @functools.wraps(original_post)
        def filtered_post(*args, **kwargs):
            return filter_response(original_post(*args, **kwargs))

        requests.get = filtered_get
        requests.post = filtered_post
        print("3S_Filter: requests library patched.")
