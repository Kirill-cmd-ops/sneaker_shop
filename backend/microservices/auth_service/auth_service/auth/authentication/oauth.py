from httpx_oauth.clients.google import GoogleOAuth2
from microservices.auth_service.auth_service.auth.config import settings

google_oauth_client = GoogleOAuth2(
    client_id=settings.auth_config.client_id,
    client_secret=settings.auth_config.client_secret,
)
