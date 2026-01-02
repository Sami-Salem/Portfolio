rom functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
import re
from collections import defaultdict
import threading

class RateLimiter:
    """Thread-safe rate limiter"""
    def _init_(self, max_requests=60, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, identifier):
        """Check if request is allowed"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds)
            
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Add current request
            self.requests[identifier].append(now)
            return True
    
    def get_remaining(self, identifier):
        """Get remaining requests"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds)
            
            recent_requests = [
                req_time for req_time in self.requests.get(identifier, [])
                if req_time > cutoff
            ]
            
            return max(0, self.max_requests - len(recent_requests))

# Global rate limiter instance
rate_limiter = None

def init_rate_limiter(app):
    """Initialize rate limiter with app config"""
    global rate_limiter
    if app.config.get('RATE_LIMIT_ENABLED', True):
        rate_limiter = RateLimiter(
            max_requests=app.config.get('RATE_LIMIT_PER_MINUTE', 60),
            window_seconds=60
        )

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if rate_limiter is None:
            return f(*args, **kwargs)
        
        # Get identifier (IP address)
        identifier = request.remote_addr
        
        if not rate_limiter.is_allowed(identifier):
            remaining = rate_limiter.get_remaining(identifier)
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.',
                'remaining': remaining
            }), 429
        
        response = f(*args, **kwargs)
        return response
    
    return decorated_function

def validate_input(required_fields=None, max_lengths=None):
    """Input validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            # Check required fields
            if required_fields:
                missing = [field for field in required_fields if field not in data]
                if missing:
                    return jsonify({
                        'error': 'Validation error',
                        'message': f'Missing required fields: {", ".join(missing)}'
                    }), 400
            
            # Check max lengths
            if max_lengths:
                for field, max_len in max_lengths.items():
                    if field in data and len(str(data[field])) > max_len:
                        return jsonify({
                            'error': 'Validation error',
                            'message': f'{field} exceeds maximum length of {max_len}'
                        }), 400
            
            # Sanitize inputs (basic XSS prevention)
            for key, value in data.items():
                if isinstance(value, str):
                    # Remove potentially dangerous characters
                    data[key] = re.sub(r'[<>]', '', value)
            
            request.validated_data = data
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def sanitize_url(url):
    """Sanitize URL input"""
    if not url:
        return None
    
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        raise ValueError('Invalid URL format')
    
    return url

def validate_api_key(api_key_name):
    """Validate API key decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import current_app
            api_key = current_app.config.get(api_key_name)
            
            if not api_key:
                return jsonify({
                    'error': 'Configuration error',
                    'message': f'{api_key_name} not configured'
                }), 500
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator