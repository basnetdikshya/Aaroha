from django.shortcuts import render, redirect,get_object_or_404
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

        # -----------------------------------------------------
        # EMPTY FIELDS
        # -----------------------------------------------------

        if not username or not password:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Please enter both username and password.',
                    'username': username,
                }
            )

        # -----------------------------------------------------
        # AUTHENTICATE USER
        # -----------------------------------------------------

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("LOGIN DEBUG")
        print("Username:", username)
        print("User:", user)

        # -----------------------------------------------------
        # WRONG USERNAME OR PASSWORD
        # -----------------------------------------------------

        if user is None:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password.',
                    'username': username,
                }
            )

        # -----------------------------------------------------
        # CHECK ACCOUNT STATUS
        # -----------------------------------------------------

        if not user.is_active:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Your account is inactive. Please contact the administrator.',
                    'username': username,
                }
            )

        # -----------------------------------------------------
        # LOGIN SUCCESS
        # -----------------------------------------------------

        login(request, user)

        print("LOGIN SUCCESS")
        print("Logged in user:", request.user)

        # -----------------------------------------------------
        # SUPERUSER = OWNER
        # -----------------------------------------------------

        if user.is_superuser:

            return redirect('owner_dashboard')

        # -----------------------------------------------------
        # GET USER PROFILE
        # -----------------------------------------------------

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
                    'username': username,
                }
            )

        # -----------------------------------------------------
        # GET ROLE
        # -----------------------------------------------------

        role = profile.role

        # -----------------------------------------------------
        # REDIRECT ACCORDING TO ROLE
        # -----------------------------------------------------

        if role == 'owner':

            return redirect(
                'owner_dashboard'
            )

        elif role == 'staff':

            return redirect(
                'staff_dashboard'
            )

        elif role == 'customer':

            return redirect(
                'customer_dashboard'
            )

        elif role == 'supplier':

            return redirect(
                'supplier_dashboard'
            )

        elif role == 'rider':

            return redirect(
                'rider_dashboard'
            )

        # -----------------------------------------------------
        # INVALID ROLE
        # -----------------------------------------------------

        logout(request)

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid user role.',
                'username': username,
            }
        )

    # ---------------------------------------------------------
    # GET REQUEST
    # ---------------------------------------------------------

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

# =========================================================
# OWNER / STAFF ORDER MANAGEMENT
# =========================================================

@login_required
def manage_orders(request):

    from orders.models import Order

    # Superuser can access
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-created_at')

        return render(
            request,
            'accounts/manage_orders.html',
            {
                'orders': orders,
            }
        )

    # Check user role
    try:
        profile = UserProfile.objects.get(
            user=request.user
        )

    except UserProfile.DoesNotExist:
        logout(request)
        return redirect('login')

    # Only owner and staff can manage orders
    if profile.role not in ['owner', 'staff']:
        return redirect_user_by_role(profile.role)

    orders = Order.objects.all().order_by('-created_at')

    return render(
        request,
        'accounts/manage_orders.html',
        {
            'orders': orders,
        }
    )


@login_required
def manage_order_detail(request, order_id):

    from django.shortcuts import get_object_or_404
    from orders.models import Order

    # Superuser can access
    if request.user.is_superuser:
        pass

    else:
        # Check user role
        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:
            logout(request)
            return redirect('login')

        # Only owner and staff can manage orders
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            'Pending',
            'Confirmed',
            'Processing',
            'Shipped',
            'Delivered',
            'Cancelled',
        ]

        if new_status in valid_statuses:

            order.status = new_status
            order.save()

        return redirect(
            'manage_order_detail',
            order_id=order.id
        )

    return render(
        request,
        'accounts/manage_order_detail.html',
        {
            'order': order,
        }
    )


# =========================================================
# SALES MANAGEMENT
# =========================================================

