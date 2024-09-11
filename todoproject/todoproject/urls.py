from django.contrib import admin
from django.urls import path
from todoapp import views
from todoapp.views import ulogin, usignup,  ulogout, urnp
urlpatterns = [
    path('admin/', admin.site.urls),
    path('task_completion_pie_chart/', views.task_completion_pie_chart, name='task_completion_pie_chart'),
    path("", ulogin, name = "ulogin"),
    path("usignup", usignup, name = "usignup"),
    path("ulogout", ulogout, name = "ulogout"),
    path("urnp", urnp, name = "urnp"),
    path('todo_list', views.todo_list, name='todo_list'),  
    path('create/', views.todo_create, name='todo_create'),  
    path('update/<int:id>/', views.todo_update, name='todo_update'),  
    path('delete/<int:id>/', views.todo_delete, name='todo_delete'), 
    
    path('api/todos/', views.todo_api_list, name='todo_api_list'),  
    path('api/todos/<int:id>/', views.todo_api_detail, name='todo_api_detail'),  ]
