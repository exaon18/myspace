from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# Create your views here.
def home(request):
    if request.method == 'POST':
        print(request.POST.get('username'))

    return render(request, 'home.html')