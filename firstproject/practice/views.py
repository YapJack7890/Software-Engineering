from django.shortcuts import render, redirect
from . forms import CreateUserForm

# Create your views here.
def home(request):

        return render(request, 'home')


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("home")
        
    context = {'registerform': form }
    return render(request, 'register.html', context=context)

def login(request):
    return render(request, 'login.html')