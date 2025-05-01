from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Movie, Review
from.forms import ReviewForm, RegisterForm, LoginForm
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.db.models import Avg

def movie_list(request):
    movies = Movie.objects.all()
    return render(request,'movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    reviews = Review.objects.filter(movie=movie)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = 0
    return render(request,'movie_detail.html', {'movie': movie,'reviews': reviews, 'average_rating': average_rating})

@login_required
def add_review(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('movie_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})