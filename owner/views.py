from django.shortcuts import render

# Create your views here.

def owner_func(request):

    return render(request, 'owner/owner.html')    

