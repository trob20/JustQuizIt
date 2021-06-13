from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),

    path('question/display_question', views.display_question),
    path('question/display_option/<int:id>', views.display_option),

    path('question/create_question', views.create_question),
    path('question/create_option/<int:id>', views.create_option),

    path('question/edit_question/<int:id>', views.edit_question),
    path('question/edit_option/<int:id>', views.edit_option),    

    path('question/update_question/<int:id>', views.update_question),
    path('question/update_option/<int:id>', views.update_option),  

    path('question/delete_question/<int:id>', views.delete_question),
    path('question/delete_option/<int:id>', views.delete_option),  

    path('quiz/display_quiz', views.display_quiz),
    path('quiz/create_quiz', views.create_quiz),

    path('quiz/take_quiz/<int:id>', views.take_quiz),
    path('quiz/grade_quiz/<int:id>', views.grade_quiz),
    path('quiz/results/<int:id>', views.results),

]