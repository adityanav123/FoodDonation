from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'portal/startPage.html')


def main(request):
    return render(request, 'portal/index.html')