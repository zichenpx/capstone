import os
import json
from flask import request, abort, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Configuration
AUTH0_DOMAIN = "ytp6dev.us.auth0.com"
API_AUDIENCE = "capstone"
ALGORITHMS = ["RS256"]
CLIENT_ID = "gjjl5lllXJzbpOCJXykQbeI4ZNvSgTSY"

# Gets JSON data from URL
# Source: https://bit.ly/3cbBd5y
# def get_json_data(url):
#     operUrl = urlopen(url)
#     if(operUrl.getcode() != 200):
#         return False

#     data = operUrl.read()
#     jsonData = json.loads(data)
#     return jsonData

"""
AuthError Exception
 - A standardized way to communicate auth failure modes
Handles authentication errors to raise exceptions.
Returns: dictionary with error message and description.
"""
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Format error response and append status code
def get_token_auth_header():
    """
    Obtains the Access Token fron the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description":"Authorization header is expected"
            },
            401
        )
    
    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description":
                    "Authorization header must start with"
                    " Bearer"
            },
            401
        )

    elif len(parts) == 1:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Token not found"
            },
            401
        )

    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 
                    "Authorization header must be"
                    " Bearer token"
            },
            401
        )
    
    token = parts[1]
    return token

# Checks permission against the payload coming from Auth0.
# For more: verify_decode_jwt()
# Accepts: permission (string) and payload (dictionary).
#  - permission: string permission (i.e. 'post:drink')
#  - payload: decoded jwt payload
# Raise an AuthError if permissions are not included in the payload
# !!NOTE check RBAC settings in Auth0
# Raise an AuthError if the requested permission string is not 
#  in the payload permissions array return true otherwise
def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
            },
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {"code": "unauthorized", "description": "Permission not found."}, 401
        )

    return True

# Fetches JSON web key set from Auth0
# Accepts: token (string)
#  - token: a json web token (string)
# Returns: rsa_key (dictionary)
# Link: https://auth0.com/docs/tokens/concepts/jwks
# it should be an Auth0 token with key id (kid)
# it should verify the token using Auth0 /.well-known/jwks.json
# it should decode the payload from the token
# it should validate the claims
# return the decoded payload
# !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):
    # Get the public key fron Auth0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    # Get the header data from the key
    unverified_header = jwt.get_unverified_header(token)

    # Choose rsa key
    rsa_key = {}
    
    # Validate the token whether contains kid
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                401,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        401,
    )

# Decorator to check permissions and authentication on endpoints.
def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError(
                    {
                        "code": "invalid_token",
                        "description": "Access denied due to invalid token",
                    },
                    401,
                )
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

# def requires_scope(required_scope):
#     """Determines if the required scope is present in the Access Token
#     Args:
#         required_scope (str): The scope required to access the resource
#     """
#     token = get_token_auth_header()
#     unverified_claims = jwt.get_unverified_claims(token)
#     if unverified_claims.get("scope"):
#             token_scopes = unverified_claims["scope"].split()
#             for token_scope in token_scopes:
#                 if token_scope == required_scope:
#                     return True
#     return False