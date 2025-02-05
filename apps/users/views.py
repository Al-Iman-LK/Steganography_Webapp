from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'user': request.user
    })

@login_required
def dashboard(request):
    user_files = request.user.steganofile_set.all()
    context = {
        'total_files': user_files.count(),
        'recent_files': user_files.order_by('-created_at')[:5],
        'profile': request.user.profile
    }
    return render(request, 'users/dashboard.html', context)
