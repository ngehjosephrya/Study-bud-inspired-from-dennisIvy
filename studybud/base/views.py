from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, ProfileForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator



class LoginPageView(View):
    template_name = 'base/login.html'
    
    def get(self, request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')
        
        context = {'page': page}
        return render(request, self.template_name, context)
    
    def post(self, request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try: 
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password Doesnot exist')
            
        context = {'page': page}
        return render(request, self.template_name, context)
            
# def loginPage(request): 
#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('home')
        
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         try: 
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'Username does not exist')
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username OR password Doesnot exist')
            
#     context = {'page': page}
#     return render(request, 'base/login.html')

class LogOutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('home')

# def logoutUser(request):
#     logout(request)
#     return redirect('home')

class RegisterView(View):
    
    template_name = 'base/login_register.html'
    
    def get(self, request):
        return render(request, self.template_name)
        
    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                messages.success(request, 'User created successfully')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register') 
# def registerUser(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username taken')
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(username=username, password=password1)
#                 user.save()
#                 print('user created')
#                 return redirect('login')

#         else:
#             messages.info(request, 'password not matching..')
#             return redirect('register')
        
        
#     else:
#         return render(request, 'base/login_register.html')

class HomeView(View):
    template_name = 'base/home.html'
    
    def get(self, request):
        q = request.GET.get('q', '')
        
        rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) )#using icontains to search for rooms and the filter object
        
        topics = Topic.objects.all()[0:4]
        room_count = rooms.count() 
        room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
        context = {'rooms': rooms, 
                   'topics': topics,
                   'room_count': room_count,
                   'room_messages': room_messages}
        
        return render(request, self.template_name, context)
        
# def home(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else '' #querying Q to search for rooms
    
#     rooms = Room.objects.filter(
#         Q(topic__name__icontains = q) |
#         Q(name__icontains = q) |
#         Q(description__icontains = q) 
#         )#using icontains to search for rooms and the filter object
    
#     topics = Topic.objects.all()[0:4]
#     room_count = rooms.count() 
#     room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    
    
#     context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
#                'room_messages': room_messages}
#     return render(request, 'base/home.html', context)

class RoomView(View):
    template_name = 'base/room.html'
    
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all().order_by('-created')
        participants = room.participants.all()
        
        context = {'room': room, 'room_messages': room_messages, 'participants': participants}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        message_body = request.POST.get('body')
        
        if message_body:
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = message_body
            )
            room.participants.add(request.user)
        
        return redirect('room', pk=room.id)
            
        
# def room(request, pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all().order_by('-created')
#     participants = room.participants.all()  
#     if request.method == 'POST':
#         message = Message.objects.create(
#             user = request.user,
#             room = room,
#             body = request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room', pk=room.id)
#     context = {'room': room, 'room_messages': room_messages,'participants': participants}
#     return render(request, 'base/room.html', context)

class UserProfileView(View):
    template_name = 'base/profile.html'
    
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {'user': user, 'rooms': rooms,
                   'topics': topics, 'room_messages': room_messages}
        return render(request, self.template_name, context)

# def userProfile(request,pk):
#     user = User.objects.get(id=pk)
#     rooms = user.room_set.all()
#     room_messages = user.message_set.all()
#     topics = Topic.objects.all()
#     context = {'user': user, 'rooms': rooms,
#                'topics': topics, 'room_messages': room_messages}
#     return render(request, 'base/profile.html', context)
 
@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateRoomView(View):
    template_name = 'base/room_form.html'
    

    def get(self, request):
        form = RoomForm()
        topics = Topic.objects.all()
        context = {'form': form, 'topics': topics}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = RoomForm(request.POST)
        topics = Topic.objects.all()
        
        if form.is_valid():
            topic_name = form.cleaned_data.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            
            Room.objects.create(
                host = request.user,
                topic = topic,
                name = form.cleaned_data.get('name'),
                description = form.cleaned_data.get('description')
            )
            return redirect('home')
        context = {'form': form, 'topics': topics}
        return render(request, self.template_name, context)
        

# @login_required(login_url='login')
# def createRoom(request):
#     form = RoomForm()
#     topics = Topic.objects.all()
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
        
#         Room.objects.create(
#             host = request.user,
#             topic = topic,
#             name = request.POST.get('name'),
#             description = request.POST.get('description')
#         )
        
#         return redirect('home')
        
