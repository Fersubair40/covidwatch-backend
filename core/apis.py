from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import InteractionRecord

def require_app_secret_key(fn):
    def decor(self, request, *args, **kwargs):
        secret_key_header = request.META.get('HTTP_X_APP_SECRET_KEY', None)
        if not secret_key_header or secret_key_header != settings.APP_SECRET_KEY:
            return Response(data={"error": "Missing/wrong secret key header"}, status=400)
        return fn(self, request, *args, **kwargs)
    return decor

class StoreInteractionRecord(APIView):
    """Stores an interaction record via POST.
    Requires the `stored_value` property
    Must be accompanied by the app secret key in the X-App-Secret-Key header
    """
    @csrf_exempt
    @require_app_secret_key
    def post(self, request):
        if "stored_value" not in request.POST:
            return Response(data={"error": "Missing stored_value property"}, status=400)

        InteractionRecord.objects.create(stored_value=request.POST['stored_value'])
        return Response(status=200)
