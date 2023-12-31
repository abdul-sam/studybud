from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Room, Topic
from .forms import RoomForm, UserForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, 'you are already logged in!!')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    context = { 'page': page }
    return render(request, 'base/login_register.html', context)


def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error was occurred during the registration')

    context = { 'form': form }
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = { 'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics }
    return render(request, 'base/profile.html', context)


def home(request):
    topic = request.GET.get('q')
    q = topic if topic != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(pk=int(pk))
    room_messages = room.message_set.all().order_by('-created_at')
    participants = room.participants.all()
    participant_count = participants.count()


    if request .method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = { 'room': room, 'room_messages': room_messages,
               'participants': participants, 'participant_count': participant_count }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def new_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        

    context = { 'form': form, 'topics': topics }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room!!')
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = { 'form': form, 'topics': topics, 'room': room }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(pk=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete this room!!')
        return redirect('home')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = { 'obj': room }
    return render(request, 'base/delete_room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(pk=pk)

    if request.user != message.user:
        messages.error(request, 'You are not allowed to delete this message!!')
        return redirect('home')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = { 'obj': message }
    return render(request, 'base/delete_room.html', context)


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)

    context = {'form': form}
    return render(request, 'base/update_profile.html', context)


def topic_list(request):
    topic = request.GET.get('q')
    q = topic if topic != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_list(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)