#     context = {'form': form, 'topics': topics}
#     return render(request, 'base/room_form.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateRoomView(View):
    template_name = 'base/room_form.html'
    
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        topics = Topic.objects.all()
        form = RoomForm(instance=room)
        
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        
        context = {'form': form, 'topics': topics, 'room': room}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        topics = Topic.objects.all()
        form = RoomForm(request.POST, instance=room)
         
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        
        if form.is_valid():
            topic_name = form.cleaned_data.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            
            room.topic = topic
            room.name = form.cleaned_data.get('name')
            room.description = form.cleaned_data.get('description')
            room.save()
            
            return redirect('home')
        
        context = {'form': form, 'topics': topics, 'room': room}
        return render(request, self.template_name, context)

# @login_required(login_url='login')
# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)
#     topics = Topic.objects.all()
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here')
        
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
#         form = RoomForm(request.POST, instance=room)
#         room.topic = topic
#         room.name = request.POST.get('name')
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')
    
#     context = {'form': form, 'topics': topics, 'room': room}
#     return render( request, 'base/room_form.html', context )


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteRoomView(View):
    
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        
        if request.method == 'POST':
            room.delete()
            return redirect('home')
        return render(request, 'base/delete.html', {'obj': 'room'})
    
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        
        if request.method == 'POST':
            room.delete()
            return redirect('home')
        return render(request, 'base/delete.html', {'obj': 'room'})
    
        
# @login_required(login_url='login')
# def deleteRoom(request, pk):
#     room = Room.objects.get(id=pk)
    
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here')
    
#     if request.method == 'POST':
#         room.delete()
#         return redirect('home')
#     return render(request, 'base/delete.html', {'obj': 'room'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteMessageView(View):
     template_name = 'base/delete.html'
     
     def get(self, request, pk):
        message = Message.objects.get(id=pk)

        if request.user != message.user:
            return HttpResponse('You are not allowed to do this')

        return render(request, self.template_name, {'obj': message})
     def post(self, request, pk):
        message = Message.objects.get(id=pk)

        if request.user != message.user:
            return HttpResponse('You are not allowed to do this')

        message.delete()
        return redirect('room', pk=message.room.id)

# @login_required(login_url='login')
# def deleteMessage(request, pk):
#     message = Message.objects.get(id=pk)
    
#     if request.user != message.user:
#         return HttpResponse('You are not allowed To do This')
    
#     if request.method == 'POST':
#         message.delete()
#         return redirect('room', pk=message.room.id)
#     return render(request, 'base/delete.html', {'obj': message})
 
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(View):
    template_name = 'base/update-user.html'


    def get(self, request, pk):
        user = User.objects.get(id=pk)

        if request.user != user:
            return HttpResponse('You are not allowed to do this')

        form = ProfileForm(instance=user.profile)
        return render(request, self.template_name, {'form': form})


    def post(self, request, pk):
        user = User.objects.get(id=pk)

        if request.user != user:
            return HttpResponse('You are not allowed to do this')

        form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

        return render(request, self.template_name, {'form': form})
    
# @login_required(login_url='login')
# def updateUser(request, pk):
#     user = User.objects.get(id=pk)
#     if request.user != user:
#         return HttpResponse('You are not allowed To do This')
#     form = ProfileForm(instance=user.profile)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user-profile', pk=user.id)
#         else:
#             print(form.errors)
#     return render(request, 'base/update-user.html', {'form': form})

class TopicPageView(View):
    template_name = 'base/topics.html'

    def get(self, request):
        q = request.GET.get('q', '')  # Use get method with a default value

        topics = Topic.objects.filter(name__icontains=q)
        return render(request, self.template_name, {'topics': topics})
    
# def topicPage(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else '' #querying Q to search for rooms
#     topics = Topic.objects.filter(name__icontains = q)
#     return render (request, 'base/topics.html', {'topics': topics})


class ActivityPageView(View):
    template_name = 'base/activity.html'

    def get(self, request):
        room_messages = Message.objects.all()[:4]
        return render(request, self.template_name, {'room_messages': room_messages})
    
# def activityPage(request):
#     room_messages = Message.objects.all()[0:4]
#     return render (request, 'base/activity.html', {'room_messages': room_messages})

# def profile_image(request):
#     profile = Profile.objects.get(user=request.user)
#     if profile.image and hasattr(profile.image, 'url'):
#         image_url = profile.image.url
#     else:
#         image_url = 'media\default.png' 