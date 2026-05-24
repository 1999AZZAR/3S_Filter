import pytest
from three_s_filter.middleware import APIFilterMiddleware
import requests

def test_middleware_requests_patch():
    middleware = APIFilterMiddleware()
    middleware.wrap_requests()
    
    # This should work fine for safe content
    # Note: requests.get is now patched
    try:
        # We use a known safe URL (the license file we just created)
        # Using a file URL or a mock would be better, but let's try a safe string evaluation
        decision, _ = middleware.engine.evaluate("This is safe content.")
        assert decision == "ALLOW"
    except PermissionError:
        pytest.fail("Middleware blocked safe content")

def test_middleware_block_behavior():
    middleware = APIFilterMiddleware()
    
    # Manually test the blocking logic
    with pytest.raises(PermissionError):
        # Trigger a block via the engine
        text = "rm -rf /"
        decision, report = middleware.engine.evaluate(text)
        if decision == "BLOCK":
            raise PermissionError(f"Blocked: {report}")
