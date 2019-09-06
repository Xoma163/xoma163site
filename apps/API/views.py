import json

from django.http import HttpResponse


# Create your views here.

def test(request):
    where = request.GET['where']
    print(where)
    print("Hello, World!")
    response_data = {'success': True}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
