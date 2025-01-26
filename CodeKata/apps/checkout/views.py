import http
import json
from django.shortcuts import HttpResponse
from CodeKata.apps.checkout.checkout_processor import cart_checkout


def checkout_cart(request):
    request_body = json.loads(request.body.decode("utf-8"))
    response = cart_checkout(request_body)
    status_code = response.pop("status_code", http.HTTPStatus.BAD_REQUEST)
    return HttpResponse(json.dumps(response, default=str), status=status_code, content_type="application/json")

