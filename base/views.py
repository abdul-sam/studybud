from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
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

    context = {}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    topic = request.GET.get('q')
    q = topic if topic != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(pk=int(pk))
    context = {'room': room}
    return render(request, 'base/room.html', context)


def new_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = { 'form': form }
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/room_form.html', context)


def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = { 'obj': room }
    return render(request, 'base/delete_room.html', context)
