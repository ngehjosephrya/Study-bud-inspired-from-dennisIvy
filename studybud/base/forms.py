from django.forms import ModelForm
from .models import Room, Profile
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta:
        model = Room
        #fields = ['name', 'topic', 'description']
        fields = '__all__'
        exclude = ['host', 'participants']

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email',]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username','email', 'image', 'about']
        include = ['username', 'email']
        
