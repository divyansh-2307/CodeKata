import http
import json
from django.shortcuts import HttpResponse
from CodeKata.apps.products.product_processor import add_new_product


def add_product(request):
    request_body = json.loads(request.body.decode("utf-8"))
    response = add_new_product(request_body)
    status_code = response.pop("status_code", http.HTTPStatus.BAD_REQUEST)
    return HttpResponse(json.dumps(response, default=str), status=status_code, content_type="application/json")
