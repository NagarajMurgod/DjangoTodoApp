from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import get_user_model,authenticate, login as django_login, logout as django_logout
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from todo.models import Task
from django.core.serializers import serialize
from todo.choices import StatusChoices
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from todo.forms import RegisterForm,LoginForm,UpdateTask

User = get_user_model()

@csrf_exempt
def register(request):

    if request.method == "GET":
        form = RegisterForm()
        return render(request,template_name="todo/auth/registerForm.html",context={"form":form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid() is False:
            return render(request,template_name="todo/auth/registerForm.html",context={"form":form})
        
        form.save()

        messages.success(request,"Successfully Registered, Please login with Registered credantials")

        return redirect(reverse('login'))

    #     return JsonResponse({
    #         "status" : "error",
    #         "message" : "not found",
    #         "payload" : {}
    #     },status=404)
    
    # request_data = json.loads(request.body)

    # username = request_data.get('username',None)
    # password = request_data.get('password', None)
    # email = request_data.get('email',None)

    # if username is None or password is None or email is None:
    #     return JsonResponse({
    #         "status" : "error",
    #         "message" : "please provide necessary data",
    #         "payload" : {}
    #     },status=400)
    
    # exisiting_user = User.objects.filter(username=username)
    # if exisiting_user.exists():
    #     return JsonResponse({
    #         "status" : "error",
    #         "message" : "user is already exisit",
    #         "payload" : {}
        
    #     },status = 400)

    # user = User(username=username,email=email)
    # user.set_password(raw_password=password)
    # user.save()

    # return JsonResponse({
    #     'status' : 'success',
    #     'message' : 'sucessfuly registered',
    #     'payload' : {
    #         'username' : user.username,
    #         'email' : user.email
    #     }

    # },status = 201)


@csrf_exempt
def login(request):
    
    if request.method == 'GET':
        form = LoginForm()
        return render(request,template_name='todo/auth/login.html',context={'form':form})

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username,password=password)

            if user is not None:
                django_login(request,user)

                if request.POST.get('next') is not None:
                    return redirect(request.POST.get('next'))
                return redirect('/list_task/')
        
        messages.error(request=request,message="Invalid Username and password , please try again")
        return render(request,template_name='todo/auth/login.html',context={'form':form})
    #     return JsonResponse({
    #         "status" : "error",
    #         "message" : "not found",
    #         "payload" : {}
    #     },status=404)
    
    # request_data = json.loads(request.body)
    # username = request_data.get('username')
    # password = request_data.get('password')

    # user=authenticate(username=username,password=password)

    # if user is not None:
    #     django_login(request,user)
    #     return JsonResponse({
    #         "status":"success",
    #         "message" : "successfully loged in",
    #         "payload" : {}
    #     },status = 200)
    # else:
    #     return JsonResponse({
    #         "status" : "failed",
    #         "message":"invalid credentials",
    #         "payload" : {}
    #     },status = 400)


@login_required
def logout(request):

    if request.method == "GET":
        return redirect('/list_task/')
    
    if request.method == 'POST':
        django_logout(request)
        return redirect(reverse('login'))

    # if request.method != 'POST':
    #     return JsonResponse({
    #         "status" : "error",
    #         "message" : "not found",
    #         "payload" : {}
    #     },status=404)
    # django_logout(request)
    # return JsonResponse({
    #     "status" : "success",
    #     "message" : "successfuly loged out",
    #     "payload" : {}
    # },status=201)


@login_required
def createTask(request):

    if request.method == 'POST':
        req_data = request.POST
        user = request.user
        title = req_data.get('title')
        description = req_data.get('description',"")
        status = req_data.get("status")
        due_date = req_data.get("due_date") if req_data["due_date"] else None
        due_time = req_data.get("due_time") if req_data["due_time"] else None

        if status == 'Status':
            status = StatusChoices.PENDING
    
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            due_time=due_time
        )


        # serialize_data = serialize("json",[task],fields={"title","description","created_at","updated_at"})

        # return JsonResponse({
        #     "status" : "success",
        #     "message" : "successfully created the task",
        #     "payload" : json.dumps(serialize_data)[0]
        # },status=201)

        return redirect("/list_task/")


