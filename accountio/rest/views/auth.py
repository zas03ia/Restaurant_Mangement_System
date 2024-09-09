from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data["email"], password=request.data["password"]
        )  # check for valid credentials
        if user:
            token, created = Token.objects.get_or_create(user=user)
            # return token key aalong with user information
            return Response(
                {"token": token.key, "name": user.get_full_name(), "email": user.email}
            )
        else:
            return Response({"error": "Invalid credentials"}, status=401)
