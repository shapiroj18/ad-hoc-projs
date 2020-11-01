from django.http import HttpResponse

# Create your views here.
def index(reequest):
    return HttpResponse("Hello, world. You're at the polls index.")