@login_required
def sales_management(request):

    from orders.models import Order
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import datetime

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can access sales
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    # -----------------------------------------------------
    # GET ALL ORDERS
    # -----------------------------------------------------

    orders = Order.objects.all().order_by('-created_at')

    # -----------------------------------------------------
    # TOTAL SALES
    # -----------------------------------------------------

    total_sales = (
        Order.objects
        .exclude(status='Cancelled')
        .aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    # -----------------------------------------------------
    # TODAY'S SALES
    # -----------------------------------------------------

    today = timezone.localdate()

    today_sales = (
        Order.objects
        .filter(
            created_at__date=today
        )
        .exclude(status='Cancelled')
        .aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    # -----------------------------------------------------
    # THIS MONTH'S SALES
    # -----------------------------------------------------

    month_start = datetime(
        today.year,
        today.month,
        1
    )

    month_sales = (
        Order.objects
        .filter(
            created_at__gte=month_start
        )
        .exclude(status='Cancelled')
        .aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    # -----------------------------------------------------
    # TOTAL ORDERS
    # -----------------------------------------------------

    total_orders = Order.objects.count()

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'today_sales': today_sales,
        'month_sales': month_sales,
        'total_orders': total_orders,
    }

    return render(
        request,
        'accounts/sales_management.html',
        context
    )


@login_required
def sales_detail(request, order_id):

    from orders.models import Order

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can access sales details
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    # -----------------------------------------------------
    # GET ORDER
    # -----------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id
    )

    # -----------------------------------------------------
    # PAGE
    # -----------------------------------------------------

    return render(
        request,
        'accounts/sales_detail.html',
        {
            'order': order
        }
    )


# =========================================================
# CUSTOMER MANAGEMENT
# =========================================================

@login_required
def customer_management(request):

    from django.contrib.auth.models import User
    from django.db.models import Q

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can manage customers
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    # -----------------------------------------------------
    # GET ALL CUSTOMERS
    # -----------------------------------------------------

    customers = User.objects.filter(
        profile__role='customer'
    ).order_by('-date_joined')

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    if search_query:

        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # -----------------------------------------------------
    # STATUS FILTER
    # -----------------------------------------------------

    status_filter = request.GET.get(
        'status',
        ''
    ).strip()

    if status_filter == 'active':

        customers = customers.filter(
            is_active=True
        )

    elif status_filter == 'inactive':

        customers = customers.filter(
            is_active=False
        )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'customers': customers,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        'accounts/customer_management.html',
        context
    )


# =========================================================
# CUSTOMER STATUS MANAGEMENT
# =========================================================

@login_required
def toggle_customer_status(request, customer_id):

    from django.contrib.auth.models import User

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can change customer status
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    # -----------------------------------------------------
    # GET CUSTOMER
    # -----------------------------------------------------

    customer = get_object_or_404(
        User,
        id=customer_id
    )

    # -----------------------------------------------------
    # MAKE SURE USER IS A CUSTOMER
    # -----------------------------------------------------

    try:

        profile = UserProfile.objects.get(
            user=customer
        )

    except UserProfile.DoesNotExist:

        return redirect('customer_management')

    if profile.role != 'customer':

        return redirect('customer_management')

    # -----------------------------------------------------
    # TOGGLE STATUS
    # -----------------------------------------------------

    customer.is_active = not customer.is_active

    customer.save()

    # -----------------------------------------------------
    # RETURN TO CUSTOMER MANAGEMENT
    # -----------------------------------------------------

    return redirect('customer_management')


# =========================================================
# CUSTOMER DETAIL
# =========================================================

@login_required
def customer_detail(request, user_id):

    from django.contrib.auth.models import User
    from orders.models import Order
    from django.db.models import Sum

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can view customer details
        if profile.role not in ['owner', 'staff']:
            return redirect_user_by_role(profile.role)

    # -----------------------------------------------------
    # GET CUSTOMER
    # -----------------------------------------------------

    customer = get_object_or_404(
        User,
        id=user_id,
        profile__role='customer'
    )

    # -----------------------------------------------------
    # CUSTOMER ORDERS
    # -----------------------------------------------------

    orders = Order.objects.filter(
        user=customer
    ).order_by('-created_at')

    # -----------------------------------------------------
    # CUSTOMER STATISTICS
    # -----------------------------------------------------

    total_orders = orders.count()

    delivered_orders = orders.filter(
        status='Delivered'
    ).count()

    pending_orders = orders.filter(
        status='Pending'
    ).count()

    total_spent = (
        orders.exclude(
            status='Cancelled'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'total_spent': total_spent,
    }

    return render(
        request,
        'accounts/customer_detail.html',
        context
    )


# =========================================================
# RIDER MANAGEMENT
# =========================================================

@login_required
def rider_management(request):

    from django.contrib.auth.models import User

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can manage riders
        if profile.role not in ['owner', 'staff']:

            return redirect_user_by_role(
                profile.role
            )

    # -----------------------------------------------------
    # GET ALL RIDERS
    # -----------------------------------------------------

    riders = User.objects.filter(
        profile__role='rider'
    ).order_by('-date_joined')

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'riders': riders,
    }

    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render(
        request,
        'accounts/rider_management.html',
        context
    )


