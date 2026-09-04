from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Superuser is treated as Owner
            if user.is_superuser:
                return redirect('owner_dashboard')

            # Get user's profile and role
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:

                logout(request)

                return render(
                    request,
                    'accounts/login.html',
                    {
                        'error': 'No role has been assigned to this user.'
                    }
                )

            # Get role
            role = profile.role

            # Redirect according to role
            if role == 'owner':
                return redirect('owner_dashboard')

            elif role == 'staff':
                return redirect('staff_dashboard')

            elif role == 'customer':
                return redirect('customer_dashboard')

            elif role == 'supplier':
                return redirect('supplier_dashboard')

            elif role == 'rider':
                return redirect('rider_dashboard')

            # If role is invalid
            logout(request)

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid user role.'
                }
            )

        # Wrong username/password
        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect('home')


# =========================================================
# OWNER DASHBOARD
# =========================================================

@login_required
def owner_dashboard(request):

    # Superuser can access Owner Dashboard
    if request.user.is_superuser:
        return render(
            request,
            'dashboards/owner.html'
        )

    # Check normal user's role
    try:
        profile = UserProfile.objects.get(
            user=request.user
        )
    except UserProfile.DoesNotExist:
        return redirect('login')

    if profile.role != 'owner':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboards/owner.html'
    )


# =========================================================
# STAFF DASHBOARD
# =========================================================

@login_required
def staff_dashboard(request):

    if request.user.is_superuser:
        return redirect('owner_dashboard')

    try:
        profile = UserProfile.objects.get(
            user=request.user
        )
    except UserProfile.DoesNotExist:
        return redirect('login')

    if profile.role != 'staff':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboards/staff.html'
    )


# =========================================================
# CUSTOMER DASHBOARD
# =========================================================

@login_required
def customer_dashboard(request):

    if request.user.is_superuser:
        return redirect('owner_dashboard')

    try:
        profile = UserProfile.objects.get(
            user=request.user
        )
    except UserProfile.DoesNotExist:
        return redirect('login')

    if profile.role != 'customer':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboards/customer.html'
    )


# =========================================================
# SUPPLIER DASHBOARD
# =========================================================

@login_required
def supplier_dashboard(request):

    if request.user.is_superuser:
        return redirect('owner_dashboard')

    try:
        profile = UserProfile.objects.get(
            user=request.user
        )
    except UserProfile.DoesNotExist:
        return redirect('login')

    if profile.role != 'supplier':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboards/supplier.html'
    )


# =========================================================
# RIDER DASHBOARD
# =========================================================

@login_required
def rider_dashboard(request):

    if request.user.is_superuser:
        return redirect('owner_dashboard')

    try:
        profile = UserProfile.objects.get(
            user=request.user
        )
    except UserProfile.DoesNotExist:
        return redirect('login')

    if profile.role != 'rider':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboards/rider.html'
    )


# =========================================================
# REDIRECT USER TO THEIR CORRECT DASHBOARD
# =========================================================

def redirect_user_by_role(role):

    if role == 'owner':
        return redirect('owner_dashboard')

    elif role == 'staff':
        return redirect('staff_dashboard')

    elif role == 'customer':
        return redirect('customer_dashboard')

    elif role == 'supplier':
        return redirect('supplier_dashboard')

    elif role == 'rider':
        return redirect('rider_dashboard')

    return redirect('login')