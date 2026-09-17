from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Empty fields
        if not username or not password:
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Please enter both username and password.',
                    'username': username,
                }
            )

        # Authenticate user
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password
        # )

        

        # # Wrong username/password
        # if user is None:
        #     return render(
        #         request,
        #         'accounts/login.html',
        #         {
        #             'error': 'Invalid username or password.',
        #             'username': username,
        #         }
        #     )

        # # Login successful
        # login(request, user)

        # # Superuser = Owner
        # if user.is_superuser:
        #     return redirect('owner_dashboard')


        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("LOGIN DEBUG")
        print("Username:", username)
        print("User:", user)

        if user is None:
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password.',
                    'username': username,
                }
            )

        login(request, user)

        print("LOGIN SUCCESS")
        print("Logged in user:", request.user)

        if user.is_superuser:
            return redirect('owner_dashboard')

        # Get UserProfile
        try:
            profile = UserProfile.objects.get(user=user)

        except UserProfile.DoesNotExist:

            logout(request)

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'No role has been assigned to this user.',
                    'username': username,
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
                'username': username,
            }
        )

    # GET request
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

    from orders.models import Order

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_orders = orders.count()

    pending_orders = orders.filter(
        status='Pending'
    ).count()

    delivered_orders = orders.filter(
        status='Delivered'
    ).count()

    cart = request.session.get('cart', {})

    cart_items = sum(cart.values())

    recent_orders = orders[:5]

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'cart_items': cart_items,
        'recent_orders': recent_orders,
    }

    return render(
        request,
        'accounts/customer_dashboard.html',
        context
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

    return redirect('login')