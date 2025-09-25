from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def home(request):
    context = {
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return render(request, 'main.html', context)