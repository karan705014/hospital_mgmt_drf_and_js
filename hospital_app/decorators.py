from functools import wraps
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return redirect(f"/adminpage/login?next={request.path}")
        response = view_func(request, *args, **kwargs)

        # cache disable
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper


def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'doctor_id' not in request.session:
            return redirect(f"/doctor/login/?next={request.path}")
        response = view_func(request, *args, **kwargs)

        # cache disable
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper
