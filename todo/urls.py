
from django.urls import path
from .views import register,login,createTask,logout,list_create_task,retrive_update_delete_task,delete_task,update_task

urlpatterns = [
    path('',list_create_task),
    path('signup/', register, name="register"),
    path('login/', login,name='login'),
    path('logout/',logout,name = 'logout'),
    path('tasks/',createTask,name = "create_task"),
    path("list_task/",list_create_task,name="list_task"),
    path("task/update/<int:id>/", update_task,name="update_task"),
    path('tasks/delete/<int:id>', delete_task,name='delete_task'),
    path("tasks/<int:id>/",retrive_update_delete_task),

]
