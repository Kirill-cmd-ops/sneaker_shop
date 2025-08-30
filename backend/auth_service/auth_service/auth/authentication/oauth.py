from httpx_oauth.clients.google import GoogleOAuth2
from auth_service.auth.config import settings

google_oauth_client = GoogleOAuth2(settings.auth_config.client_id, settings.auth_config.client_secret)

