import asyncio

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tg_bot.models import InitData


class TestTGAuth(APIView):
    def get(self, request):
        header_auth = request.headers.get('authorization')
        # asyncio.run(send_tg_messages())
        InitData.objects.create(text=header_auth)
        return Response(header_auth, status=status.HTTP_200_OK)
