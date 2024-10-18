from django.shortcuts import render


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser, Role

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser

# Register view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser, Role

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='login')  # Only allow superusers or admins to access this view
def user_list(request):
    users = CustomUser.objects.all()
    roles = Role.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users, 'roles': roles})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def assign_role(request, user_id, role_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    role = get_object_or_404(Role, pk=role_id)
    user.roles.add(role)
    messages.success(request, f"{role.name} role assigned to {user.username}.")
    return redirect('user_list')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def remove_role(request, user_id, role_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    role = get_object_or_404(Role, pk=role_id)
    user.roles.remove(role)
    messages.success(request, f"{role.name} role removed from {user.username}.")
    return redirect('user_list')

def no_permission(request):
    return render(request, 'accounts/no_permission.html')


'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages

CustomUser = get_user_model()

# Utility to check if the user is a custom admin
def is_custom_admin(user):
    return user.is_admin or user.is_superuser

@login_required
@user_passes_test(is_custom_admin)  # Only allow custom admins to access this view
def user_list(request):
    """
    View to list all users and allow custom admins to assign roles.
    """
    users = CustomUser.objects.all()  # Get all users in the system
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(is_custom_admin)  # Only allow custom admins to access this view
def assign_role(request, user_id, role):
    """
    View to assign or remove a role (moderator, feedback contributor) from a user.
    """
    user = get_object_or_404(CustomUser, pk=user_id)

    if role == 'moderator':
        user.is_moderator = not user.is_moderator  # Toggle the role
    elif role == 'feedback':
        user.is_feedback_contributor = not user.is_feedback_contributor  # Toggle the role
    else:
        messages.error(request, "Invalid role specified.")
        return redirect('user_list')

    user.save()
    messages.success(request, f"User {user.username} role updated successfully.")
    return redirect('user_list')
'''