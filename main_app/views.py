from django.shortcuts import render

# Create your views here.


def home_page(request):
    return render(request, 'main_app/home_page.html', context={})


def test_page(request):
    return render(request, 'main_app/test_page.html', context={})


def serve_test_page(request):
    return render(request, 'main_app/test_page.html', context={})
