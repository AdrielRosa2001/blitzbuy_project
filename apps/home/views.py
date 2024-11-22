import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    context = {}
    return render(request, "home/home.html", context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        context = {} 
        return render(request, "home/login.html", context)

def register_page(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        context = {} 
        return render(request, "home/register.html", context)

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@require_POST
def make_login_default(request):
    data = json.loads(request.body)
    email = data['email_input']
    password = data['password_input']
    try:
        username = User.objects.get(email=email)
        user = authenticate(request, username=username.username, password=password)  # Tenta autenticar com e-mail e senha

        if user is not None:
            login(request, user)  # Realiza o login
            return HttpResponse("Login realizado com sucesso", status=200)  # Resposta para login bem-sucedido
        else:
            return HttpResponse("Login ou senha inválido!", status=401)  # Resposta para falha no login
    except:
        return HttpResponse("Login ou senha inválido!", status=401)  # Resposta para falha no login

@require_POST
def make_register_default(request):
    data = json.loads(request.body)
    username = data['username_input']
    first_name_input = data['first_name_input']
    second_name_input = data['second_name_input']
    email = data['email_input']
    password = data['password_input']
    
    search_user = User.objects.filter(username=username)
    search_email = User.objects.filter(email=email)

    if len(search_user) == 0 and len(search_email) == 0:
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name_input,
                last_name=second_name_input,
                )
            return HttpResponse("Usuário criado!", status=200)
        except Exception as error:
            return HttpResponse(f"Erro ao criar usuário!\n{error}", status=500)
    else:
        if len(search_user) != 0 and len(search_email) != 0:
            return HttpResponse("Usuário e e-mail já utilizados!", status=401)
        elif len(search_user) != 0 and len(search_email) == 0:
            return HttpResponse("Usuário já utilizado!", status=401)
        elif len(search_user) == 0 and len(search_email) != 0:
            return HttpResponse("E-mail já utilizado!", status=401)