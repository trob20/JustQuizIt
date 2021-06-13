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
            return redirect("/dashboard")
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
        quiz = Quiz.objects.all()     

        context = {
            "first_name": user.first_name,
            "quizzes": quiz
        }
        return render(request, "dashboard.html", context)
    return redirect ("/")



#==========================================================
# Create Quiz
#==========================================================

def create_quiz(request):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        # errors = Quiz.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/quiz/display_quiz')

        user = User.objects.get(id=request.session["u_id"])

        Quiz.objects.create(
            source="User", 
            source_name=user.first_name, 
            technology=request.POST['technology'], 
            domain=request.POST['domain'], 
            question_type=request.POST['question_type'], 
            question_text=request.POST['question_text'], 
            question_created_by=user
        )
        questionId = Question.objects.last().id
        return redirect ('/question/display_option/'+ str(questionId))
    return redirect ('/')


#==========================================================
# Take Quiz
#==========================================================

def take_quiz(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        quiz = Quiz.objects.get(id=id)

        print("QUIZ1: ", quiz.name)
        print("QUIZ2: ", quiz.questions.all())


        # print("QUIZ3: ", quiz.questions.answer_options.answer_options)

        context = {
            "quiz": quiz
        }
        return render(request, "take_quiz.html", context)

    return redirect ("/")


#==========================================================
# Record Answer
#==========================================================

def record_answer(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        quiz = Quiz.objects.get(id=id)

        return redirect('/quiz/take_quiz/' + id)

    return redirect ("/")


#==========================================================
# Exit Quiz
#==========================================================

def exit_quiz(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        quiz = Quiz.objects.get(id=id)

        # print("QUIZ1: ", quiz.name)
        # print("QUIZ2: ", quiz.questions.question_text)
        # print("QUIZ3: ", quiz.questions.answer_options.answer_options)

        context = {
            "quiz": quiz
        }
        return redirect('/dashboard')

    return redirect ("/")


#==========================================================
# Save Quiz
#==========================================================

def save_quiz(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        user = User.objects.get(id=request.session["u_id"])

        Question.objects.create(
            source="User", 
            source_name=user.first_name, 
            technology=request.POST['technology'], 
            domain=request.POST['domain'], 
            question_type=request.POST['question_type'], 
            question_text=request.POST['question_text'], 
            question_created_by=user
        )

        return redirect('/take_quiz/' + str(id))

    return redirect ("/")



#==========================================================
# Display Results
#==========================================================

def results(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        results = QuizHistory.objects.get(id=id)

        question_type = QuestionType.objects.all()
        context = {
            "domains": domain,
            "question_types": question_type
        }
        return render(request, "add_question.html", context)

    return redirect ("/")








#==========================================================
# Create Question
#==========================================================

def display_question(request):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        domain = Domain.objects.all()
        question_type = QuestionType.objects.all()
        context = {
            "domains": domain,
            "question_types": question_type
        }
        return render(request, "add_question.html", context)

    return redirect ("/")


def create_question(request):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        # errors = Question.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/display_question')

        user = User.objects.get(id=request.session["u_id"])

        Question.objects.create(
            source="User", 
            source_name=user.first_name, 
            technology=request.POST['technology'], 
            domain=request.POST['domain'], 
            question_type=request.POST['question_type'], 
            question_text=request.POST['question_text'], 
            question_created_by=user
        )
        questionId = Question.objects.last().id
        return redirect ('/question/display_option/'+ str(id))
    return redirect ('/')





#==========================================================
# Create Answer Options
#==========================================================


def display_option(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        correct = Correct.objects.all()
        question = Question.objects.get(id=id)

        context = {
            "correct": correct,
            "question": question
        }
        return render(request, "add_option.html", context)
    return redirect ("/")


def create_option(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        # errors = AnswerOption.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/display_option/'+ str(id)')

        user = User.objects.get(id=id)

        question = Question.objects.get(id=id)

        AnswerOption.objects.create(
            answer_option=request.POST['answer_option'], 
            answer =request.POST['answer'], 
        )
        option = AnswerOption.objects.last()
        option.related_question = question

        return redirect ('/dashboard')
    return redirect ('/')



#==========================================================
# Edit Question
#==========================================================

def edit_question(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        context= {
            "question": Question.objects.get(id=id),
        }
        return render(request, "edit_question.html", context)
    return redirect ('/')

def update_question(request, id):
    if(request.method=="POST"):
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

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
    return redirect ('/')




#==========================================================
# Edit Answer Option
#==========================================================

def edit_option(request, id):
    if(request.method=="GET"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        context= {
            "option": AnswerOption.objects.get(id=id),
        }
        return render(request, "edit_option.html", context)
    return redirect ('/')

def update_option(request, id):
    if(request.method=="POST"):
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

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
    return redirect ('/')





#==========================================================
# Delete Question, Answer Options
#==========================================================

def delete_question(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        question = Question.objects.get(id=id)
        question.delete()
        return redirect ('/dashboard')
    return redirect ('/')

def delete_option(request, id):
    if(request.method=="POST"): 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        option = AnswerOption.objects.get(id=id)
        option.delete()
        return redirect ('/dashboard')
    return redirect ('/')