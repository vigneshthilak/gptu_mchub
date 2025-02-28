from django.shortcuts import render, redirect
from home.models import UserProfile
from django.contrib.auth.models import User
from django.db import connection

def dashboard(request):
    user_id = request.session.get("user_id")  # Get logged-in user ID from session

    if not user_id:
        return redirect("home:login")  # Redirect to login if not authenticated

    # Fetch user details from the database
    query = "SELECT * FROM home_userprofile WHERE user_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        user = cursor.fetchone()

    if user:
        context = {
            "first_name": user[1],  # Assuming first_name is at index 0
            "last_name": user[2],   # Assuming last_name is at index 1
            "department": user[7],  # Assuming department is at index 2
            "user_category": user[8],  # Assuming userCategory is at index 3
        }
        return render(request, "users/dashboard.html", context)
    else:
        # If user not found in DB (which shouldn't happen normally), clear session and redirect
        request.session.flush()
        return redirect("home:login")


def logout(request):
    request.session.flush()
    return redirect('home:index')