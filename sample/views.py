from rest_framework.response import Response
from rest_framework.views import APIView

from sample.time_based_hash import get_toth

# Create your views here.

class LoginTest(APIView):
    """
        URL: /sample/login-test/
        Method: POST
        data: {
            "username": "admin",
            "password": "nothing1234"
        }
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data

        if "HTTP_TOTH" not in request.META or "HTTP_SERVICE_NAME" not in request.META:
            return Response('test', status=403)
        toth = request.META.get("HTTP_TOTH")
        service_name = request.META.get("HTTP_SERVICE_NAME")

        if not (toth and service_name):
            return Response({"msg": "TOTH or Service name value does not exists"}, status=403)
        if not toth == get_toth(service_name):
            return Response({"msg": 'TOTH did not match'}, status=403)

        return Response({"msg": "success"}, status=200)

