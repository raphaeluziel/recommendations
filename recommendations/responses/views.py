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

import datetime

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

        # If so, check whether she has uploaded a file
        if answers.file_upload is not None:
            head, tail = os.path.split(str(answers.file_upload))
            fileName = tail

        context = {
            "student_response": answers or None,
            "fileName": fileName or None,
            }

    # Student is a new user, or has not submitted anything yet
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

    # User clicks submit responses in homepage
    if request.method == "POST":

        # Check if student has already submitted a form
        if Responses.objects.filter(student=request.user):
            answers = Responses.objects.get(student=request.user)

        # If not, create an empty database row for student
        else:
            answers = Responses(student=request.user)

        # Add and or replace answers
        answers.question01 = request.POST["question01"]
        answers.question02 = request.POST["question02"]
        answers.question03 = request.POST["question03"]
        answers.question04 = request.POST["question04"]
        answers.question05 = request.POST["question05"]
        answers.question06 = request.POST["question06"]
        answers.status = 'Submitted'
        answers.save()

        # If user uploaded a file, then add it to the database
        if len(request.FILES) != 0:

            # Did student upload a file?
            if request.FILES.get('work'):

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
                    answers.file_upload = request.FILES['work']
                    answers.save()

        list_of_items_for_email = ''

        email_content = "Hi " + request.user.first_name + ", " + "<br><br>I\'ve received your responses.  If you wish to change your answers, or check on the status of the recommendation feel free to go back to <a href='https://recommendations.raphaeluziel.net'>https://recommendations.raphaeluziel.net</a>. You may update your answers until the status of your recommendation changes to 'written'.<br><br>Best of luck,<br><br>Mr. Uziel"

        email_subject = "Recommendation form received"

        # The following uses SendGrid to send a confirmation email to the user
        message = Mail(
            from_email='ruziel@hsas-lehman.org',
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

    return HttpResponseRedirect(reverse('index'))


@login_required()
def confirmation(request):

    return render(request, "responses/confirmation.html")



@staff_member_required
def get_student_list(request):

    """
        This will display a list of all students in the database with links
        to their individual response pages.  The first column will list all
        students who have registered, the second column all who have gone the
        next step and submitted a response
    """

    # get a list of all students who regitered
    students = User.objects.filter(is_staff=False).order_by('last_name')

    # Get a lit of all students who responded
    responses = Responses.objects.filter(student__is_staff=False).order_by('status', 'timestamp')

    # How many letters did I write?
    total = responses.count()
    written = responses.filter(status='Written').count()
    if total > 0:
        percentage = round((100 * written / total), 1)
    else:
        percentage = 0

    context = {
        "students": students,
        "responses": responses,
        "total": total,
        "written": written,
        "percentage": percentage
    }
    return render(request, "responses/get_student_list.html", context)


@staff_member_required
def get_student_responses(request, student_id):

    """
        This is the page where I will see the student responses
    """

    try:
        student = User.objects.get(pk=student_id)
    except:
        return render(request, "responses/error.html", {"message": "Student Does Not Exist"})

    # Check if student submitted any answers at all
    try:
        students_answers = Responses.objects.get(student_id=student_id)
    except:
        students_answers = None

    context = {
        "student": student,
        "students_answers": students_answers
    }
    return render(request, "responses/get_student_responses.html", context)
