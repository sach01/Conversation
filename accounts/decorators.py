from django.shortcuts import redirect
from functools import wraps

'''
def role_required(role_name):
    """
    Decorator to ensure the user has a specific dynamic role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.has_role(role_name):
                return view_func(request, *args, **kwargs)
            return redirect('no_permission')  # Redirect to a no_permission page
        return _wrapped_view
    return decorator
'''


from django.shortcuts import redirect
from functools import wraps

def group_required(group_name):
    """
    Decorator to ensure that the user belongs to a specific group/role.
    Redirects to 'no_permission' page if the user does not belong to the group.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if group_name == 'Moderator' and user.is_moderator:
                    return view_func(request, *args, **kwargs)
                elif group_name == 'Data Collector' and user.is_data_collector:
                    return view_func(request, *args, **kwargs)
                elif group_name == 'Feedback Contributor' and user.is_feedback_contributor:
                    return view_func(request, *args, **kwargs)
            return redirect('no_permission')  # Redirect to a no_permission page
        return _wrapped_view
    return decorator
