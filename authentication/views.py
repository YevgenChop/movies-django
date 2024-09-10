import requests
from django.conf import settings
from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import (
    TokenRefreshView as BaseTokenRefreshView
)

from .services import (
    GoogleRawLoginFlowService,
    set_auth_cookies,
    clear_auth_cookies
)
from .serializers import UserRegisterSerializer
from .models import User


class RegisterView(APIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = UserRegisterSerializer
    token_uri = reverse_lazy("token_obtain_pair")

    def _get_token_url(self):
        domain = settings.BASE_BACKEND_URL
        return f"{domain}{self.token_uri}"

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {'error': e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
                exception=True
            )

        serializer.create(serializer.validated_data)

        response = requests.post(self._get_token_url(), data=serializer.data)
        return Response(
            response.json(),
            status=response.status_code,
            headers=response.headers,
            content_type=response.headers['Content-Type']
        )


class TokenObtainPairView(TokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except ValidationError as e:
            return Response(
                {'error': e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
                exception=True
            )

        response = Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )
        response = set_auth_cookies(
            response,
            refresh_token=str(serializer.validated_data['refresh']),
            access_token=str(serializer.validated_data['access'])
        )

        return response


class LogoutView(APIView):
    def post(self, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_200_OK)
        response = clear_auth_cookies(response)
        return response


class TokenRefreshView(BaseTokenRefreshView):
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)

        if not serializer.initial_data.get('refresh'):
            serializer.initial_data['refresh'] = request.COOKIES.get(
                settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']
            )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            response = set_auth_cookies(
                response,
                refresh_token=str(response.data['refresh']),
                access_token=str(response.data['access'])
            )

        return super().finalize_response(request, response, *args, **kwargs)


class GoogleLoginRedirectView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request: Request):
        google_login_flow = GoogleRawLoginFlowService(
            google_client_id=settings.GOOGLE_CLIENT_ID,
            google_client_secret=settings.GOOGLE_CLIENT_SECRET
        )

        authorization_url, state = google_login_flow.get_authorization_url()
        request.session["google_oauth2_state"] = state
        return redirect(authorization_url)


class GoogleLoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    TOKEN_OBTAIL_URI = reverse_lazy("token_obtain_pair")

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        if not isinstance(validated_data, dict):
            return Response(
                {"error": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        if code is None or state is None:
            return Response(
                {"error": "Code and state are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        session_state = request.session.get("google_oauth2_state")

        if session_state is None:
            return Response(
                {"error": "CSRF check failed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        del request.session["google_oauth2_state"]

        if state != session_state:
            return Response(
                {"error": "CSRF check failed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        google_login_flow = GoogleRawLoginFlowService(
            google_client_id=settings.GOOGLE_CLIENT_ID,
            google_client_secret=settings.GOOGLE_CLIENT_SECRET
        )

        _, access_token = google_login_flow.get_tokens(code=code)

        user_info = google_login_flow.get_user_info(access_token)
        user_email = user_info["email"]

        if not User.objects.filter(email=user_email).exists():
            User.objects.create_user(email=user_email, password=None)

        user = User.objects.get(email=user_email)
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email

        response = redirect(settings.BASE_FRONTEND_URL + "/dashboard/movies")
        response = set_auth_cookies(
            response,
            refresh_token=str(refresh),
            access_token=str(refresh.access_token)
        )

        return response
