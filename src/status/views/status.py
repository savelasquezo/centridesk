from rest_framework.response import Response
from rest_framework.views import APIView


class HealthStatus(APIView):

    @staticmethod
    def get(request):
        return Response({'message': 'ok'}, 200)