# =========================================================
# ADD RIDER
# =========================================================

@login_required
def add_rider(request):

    from django.contrib.auth.models import User

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can add riders
        if profile.role not in ['owner', 'staff']:

            return redirect_user_by_role(
                profile.role
            )

    # -----------------------------------------------------
    # HANDLE FORM SUBMISSION
    # -----------------------------------------------------

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        # -------------------------------------------------
        # REQUIRED FIELDS
        # -------------------------------------------------

        if not username or not password:

            return render(
                request,
                'accounts/add_rider.html',
                {
                    'error': 'Username and password are required.',
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )

        # -------------------------------------------------
        # CHECK USERNAME
        # -------------------------------------------------

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'accounts/add_rider.html',
                {
                    'error': 'Username already exists.',
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )

        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        rider = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True
        )

        # -------------------------------------------------
        # CREATE RIDER PROFILE
        # -------------------------------------------------

        UserProfile.objects.create(
            user=rider,
            role='rider'
        )

        # -------------------------------------------------
        # RETURN TO RIDER MANAGEMENT
        # -------------------------------------------------

        return redirect(
            'rider_management'
        )

    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    return render(
        request,
        'accounts/add_rider.html'
    )

# =========================================================
# TOGGLE RIDER STATUS
# =========================================================

@login_required
def toggle_rider_status(request, rider_id):

    from django.contrib.auth.models import User

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can manage riders
        if profile.role not in ['owner', 'staff']:

            return redirect_user_by_role(
                profile.role
            )

    # -----------------------------------------------------
    # GET RIDER
    # -----------------------------------------------------

    rider = get_object_or_404(
        User,
        id=rider_id
    )

    # -----------------------------------------------------
    # VERIFY RIDER ROLE
    # -----------------------------------------------------

    try:

        rider_profile = UserProfile.objects.get(
            user=rider
        )

    except UserProfile.DoesNotExist:

        return redirect('rider_management')

    if rider_profile.role != 'rider':

        return redirect('rider_management')

    # -----------------------------------------------------
    # TOGGLE STATUS
    # -----------------------------------------------------

    rider.is_active = not rider.is_active

    rider.save()

    # -----------------------------------------------------
    # RETURN TO RIDER MANAGEMENT
    # -----------------------------------------------------

    return redirect(
        'rider_management'
    )

# =========================================================
# EDIT RIDER
# =========================================================

@login_required
def edit_rider(request, rider_id):

    from django.contrib.auth.models import User

    # -----------------------------------------------------
    # ACCESS CONTROL
    # -----------------------------------------------------

    if request.user.is_superuser:
        pass

    else:

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )

        except UserProfile.DoesNotExist:

            logout(request)
            return redirect('login')

        # Only owner and staff can edit riders
        if profile.role not in ['owner', 'staff']:

            return redirect_user_by_role(
                profile.role
            )

    # -----------------------------------------------------
    # GET RIDER
    # -----------------------------------------------------

    rider = get_object_or_404(
        User,
        id=rider_id
    )

    # -----------------------------------------------------
    # VERIFY RIDER ROLE
    # -----------------------------------------------------

    try:

        rider_profile = UserProfile.objects.get(
            user=rider
        )

    except UserProfile.DoesNotExist:

        return redirect('rider_management')

    if rider_profile.role != 'rider':

        return redirect('rider_management')

    # -----------------------------------------------------
    # HANDLE FORM SUBMISSION
    # -----------------------------------------------------

    if request.method == 'POST':

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        # -------------------------------------------------
        # UPDATE RIDER INFORMATION
        # -------------------------------------------------

        rider.first_name = first_name
        rider.last_name = last_name
        rider.email = email

        # -------------------------------------------------
        # UPDATE PASSWORD ONLY IF ENTERED
        # -------------------------------------------------

        if password:

            rider.set_password(password)

        rider.save()

        # -------------------------------------------------
        # RETURN TO RIDER MANAGEMENT
        # -------------------------------------------------

        return redirect(
            'rider_management'
        )

    # -----------------------------------------------------
    # DISPLAY EDIT FORM
    # -----------------------------------------------------

    context = {
        'rider': rider,
    }

    return render(
        request,
        'accounts/edit_rider.html',
        context
    )