from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


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