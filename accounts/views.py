from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # -----------------------------------------------------
    # LOGIN FORM SUBMITTED
    # -----------------------------------------------------

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # -------------------------------------------------
        # Check empty fields
        # -------------------------------------------------

        if not username or not password:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Please enter both username and password.',
                    'username': username
                }
            )

        # -------------------------------------------------
        # Authenticate username and password
        # -------------------------------------------------

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # -------------------------------------------------
        # Authentication failed
        # -------------------------------------------------

        if user is None:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password.',
                    'username': username
                }
            )

        # -------------------------------------------------
        # Authentication successful
        # -------------------------------------------------

        login(request, user)

        # -------------------------------------------------
        # SUPERUSER = OWNER
        # -------------------------------------------------

        if user.is_superuser:

            return redirect('owner_dashboard')

        # -------------------------------------------------
        # Get UserProfile
        # -------------------------------------------------

        try:

            profile = UserProfile.objects.get(
                user=user
            )

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

        # -------------------------------------------------
        # Get user's role
        # -------------------------------------------------

        role = profile.role

        # -------------------------------------------------
        # Redirect according to role
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Invalid role
        # -------------------------------------------------

        logout(request)

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid user role.',
                'username': username
            }
        )

    # -----------------------------------------------------
    # NORMAL GET REQUEST
    # Always show login page
    # -----------------------------------------------------

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

    # Superuser can access owner dashboard
    if request.user.is_superuser:

        return render(
            request,
            'dashboard/owner.html'
        )

    # Get profile
    try:

        profile = UserProfile.objects.get(
            user=request.user
        )

    except UserProfile.DoesNotExist:

        logout(request)

        return redirect('login')

    # Check role
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

    if profile.role != 'rider':

        return redirect_user_by_role(profile.role)

    return render(
        request,
        'dashboard/rider.html'
    )


# =========================================================
# REDIRECT USER BY ROLE
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

    # Unknown role
    return redirect('login')