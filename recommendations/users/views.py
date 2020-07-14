from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm
from responses.models import Responses

# Create your views here.

def signup(request):
    # If user has already logged in skip the signup form
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # Create a database row for new student, and set status
            answers = Responses(student=user)
            answers.status = 'Not Submitted'
            answers.save()

            login(request, user)
            return redirect ('index')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})
