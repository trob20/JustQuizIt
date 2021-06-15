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
    if request.method=="POST": 
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
    if request.method=="POST": 
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
    if request.method=="POST": 
        del request.session["u_id"]
        request.session.clear()
    return redirect ("/")


#==========================================================
# Dashboard
#==========================================================


def dashboard(request):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        user = User.objects.get(id=request.session["u_id"])
        quizzes = Quiz.objects.all()     

        context = {
            "u_id": u_id,
            "first_name": user.first_name,
            "quizzes": quizzes
        }
        return render(request, "dashboard.html", context)
    return redirect ("/")


#==========================================================
# Take Quiz
#==========================================================

def take_quiz(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        user = User.objects.get(id=request.session["u_id"])
        quiz = Quiz.objects.get(id=id)

        context = {
            "first_name": user.first_name,
            "quiz": quiz
        }
        return render(request, "take_quiz.html", context)

    return redirect ("/")


#==========================================================
# Grade Quiz
#==========================================================

def grade_quiz(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        user = User.objects.get(id=request.session["u_id"])
        quiz = Quiz.objects.get(id=id)

        result = QuizResult.objects.create(
            quiz_taken_by=user, 
            related_quiz=quiz
        )

        answers = request.POST.getlist("answers_selected")
        for answer in answers:
            answer_selected = AnswerOption.objects.get(id=request.POST['answer_id'])
            related_question = Question.objects.get(id=request.POST['question_id'])
            AnswerSelected.objects.create(
                answer_selected = answer_selected, 
                related_question = related_question, 
                related_result = result
            )
        return redirect('quiz/results/' + str(quiz_result.id))

    return redirect ("/")


#==========================================================
# Results
#==========================================================

def results(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect ("/")

        user = User.objects.get(id=request.session["u_id"])
        result = QuizResult.objects.get(id=id)

        #question_count = Question.objects.filter(username='myname', status=0).count()

        # correct_answer  = result.quiz_answers.related_question.answer_options (find option with correct = True)
        # answer_selected = result.quiz_answers.answer_selected.correct


        # if correct_answer == answer_selected:
        #     correct = true
        #     correct_count++
        # else:
        #     correct = false
        #     incorrect_count++

        # score = correct_count / question_count


        context = {
            "first_name": user.first_name,
            "result": result
        }
        return render(request, "results.html", context)

    return redirect ("/")



#==========================================================
# Display Quiz
#==========================================================


def display_quiz(request):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        u_id = request.session["u_id"]
        user = User.objects.get(id=u_id)
        
        questions = Question.objects.all()  

        context = {
            "first_name": user.first_name,
            "questions": questions
        }
        return render(request, "create_quiz.html", context)

    return redirect ('/')

#==========================================================
# Create Quiz
#==========================================================

def create_quiz(request):
    if request.method=="POST": 
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
            source=user.first_name, 
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
# Create Question
#==========================================================

def display_question(request):
    if request.method=="GET": 
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
    if request.method=="POST": 
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
    if request.method=="GET": 
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
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        # errors = AnswerOption.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/display_option/'+ str(id)')

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
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        context= {
            "question": Question.objects.get(id=id),
        }
        return render(request, "edit_question.html", context)
    return redirect ('/')

def update_question(request, id):
    if request.method=="POST":
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
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        context= {
            "option": AnswerOption.objects.get(id=id),
        }
        return render(request, "edit_option.html", context)
    return redirect ('/')

def update_option(request, id):
    if request.method=="POST":
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
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        question = Question.objects.get(id=id)
        question.delete()
        return redirect ('/dashboard')
    return redirect ('/')

def delete_option(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect ("/")

        option = AnswerOption.objects.get(id=id)
        option.delete()
        return redirect ('/dashboard')
    return redirect ('/')