from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ArtForm,UserCreationForm,CustomLoginForm, ProfileForm,CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Picture,User, Comment
from django.contrib.auth.decorators import login_required

def gallery(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    arts = Picture.objects.filter(
        Q(title__icontains=q)|
        Q(uploaded_by__username__icontains=q)
    )

    for art in arts:
        art.liked_by_user = False
        if request.user.is_authenticated:
            art.liked_by_user = art.likes.filter(user=request.user).exists()
    art_count = arts.count()
    context={'arts':arts,
             'arts_count':art_count}
    return render(request, 'gallery/gallery.html', context)


@login_required(login_url='login')
def art(request, pk):
    art = Picture.objects.filter(id=pk)
    art = get_object_or_404(Picture, id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.picture = art
            comment.save()
            return redirect('art', pk=pk)
    else:
        form = CommentForm()

    context = {
        'art': art,
        'form': form
    }
    return render(request, 'gallery/art.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        art_id = comment.picture.id
        comment.delete()
        return redirect('art', pk=art_id)
    return redirect('art', pk=comment.picture.id)


def info(request):
    context={}
    return render(request, 'gallery/info.html', context)

@login_required(login_url='login')
def create_art(request):
    form = ArtForm()

    if request.method == 'POST':
        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(commit=False)
            art.uploaded_by = request.user
            art.save()
            return redirect('gallery')

    context={'form': form}
    return render(request, 'gallery/art_form.html', context)


@login_required(login_url='login')
def edit(request,pk):
    art = get_object_or_404(Picture, id=pk)
    form = ArtForm(instance=art)

    if request.user != art.uploaded_by:
        return HttpResponseForbidden('You are not allowed here!!!')

    if request.method == 'POST':
        form = ArtForm(request.POST,request.FILES, instance=art)
        if form.is_valid():
            form.save()
            return redirect('myarts')


    context={'form':form}
    return render(request, 'gallery/art_form.html', context)


@login_required(login_url='login')
def delete(request, pk):
    art = Picture.objects.get(id=pk)

    if request.user != art.uploaded_by:
        return HttpResponseForbidden('You are not allowed here!!!')
    
    if request.method == 'POST':
        art.delete()
        return redirect ('profile')
    
    return render(request, 'gallery/delete.html', {'obj':art})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'gallery/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gallery')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'gallery/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('gallery') 

@login_required(login_url='login')
def profile_view(request):
    user_arts = Picture.objects.filter(uploaded_by=request.user)
    liked_items_count = Picture.objects.filter(liked=request.user).count()
    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
        'user_arts': user_arts,
        'art_count': user_arts.count(),
        'liked_items_count': liked_items_count,
    }
    return render(request, 'gallery/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'gallery/edit_profile.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    arts = Picture.objects.filter(uploaded_by=user)
    return render(request, 'gallery/profile.html', {
        'profile_user': user,
        'profile': user.profile,
        'arts': arts
    })


@login_required
def toggle_like(request, pk):
    art = Picture.objects.get(pk=pk) 

    if request.user in art.liked.all():
        art.liked.remove(request.user)
    else:
        art.liked.add(request.user)

    return redirect('art', pk=pk)

@login_required
def liked(request):
    user = request.user
    liked_items = Picture.objects.filter(liked=user)

    return render(request, 'gallery/liked.html', {'liked_items': liked_items})
