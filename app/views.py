from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


#==========================================================
# Registration, Login, Logout
#==========================================================

def index(request):
    return render(request, "index.html")


def register(request):
    if(request.method=="POST"): 
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        password_input = request.POST["password"]
        pw_hash = bcrypt.hashpw(password_input.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=pw_hash
        )
        messages.success(request, "Registration complete! Please log in.")
    return redirect("/")


def login(request):
    if(request.method=="POST"): 
        email = request.POST["email"]
        password_input = request.POST["password"]

        user = User.objects.filter(email=email)
        if not user:
            messages.error(request, "Invalid credentials")
            return redirect ("/")

        logged_in_user = user[0]

        if bcrypt.checkpw(password_input.encode(), logged_in_user.password.encode()):
            request.session["u_id"] = logged_in_user.id
            return redirect("/quiz/dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect ("/")
    return redirect ("/")


def logout(request):
    if(request.method=="POST"): 
        del request.session["u_id"]
        request.session.clear()
    return redirect ("/")


#==========================================================
# Dashboard
#==========================================================


def dashboard(request):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        u_id = request.session["u_id"]
        user = User.objects.get(id=u_id)        

        context = {
            "first_name": user.first_name,
            "u_id": u_id
        }
        return render(request, "dashboard.html", context)
    return redirect ("/")



#==========================================================
# Display Quiz
#==========================================================




#==========================================================
# Create Quiz Results
#==========================================================




#==========================================================
# Display Results
#==========================================================



#==========================================================
# Display New - Question, Answer Options
#==========================================================

def display_new_question(request):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/index")

        domain = Domain.objects.all()
        question_type = QuestionType.objects.all()
        context = {
            "domains": domain,
            "question_types": question_type
        }
        return render(request, "new_question.html", context)

    return redirect ("/index")


def display_new_option(request):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/index")

        correct = Correct.objects.all()
        question = Question.objects.get("q_id", id)

        context = {
            "correct": correct,
            "question": question
        }
        return render(request, "new_option.html", context)
    return redirect ("/index")


#==========================================================
# Create - Question, Answer Options
#==========================================================

def create_question(request):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        errors = Question.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/question/new')

        user = User.objects.get(id=request.session["u_id"])

        Question.objects.create(name=request.POST['name'])
        Question.objects.create(
            source=request.POST['source'], 
            source_name=request.POST['source_name'], 
            technology=request.POST['technology'], 
            domain=request.POST['domain'], 
            question_type=request.POST['question_type'], 
            question_text=request.POST['question_text'], 
            question_created_by=user
        )
        questionId = Question.objects.last().id
        return redirect ('/question/edit/'+ str(questionId))
    return redirect ('/index')


def create_option(request):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        errors = AnswerOption.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/option/new')

        user = User.objects.get(id=request.session["u_id"])

        question = Question.objects.get(id=request.session["question_id"])

        AnswerOption.objects.create(
            answer_option=request.POST['answer_option'], 
            answer =request.POST['answer'], 
        )
        option = AnswerOption.objects.last()
        option.related_question = question

        return redirect ('/option/edit/'+ str(optionId))
    return redirect ('/index')



#==========================================================
# Display Edit - Question, Answer Options
#==========================================================

def display_edit_question(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        context= {
            "question": Question.objects.get(id=id),
        }
        return render(request, "edit_question.html", context)
    return redirect ('/index')


def display_edit_option(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        context= {
            "option": AnswerOption.objects.get(id=id),
        }
        return render(request, "edit_option.html", context)
    return redirect ('/index')



#==========================================================
# Update - Question, Answer Options
#==========================================================


def update_question(request, id):
    if(request.method=="POST"):
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        errors = Question.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/question/edit/'+ str(id))

        question = Question.objects.get(id=id)
        question.source=request.POST['source']
        question.source_name=request.POST['source_name']
        question.technology=request.POST['technology']
        question.domain=request.POST['domain']
        question.question_type=request.POST['question_type']
        question.question_text=request.POST['question_text']
        question.question_created_by.id['user_id']
        question.save()

        return redirect ('/question/edit/'+ str(id))
    return redirect ('/index')


def update_option(request, id):
    if(request.method=="POST"):
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        errors = AnswerOption.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/option/edit/'+ str(id))

        option = AnswerOption.objects.get(id=id)
        option.answer_option=request.POST['answer_option']
        option.answer=request.POST['answer']
        option.save()

        return redirect ('/option/edit/'+ str(id))
    return redirect ('/index')



#==========================================================
# Delete - Question, Answer Options
#==========================================================

def delete_question(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        question = Question.objects.get(id=id)
        question.delete()
        return redirect ('/quiz/dashboard')
    return redirect ('/index')

def delete_option(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/index")

        option = AnswerOption.objects.get(id=id)
        option.delete()
        return redirect ('/quiz/dashboard')
    return redirect ('/index')