from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # If user is already logged in, send them to their dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('owner_dashboard')

        try:
            profile = UserProfile.objects.get(user=request.user)
            return redirect_user_by_role(profile.role)

        except UserProfile.DoesNotExist:
            logout(request)
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'No role has been assigned to this user.'
                }
            )

    # Handle login form submission
    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Check empty fields
        if not username or not password:
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'TEST: Invalid username or password.',
                    'username': username
                }
            )

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # =================================================
        # SUCCESSFUL LOGIN
        # =================================================

        if user is not None:

            login(request, user)

            # Superuser = Owner
            if user.is_superuser:
                return redirect('owner_dashboard')

            # Get user's profile
            try:
                profile = UserProfile.objects.get(user=user)

            except UserProfile.DoesNotExist:

                logout(request)

                return render(
                    request,
                    'accounts/login.html',
                    {
                        'error': 'No role has been assigned to this user.',
                        'username': username
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

            # Invalid role
            logout(request)

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid user role.',
                    'username': username
                }
            )

        # =================================================
        # WRONG USERNAME OR PASSWORD
        # =================================================

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.',
                'username': username
            }
        )

    # =====================================================
    # NORMAL GET REQUEST
    # =====================================================

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
            'dashboard/owner.html'
        )

    try:
        profile = UserProfile.objects.get(
            user=request.user
        )

    except UserProfile.DoesNotExist:
        logout(request)
        return redirect('login')

    # Only owner can access
    if profile.role != 'owner':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/owner.html'
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
        logout(request)
        return redirect('login')

    # Only staff can access
    if profile.role != 'staff':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/staff.html'
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
        logout(request)
        return redirect('login')

    # Only customer can access
    if profile.role != 'customer':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/customer.html'
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
        logout(request)
        return redirect('login')

    # Only supplier can access
    if profile.role != 'supplier':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/supplier.html'
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
        logout(request)
        return redirect('login')

    # Only rider can access
    if profile.role != 'rider':
        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/rider.html'
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
