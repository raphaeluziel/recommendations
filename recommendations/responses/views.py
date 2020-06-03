from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Responses

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os


# Create your views here.


@login_required()
def index(request):

    """
        This is the main page, which is the questionnaire page.
    """

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

    """
        This view will accept student responses, add it to the database
        send a confirmation email, show the status, etc...
    """

    message = ""

    # Check if student has already submitted a form
    if Responses.objects.filter(student=request.user):
        answers = Responses.objects.get(student=request.user)

    # Of not, create an empty database row for student
    else:
        answers = Responses(student=request.user)

    # Add and or replace answers
    answers.question01 = request.POST["question01"]
    answers.question02 = request.POST["question02"]
    answers.question03 = request.POST["question03"]
    answers.question04 = request.POST["question04"]
    answers.question05 = request.POST["question05"]
    answers.question06 = request.POST["question06"]
    answers.save()

    # If user uploaded a file, then add it to the database
    if len(request.FILES) != 0:

        # Do not add files over 10MB to database, send user back to questionnaire page
        if request.FILES['work'].size > 10485760:
            message = "File size must be less than 10 MB"
            context = {
                "student_response": Responses.objects.get(student=request.user),
                "message": message
                }
            return render(request, "responses/index.html", context, message)

        # File is looking good go to confirmation page
        else:
            message = "File uploaded succesfully"
            answers.file_upload = request.FILES['work']

            answers.save()

    list_of_items_for_email = ''

    # User clicks submit responses in homepage
    if request.method == "POST":

        email_content = "Your questionnaire sent to recommendations@raphaeluziel.net confirmed"

        email_subject = "Your questionnaire sent to recommendations@raphaeluziel.net confirmed"

        # The following uses SendGrid to send a confirmation email to the user
        message = Mail(
            from_email='recommendations@raphaeluziel.net',
            to_emails=request.user.email,
            subject=email_subject,
            html_content=email_content
            )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    return render(request, "responses/confirmation.html")


@login_required()
def confirmation(request):

    return render(request, "responses/confirmation.html")



@staff_member_required
def get_student_list(request):

    """
        This will display a list of all students in the database with links
        to their individual response pages
    """

    students = User.objects.all().order_by('id')

    context = {
        "students": students
    }
    return render(request, "responses/get_student_list.html", context)


@staff_member_required
def get_student_responses(request, student_id):

    """
        This is the page where I will see the student responses
    """

    student = User.objects.get(pk=student_id)
    students_answers = Responses.objects.get(student_id=student_id)

    context = {
        "student": student,
        "students_answers": students_answers
    }
    return render(request, "responses/get_student_responses.html", context)
