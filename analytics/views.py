from django.shortcuts import render

# Create your views here.

def location_view(request):
    return render(request, 'location_views.html')
