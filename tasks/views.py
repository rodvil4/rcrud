from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .forms import TaskForm
from .models import Task

# Create your views here.

#def helloworld(request):
#    return HttpResponse("<h1>Hello World! </h1>")

#def helloworld(request):
#    return render(request, 'signup.html')

#def helloworld(request):
#    title = "Hola Mundo "
#    return render(request, 'signup.html', {'mytitle':title})

#def helloworld(request):
#    return render(request, 'signup.html', {'form':UserCreationForm})

def home(request):
    return render(request, 'home.html')

#def signup(request):
#    print(request.POST)   --- podemos ver la información que nos está enviando la forma
#    return render(request, 'signup.html', {'form':UserCreationForm})


#def signup(request):
#    if request.method == 'GET':
#        return render(request, 'signup.html', {
#            'form': UserCreationForm
#        })
#    else:
#        if request.POST['password1'] == request.POST['password2']:
#            # register user
#            try:
#                user = User.objects.create_user(
#                    username=request.POST['username'], password=request.POST['password1'])
#                user.save()
#                return HttpResponse('User created successfully')
#            except:
#                return HttpResponse('Username already exists') 
#        return HttpResponse('Password do not match')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
#                return HttpResponse('User created successfully')
                login(request, user)   # Esto nos crea una cookie con el usuario
                return render(request, 'tasks.html')
                return redirect('tasks')
            except:
                #                return HttpResponse('Username already exists')    -- reemplazamos estás lineas por las que siguen
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username Already Exists'
                })
#        return HttpResponse('Password do not match')
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not Match'
        })


def tasks(request):
#    tasks = Task.objects.all()   # con esto me trae todas las tareas que existen
#    tasks = Task.objects.filter(user=request.user)   # con esto solo me trae las tareas del usuario que está logeado
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)   # con esto solo me trae las tareas del usuario que está logeado y que están pendientes de terminarse
#    return render(request, 'tasks.html')  # esto solo está mandando llamar a la página sin datos
    return render(request, 'tasks.html', {    # Estamos mandando llamar la pagina y le mandamos la tareas que estamos connsultando
        'tasks': tasks
    })

def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
#        print(request.POST
        try:
            form = TaskForm(request.POST)
    #        print(form)   Esto solo nos imprime la forma 
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
    })
    else:
#        print(request.POST)   # con esto escribo lo que nos envia el post!!
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'] )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username o Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
        

