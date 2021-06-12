from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('dashboard', views.dashboard),

    path('quiz/add_question', views.add_question),
    path('quiz/add_option/<int:id>', views.add_option),

    path('quiz/create_question', views.create_question),
    path('quiz/create_option/<int:id>', views.create_option),

    path('quiz/edit_question/<int:id>', views.edit_question),
    path('quiz/edit_option/<int:id>', views.edit_option),    

    path('quiz/update_question/<int:id>', views.update_question),
    path('quiz/update_option/<int:id>', views.update_option),  

    path('quiz/delete_question/<int:id>', views.delete_question),
    path('quiz/delete_option/<int:id>', views.delete_option),  

]