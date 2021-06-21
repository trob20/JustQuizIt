from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.core.exceptions import ObjectDoesNotExist


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
            return redirect("/")

        logged_in_user = user[0]

        if bcrypt.checkpw(password_input.encode(), logged_in_user.password.encode()):
            request.session["u_id"] = logged_in_user.id
            return redirect("/dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    return redirect("/")


def logout(request):
    if request.method=="POST": 
        del request.session["u_id"]
        request.session.clear()
    return redirect("/")


#==========================================================
# Dashboard
#==========================================================


def dashboard(request):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")
        u_id = request.session["u_id"]
        user = User.objects.get(id=u_id)
        quizzes = Quiz.objects.all()

        results = QuizResult.objects.filter(quiz_taken_by = u_id)
        print("***** results *****", results)

        quizzes_taken = []
        for result in results.all():
            quiz_result_id = result.id
            for quiz in result.related_quiz.all():
                quiz_id = quiz.id
                quiz_name = quiz.name
                items = {
                    "quiz_id": quiz_id,
                    "quiz_name": quiz_name,
                    "date_completed": result.updated_at,
                    "score": result.score,
                    "quiz_result_id": quiz_result_id
                }
                quizzes_taken.append(items)
                print("***** quizzes_taken *****", quizzes_taken)

        context = {
            "u_id": u_id,
            "first_name": user.first_name,
            "quizzes": quizzes,
            "results": results,
            "quizzes_taken": quizzes_taken
 
        }
        return render(request, "dashboard.html", context)
    return redirect("/")


#==========================================================
# Exam
#==========================================================

def take_quiz(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        quiz = Quiz.objects.get(id=id)

        context = {
            "first_name": user.first_name,
            "quiz_id": quiz.id,
            "quiz": quiz
        }
        return render(request, "take_quiz.html", context)

    return redirect("/")


def score_quiz(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])

        # get Quiz object
        quiz = Quiz.objects.get(id=id)
        # create Quiz_Result object
        quiz_result = QuizResult.objects.create( quiz_taken_by=user )
        # add Quiz object to QuizResult object
        quiz_result.related_quiz.add(quiz)

        for key, value in request.POST.items():
            # key = question id, value = answer_option id

            # skip csrf key/value pair
            csrf = "csrf"
            if csrf in key:
                continue

            # get Question object
            question = Question.objects.get(id=key)
            # get AnswerOption object
            answer_option = AnswerOption.objects.get(id=value)
            # create Answer_Selected object
            answer_selected = AnswerSelected.objects.create( answer=value, related_result=quiz_result, related_question=question, related_answer_option=answer_option )

            # print("value: ", value)
            # print("option: ", answer_option.id)
            # print("correct: ", answer_option.correct)

            if answer_option.correct == True:
                answer_selected.correct = True
                answer_selected.save()
            else:
                answer_selected.correct = False
                answer_selected.save()
            
        num_questions = quiz.questions.count()
        num_correct = QuizResult.objects.filter(quiz_answers__correct = True, id=quiz_result.id).count()

        score = round(num_correct / num_questions * 100)
        quiz_result.score = score
        quiz_result.save()
        # print("quiz_result.score: ", quiz_result.score)
        # print("num_questions: ", num_questions, "num_correct: ", num_correct, "quiz_result.score: ", quiz_result.score)

        return redirect('/exam/display_result/' + str(quiz_result.id))

    return redirect("/")


def display_one_result(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        quiz_result = QuizResult.objects.get(id=id)
        quiz_id = quiz_result.related_quiz.first().id
        quiz = Quiz.objects.get(id=quiz_id)
        
        questions = []      
        for question in quiz.questions.all():
            question_id = question.id
            questionObject = Question.objects.get(id=question_id)
            answer_selected_id = 0
            quiz_result_query_set = questionObject.question_answered.all().filter(related_result = quiz_result.id)
            for record in quiz_result_query_set:
                answer_selected_id = record.id

            try:
                answer_selected_object = AnswerSelected.objects.get(id=answer_selected_id)
                selected_option_id = answer_selected_object.answer
            except ObjectDoesNotExist:
                selected_option_id = 0

            answer_options = []
            for option in question.answer_options.all():

                answer_result = ""
                answer_color = ""
                if option.correct == True and option.id == selected_option_id:
                    answer_result = "Your answer / Correct!"
                    answer_color = "Both"
                elif option.correct == True and option.id != selected_option_id: 
                        answer_result = "Correct answer"
                        answer_color = "Correct"
                elif option.correct == False and option.id == selected_option_id: 
                        answer_result = "Your answer"
                        answer_color = "Incorrect"

                result = {
                    "answer_option": option.answer_option,
                    "answer_result": answer_result,
                    "answer_color": answer_color
                }
                answer_options.append(result)

                # print("****** START ******")
                # print("option.correct", option.correct)
                # print("option.id", option.id)
                # print("selected_option_id", selected_option_id)
                # print("answer_result", answer_result)
                
            question_set = {
                "question_text": question.question_text,
                "answer_options": answer_options
            }
            questions.append(question_set)

        # print("***** QUESTIONS *****", questions)
        context = {
            "first_name": user.first_name,
            "score": quiz_result.score,
            "quiz_id": quiz.id,
            "quiz_name": quiz.name,
            "questions": questions
        }
        return render(request, "quiz_result.html", context)

    return redirect("/")



def display_all_results(request):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        result = QuizResult.objects.get(id=id)

        context = {
            "first_name": user.first_name,
            "result": result
        }
        return render(request, "display_results.html", context)

    return redirect("/")



#==========================================================
# Quiz
#==========================================================

def new_quiz(request):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        user = User.objects.get(id=u_id)
        
        questions = Question.objects.all()  

        context = {
            "first_name": user.first_name,
            "questions": questions
        }
        return render(request, "new_quiz.html", context)

    return redirect('/')


def create_quiz(request):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        # errors = Quiz.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/quiz/display_quiz')

        user = User.objects.get(id=request.session["u_id"])
        
        quiz = Quiz.objects.create(
            name=request.POST["quiz_name"], 
            created_by=user
        )

        questions_added = request.POST.getlist("add")
        for question in questions_added:
            quiz.questions.add(question)

        return redirect('/quiz/edit_quiz/'+ str(quiz.id))
    return redirect('/')

def edit_quiz(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        u_id = request.session["u_id"]

        context= {
            "first_name": user.first_name,
            "quiz": Quiz.objects.get(id=id),
        }
        return render(request, "edit_quiz.html", context)
    return redirect('/')


def update_quiz(request, id):
    if request.method=="POST":
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        errors = Quiz.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quiz/edit/'+ str(id))

        quiz = Quiz.objects.get(id=id)
        quiz.name=request.POST['name']
        quiz.created_by=request.POST['u_id']
        question.save()

        return redirect('/quiz/edit/'+ str(id))
    return redirect('/')


def delete_quiz(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        quiz = Quiz.objects.get(id=id)
        quiz.delete()

        return redirect('/dashboard')
    return redirect('/')



#==========================================================
# Questions
#==========================================================

def question_bank(request):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        questions = Question.objects.all()  

        context = {
            "first_name": user.first_name,
            "questions": questions
        }
        return render(request, "question_bank.html", context)

    return redirect('/')

def new_question(request):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == 'no u_id': 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])

        domain = Domain.objects.all()
        context = {
            "first_name": user.first_name,
            "domains": domain,
        }
        return render(request, "new_question.html", context)
    return redirect("/")


def create_question(request):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        # errors = Question.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/display_question')

        user = User.objects.get(id=request.session["u_id"])

        question = Question.objects.create(
            source=user.first_name, 
            technology=request.POST['technology'], 
            domain=request.POST['domain'], 
            question_text=request.POST['question_text'], 
            question_created_by=user
        )
        
        return redirect('/question/edit_question/'+ str(question.id))
    return redirect('/')


def edit_question(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        question = Question.objects.get(id=id)
        domain = Domain.objects.all()

        context= {
            "first_name": user.first_name,
            "question": question,
            "domains": domain, 
            "q_id": question.id
        }
        return render(request, "edit_question.html", context)
    return redirect('/')


def update_question(request, id):
    if request.method=="POST":
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        # errors = Question.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/edit/'+ str(id))

        user = User.objects.get(id=request.session["u_id"])

        question = Question.objects.get(id=id)
        question.source=user.first_name
        question.technology=request.POST['technology']
        question.domain=request.POST['domain']
        question.question_text=request.POST['question_text']
        question.save()

        return redirect('/question/question_bank')
    return redirect('/')


def delete_question(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        question = Question.objects.get(id=id)
        question.delete()
        return redirect('/question/question_bank')
    return redirect('/')



#==========================================================
# Answer Options
#==========================================================

def new_option(request, id):
    if request.method=="GET": 
        sessionTest = request.session.get("u_id", "no u_id")
        if sessionTest == "no u_id": 
            return redirect("/")

        user = User.objects.get(id=request.session["u_id"])
        question = Question.objects.get(id=id)

        context = {
            "first_name": user.first_name,
            "question": question
        }
        return render(request, "new_option.html", context)
    return redirect("/")


def create_option(request, id):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        # errors = AnswerOption.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/question/display_option/'+ str(id)')

        question = Question.objects.get(id=id)

        correct_selected = False
        correct_option = request.POST.getlist("correct")

        for correct in correct_option:
            if request.POST['correct'] is None:
                correct_selected = False
            else:
                correct_selected = True

        option = AnswerOption.objects.create(
            answer_option=request.POST['answer_option'], 
            correct = correct_selected,
            related_question = question
        )
        return redirect('/question/edit_question/' + str(id))
    return redirect('/')


def edit_option(request, id, q_id):
    if request.method=="GET": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")
        
        user = User.objects.get(id=request.session["u_id"])
        question = Question.objects.get(id=q_id)

        context= {
            "first_name": user.first_name,
            "option": AnswerOption.objects.get(id=id),
            "question": question,
            "q_id": question.id
        }
        return render(request, "edit_option.html", context)
    return redirect('/')


def update_option(request, id, q_id):
    if request.method=="POST":
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        # errors = AnswerOption.objects.basic_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/option/edit/'+ str(id))

        question = Question.objects.get(id=q_id)

        correct_selected = False
        correct_option = request.POST.getlist("correct")

        for correct in correct_option:
            if request.POST['correct'] is None:
                correct_selected = False
            else:
                correct_selected = True

        option = AnswerOption.objects.get(id=id)
        option.answer_option = request.POST['answer_option']
        option.correct = correct_selected
        option.save()

        return redirect('/question/edit_question/' + str(q_id))
    return redirect('/')


def delete_option(request, id, q_id):
    if request.method=="POST": 
        sessionTest = request.session.get('u_id', 'no u_id')
        if sessionTest == 'no u_id': 
            return redirect("/")

        option = AnswerOption.objects.get(id=id)
        option.delete()
        return redirect('/question/edit_question/' + str(q_id))
    return redirect('/')