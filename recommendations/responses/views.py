from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Responses

# Create your views here.

@login_required()
def index(request):

    # Check if student has already submitted a form
    if Responses.objects.filter(student=request.user):
        answers = Responses.objects.get(student=request.user)

        context = {
            "student_response": answers or None
            }

    else:
        context = {}

    return render(request, "responses/index.html", context)

@login_required()
def submit_responses(request):

    # Check if student has already submitted a form
    if Responses.objects.filter(student=request.user):
        answers = Responses.objects.get(student=request.user)

    # Of not, create an empty database row for student
    else:
        answers = Responses(student=request.user)

    answers.question01 = request.POST["question01"]
    answers.question02 = request.POST["question02"]
    answers.question03 = request.POST["question03"]
    answers.question04 = request.POST["question04"]
    answers.question05 = request.POST["question05"]
    answers.question06 = request.POST["question06"]

    answers.save()

    context = {
        "student_response": Responses.objects.get(student=request.user)
        }

    return render(request, "responses/index.html", context)