@login_required
@csrf_exempt
def list_create_task(request):
    if request.method == "GET":
        page = request.GET.get("page",1)
        search = request.GET.get("search",None)
        status = request.GET.get("status",None)
        sort_by = request.GET.get("sort", "-created_at")
        task_queryset = Task.objects.filter(user=request.user).order_by(sort_by)

        if search is not None:
            task_queryset = task_queryset.filter(title__icontains=search)
        if status is not None and status != "ALL":
            task_queryset = task_queryset.filter(status=status)

        page_size = 5

        paginator = Paginator(task_queryset,page_size)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        

        next_page,prev_page = "",""

        # if page_obj.has_next():
        #     next_page = page_obj.next_page_number()
        
        # if page_obj.has_previous():
        #     prev_page = page_obj.previous_page_number()
        
        serialize_data = serialize("json",page_obj.object_list)

        # return JsonResponse({
        #     "status" : "scuess",
        #     "message" : "succesfuly retrived the data",
        #     "payload" : {
        #         "count" : page_obj.paginator.count,
        #         "previous" : prev_page,
        #         "next" : next_page,
        #         "result" : json.loads(serialize_data)
        #     }
        # },status=200)
    
        context = {
            "is_paginated" : False,
            "page_obj" : page_obj,
            "paginator" : page_obj.paginator,
            "results" : page_obj.object_list,
            "search_str" : search,
            "is_loged_in": True
        }

        if context["results"]:
            context["is_paginated"] = True
        return render(request, template_name='todo/todo_list.html',context=context)

    else:
        return JsonResponse({
            "status" : "error",
            "message" : "not found",
            "payload" : {}
        },status=404)



@login_required
@csrf_exempt
def retrive_update_delete_task(request,id):
    if request.method == "GET":
        task = Task.objects.filter(user=request.user,id=id).first()
        if task is None:
            response_data = {
                "status" : "error",
                "message" : "task with this id not found",
                "payload" : {}
            }
            return HttpResponse(json.dumps(response_data),content_type="json",status=400)
        
        serialize_data = serialize("json",[task])

        return JsonResponse({
            "status" : "success",
            "message" : "succesfully retrived the data",
            "payload" : json.loads(serialize_data)[0]
        })
    
    # if request.method in ["PUT","PATCH"]:
    #     req_data = json.loads(request.body)

    #     task = Task.objects.filter(user = request.user, id=id).first()

    #     if task is None :
    #         return JsonResponse({
    #             "status" : "error",
    #             "message" : "user id not found",
    #             "payload" : {}
    #         },status=400)
        
    #     for k,v in req_data.items():
    #         setattr(task,k,v)
    #     task.save()

    #     serialize_data = serialize("json",[task])
    #     return JsonResponse({
    #         "status" : "success",
    #         "messge" : "successfuly updated",
    #         "payload" : json.loads(serialize_data)
    #     },status=201)

@login_required
def delete_task(request, id):

    task = Task.objects.filter(id = id)
    if task is None:
        return HttpResponse("not found")
    
    task.delete()
    messages.warning(request=request, message="deleted the task")
    return redirect(reverse('list_task'))


@login_required
def update_task(request,id):

    if request.method == 'POST':
        task = Task.objects.filter(user=request.user , id=id).first()
        if task is None:
            return HttpResponse("Opps something went wrong")

        form = UpdateTask(request.POST,instance=task)

        if form.is_valid():
            form.save()
            messages.info(request=request, message="Successfully Updated the Task")
            return redirect("/list_task/")

        messages.error(request=request, message="something went wrong, please try again")
        return redirect("/list_task/")
    
    else:
        messages.error(request=request, message="Unable to update the task , please try again")
        return redirect("/list_task/")
        

        # task = Task.objects.filter(user=request.user , id=id).first()
        # if task is None:
        #     return HttpResponse("Opps something went wrong")
        # req_data = request.POST


        # due_date = req_data.get("due_date") if req_data["due_date"] else None
        # due_time = req_data.get("due_time") if req_data["due_time"] else None
        
        # task.title = req_data.get('title')
        # task.description = req_data.get('description')
        # task.status=req_data.get("status")
        # task.due_date = due_date
        # task.due_time = due_time

        # task.save()
        # messages.info(request=request, message="updated the task")

        # return redirect(reverse('list_task'))