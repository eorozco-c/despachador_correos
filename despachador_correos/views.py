import code
from django.shortcuts import render
from django.template import RequestContext

# HTTP ERROR 400
def bad_request(request, exception):
    #error code 400
    code = 400
    return render(request, "errors.html", {"code": code})

def permission_denied(request, exception=None):
    code = 403
    return render(request, "errors.html", {"code": code})

def page_not_found(request, exception=None):
    code = 404
    return render(request, "errors.html", {"code": code})

def server_error(request):
    code = 500
    return render(request, "errors.html", {"code": code})