from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import forms
from todo.models import Task


User  = get_user_model()

class RegisterForm(UserCreationForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email"].required = True
        
    class Meta:
        model = User
        fields= [
            "username",
            "email"
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)


class UpdateTask(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "due_date",
            "due_time"
        ]