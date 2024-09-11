from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import ToDo, Category
from .forms import ToDoForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from random import randrange
from django.core.mail import send_mail
import matplotlib.pyplot as plt
from io import BytesIO
from django.utils import timezone
from datetime import timedelta 

def urnp(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    else:
        if request.method == "POST":
            un = request.POST.get("un")
            try:
                usr = User.objects.get(username=un)
                pw = ""
                text = "0123456789"
                for i in range(1, 5):
                    pw += text[randrange(len(text))]
                usr.set_password(pw)
                usr.save()
                subject = "Welcome to Sqrt Finder App"
                text = "Thank you for your registration. Your new password is " + str(pw)
                from_email = "akshata.tester@gmail.com"
                to_email = [str(un)]
                send_mail(subject, text, from_email, to_email)
                return redirect("ulogin")
            except User.DoesNotExist:
                msg = "email does not exist"
                return render(request, "urnp.html", {"msg": msg})
        else:
            return render(request, "urnp.html")


def ulogin(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        usr = authenticate(username=un, password=pw)
        if usr is None:
            msg = "invalid credentials"
            return render(request, "ulogin.html", {"msg": msg})
        else:
            login(request, usr)
            return redirect("todo_list")
    else:
        return render(request, "ulogin.html")


def usignup(request):
    if request.user.is_authenticated:
        return redirect("uhome")
    else:
        if request.method == "POST":
            un = request.POST.get("un")
            try:
                usr = User.objects.get(username=un)
                msg = "email already registered"
                return render(request, "usignup.html", {"msg": msg})
            except User.DoesNotExist:
                pw = ""
                text = "0123456789"
                for i in range(1, 5):
                    pw += text[randrange(len(text))]
                usr = User.objects.create_user(username=un, password=pw)
                usr.save()
                subject = "Welcome to Sqrt Finder App"
                text = "Your password is " + str(pw)
                from_email = "akshata.tester@gmail.com"
                to_email = [str(un)]
                send_mail(subject, text, from_email, to_email)
                return redirect("ulogin")
        else:
            return render(request, "usignup.html")


def ulogout(request):
    logout(request)
    return redirect("ulogin")


def todo_list(request):
    
    selected_category = request.GET.get('category')
    if selected_category:
        todos = ToDo.objects.filter(category__id=selected_category)
    else:
        todos = ToDo.objects.all()
    now = timezone.now()
    upcoming_due_date = now + timedelta(days=1)  
    reminders = ToDo.objects.filter(due_date__lte=upcoming_due_date, completed=False)

    categories = Category.objects.all()  
    return render(request, 'todo_list.html', {
        'todos': todos,
        'categories': categories,
        'selected_category': selected_category,
        'reminders': reminders,
    })


def todo_create(request):
    
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = ToDoForm()
    return render(request, 'todo_form.html', {'form': form})


def todo_update(request, id):
    
    todo = get_object_or_404(ToDo, id=id)
    if request.method == "POST":
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = ToDoForm(instance=todo)
    return render(request, 'todo_form.html', {'form': form})


def todo_delete(request, id):
    
    todo = get_object_or_404(ToDo, id=id)
    if request.method == "POST":
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo_confirm_delete.html', {'todo': todo})


def todo_api_list(request):
    
    category_id = request.GET.get('category')
    if category_id:
        todos = ToDo.objects.filter(category__id=category_id).values()
    else:
        todos = ToDo.objects.values()
    return JsonResponse(list(todos), safe=False)


def todo_api_detail(request, id):
    
    todo = get_object_or_404(ToDo, id=id)
    return JsonResponse({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed,
        'category': todo.category.name if todo.category else None,
    })


def todo_api_create(request):
       if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            return JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed,
                'category': todo.category.name if todo.category else None,
            }, status=201)
        return JsonResponse({'error': 'Invalid data'}, status=400)


def task_completion_pie_chart(request):
    
    completed_tasks = ToDo.objects.filter(user=request.user, completed=True).count()
    non_completed_tasks = ToDo.objects.filter(user=request.user, completed=False).count()

    
    labels = ['Completed', 'Not Completed']
    sizes = [completed_tasks, non_completed_tasks]
    colors = ['#4CAF50', '#FF6347'] 
    explode = (0.1, 0)  


    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')  

    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    return HttpResponse(buffer, content_type='image/png')

