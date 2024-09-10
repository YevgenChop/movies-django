import requests
from random import SystemRandom
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse_lazy
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from rest_framework_simplejwt.authentication import JWTAuthentication


class GoogleRawLoginFlowService:
    API_URI = reverse_lazy("google_login_callback")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self, google_client_id: str, google_client_secret: str):
        print(google_client_id, google_client_secret)
        self._google_client_id = google_client_id
        self._google_client_secret = google_client_secret

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = settings.BASE_BACKEND_URL
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._google_client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens(self, *, code: str):
        redirect_uri = self._get_redirect_uri()

        data = {
            "code": code,
            "client_id": self._google_client_id,
            "client_secret": self._google_client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(
            self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise Exception("Failed to obtain access token from Google.")

        tokens = response.json()

        return (
            tokens["id_token"],
            tokens["access_token"]
        )

    def get_user_info(self, access_token: str):
        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

        if not response.ok:
            raise Exception("Failed to obtain user info from Google.")

        return response.json()


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get(
            settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']) or None

        if access_token is None:
            return None

        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token


def set_auth_cookies(response, refresh_token, access_token):
    response.set_cookie(
        key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
        value=refresh_token,
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        samesite='strict',
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
        value=access_token,
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        samesite='strict',
    )
    return response


def clear_auth_cookies(response):
    response.delete_cookie(
        key=settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE'],
        samesite='strict',
    )
    response.delete_cookie(
        key=settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE'],
        samesite='strict',
    )
    return response
