from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Define department-specific content
    department_content = {
        'CSE': "Welcome to the Computer Science Department! Here are some resources for programming, AI, and software development.",
        'ECE': "Welcome to the Electronics and Communication Department! Explore circuits, embedded systems, and communication technologies.",
        'MECH': "Welcome to Mechanical Engineering! Get insights into thermodynamics, manufacturing, and automation.",
    }

    # Get content based on user’s department
    user_department = user_profile.department
    content = department_content.get(user_department, "Welcome! Explore our resources.")

    return render(request, 'home/dashboard.html', {
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'content': content
    })
