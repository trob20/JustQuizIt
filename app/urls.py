from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),

    path('exam/take_quiz/<int:id>', views.take_quiz),
    path('exam/score_quiz/<int:id>', views.score_quiz),
    path('exam/display_result/<int:id>', views.display_one_result),
    path('exam/display_results', views.display_all_results),

    path('quiz/new_quiz', views.new_quiz),
    path('quiz/create_quiz', views.create_quiz),  
    path('quiz/edit_quiz/<int:id>', views.edit_quiz),
    path('quiz/update_quiz/<int:id>', views.update_quiz),
    path('quiz/delete_quiz/<int:id>', views.delete_quiz),

    path('question/question_bank', views.question_bank),
    path('question/new_question', views.new_question),
    path('question/create_question', views.create_question),
    path('question/edit_question/<int:id>', views.edit_question),
    path('question/update_question/<int:id>', views.update_question),
    path('question/delete_question/<int:id>', views.delete_question),

    path('option/new_option/<int:id>', views.new_option),
    path('option/create_option/<int:id>', views.create_option),
    path('option/edit_option/<int:id>/<int:q_id>', views.edit_option), 
    path('option/update_option/<int:id>/<int:q_id>', views.update_option), 
    path('option/delete_option/<int:id>/<int:q_id>', views.delete_option),  

]