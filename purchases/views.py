from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from .models import Purchase


# =====================================================
# PURCHASE ACCESS CONTROL
# =====================================================

def purchase_access(request):

    if request.user.is_superuser:
        return True

    try:
        profile = request.user.userprofile
    except Exception:
        return False

    return profile.role in ['owner', 'staff']


# =====================================================
# PURCHASE LIST
# =====================================================

@login_required
def purchase_list(request):

    if not purchase_access(request):
        return redirect('home')

    purchases = (
        Purchase.objects
        .select_related('supplier')
        .prefetch_related('items')
        .order_by('-purchase_date', '-id')
    )

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search = request.GET.get('search', '').strip()

    if search:

        purchases = purchases.filter(
            Q(supplier__name__icontains=search)
            |
            Q(supplier__company_name__icontains=search)
        )

    # -------------------------------------------------
    # STATUS FILTER
    # -------------------------------------------------

    status = request.GET.get('status', '').strip()

    if status in ['Pending', 'Received', 'Cancelled']:

        purchases = purchases.filter(
            status=status
        )

    # -------------------------------------------------
    # PURCHASE SUMMARY
    # -------------------------------------------------

    total_purchases = purchases.count()

    received_purchases = purchases.filter(
        status='Received'
    ).count()

    pending_purchases = purchases.filter(
        status='Pending'
    ).count()

    cancelled_purchases = purchases.filter(
        status='Cancelled'
    ).count()

    total_amount = purchases.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    # -------------------------------------------------
    # PAGINATION
    # -------------------------------------------------

    paginator = Paginator(
        purchases,
        10
    )

    page_number = request.GET.get('page')

    purchases = paginator.get_page(
        page_number
    )

    # -------------------------------------------------
    # CONTEXT
    # -------------------------------------------------

    context = {

        'purchases': purchases,

        'search': search,

        'selected_status': status,

        'total_purchases': total_purchases,

        'received_purchases': received_purchases,

        'pending_purchases': pending_purchases,

        'cancelled_purchases': cancelled_purchases,

        'total_amount': total_amount,

    }

    return render(
        request,
        'purchases/purchase_list.html',
        context
    )


# =====================================================
# ADD PURCHASE
# =====================================================

@login_required
def add_purchase(request):

    if not purchase_access(request):
        return redirect('home')

    from suppliers.models import Supplier
    from products.models import Product

    suppliers = Supplier.objects.filter(
        status='Active'
    ).order_by('name')

    products = Product.objects.filter(
        is_available=True
    ).order_by('name')

    if request.method == 'POST':

        supplier_id = request.POST.get(
            'supplier'
        )

        purchase_date = request.POST.get(
            'purchase_date'
        )

        status = request.POST.get(
            'status'
        )

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        if not supplier_id or not purchase_date:

            return render(
                request,
                'purchases/add_purchase.html',
                {
                    'suppliers': suppliers,
                    'products': products,
                    'error': 'Please select a supplier and purchase date.'
                }
            )

        supplier = get_object_or_404(
            Supplier,
            id=supplier_id
        )

        # -------------------------------------------------
        # CREATE PURCHASE
        # -------------------------------------------------

        with transaction.atomic():

            purchase = Purchase.objects.create(
                supplier=supplier,
                purchase_date=purchase_date,
                status=status or 'Pending',
                notes=notes,
                total_amount=Decimal('0.00')
            )

            total_amount = Decimal('0.00')

            # -------------------------------------------------
            # GET PURCHASE ITEMS
            # -------------------------------------------------

            product_ids = request.POST.getlist(
                'product'
            )

            quantities = request.POST.getlist(
                'quantity[]'
            )

            cost_prices = request.POST.getlist(
                'cost_price[]'
            )

            # -------------------------------------------------
            # CREATE PURCHASE ITEMS
            # -------------------------------------------------

            for index in range(len(product_ids)):

                product_id = product_ids[index]

                if not product_id:
                    continue

                try:

                    quantity = int(
                        quantities[index]
                    )

                    cost_price = Decimal(
                        cost_prices[index]
                    )

                except (
                    ValueError,
                    InvalidOperation,
                    IndexError
                ):

                    continue

                if quantity <= 0 or cost_price < 0:
                    continue

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                item_subtotal = (
                    Decimal(quantity)
                    * cost_price
                )

                purchase.items.create(
                    product=product,
                    quantity=quantity,
                    cost_price=cost_price,
                    subtotal=item_subtotal
                )

                total_amount += item_subtotal

                # -------------------------------------------------
                # ADD STOCK IF RECEIVED
                # -------------------------------------------------

                if purchase.status == 'Received':

                    product.stock += quantity

                    product.save(
                        update_fields=['stock']
                    )

            # -------------------------------------------------
            # SAVE TOTAL
            # -------------------------------------------------

            purchase.total_amount = total_amount

            purchase.save(
                update_fields=['total_amount']
            )

        return redirect(
            'purchase_detail',
            pk=purchase.id
        )

    return render(
        request,
        'purchases/add_purchase.html',
        {
            'suppliers': suppliers,
            'products': products,
        }
    )


# =====================================================
# PURCHASE DETAIL
# =====================================================

@login_required
def purchase_detail(request, pk):

    if not purchase_access(request):
        return redirect('home')

    purchase = get_object_or_404(
        Purchase.objects
        .select_related('supplier')
        .prefetch_related('items__product'),
        pk=pk
    )

    return render(
        request,
        'purchases/purchase_detail.html',
        {
            'purchase': purchase
        }
    )


# =====================================================
# EDIT PURCHASE
# =====================================================

@login_required
def edit_purchase(request, pk):

    if not purchase_access(request):
        return redirect('home')

    from suppliers.models import Supplier
    from products.models import Product

    purchase = get_object_or_404(
        Purchase.objects
        .select_related('supplier')
        .prefetch_related('items__product'),
        pk=pk
    )

    suppliers = Supplier.objects.filter(
        status='Active'
    ).order_by('name')

    products = Product.objects.filter(
        is_available=True
    ).order_by('name')

    if request.method == 'POST':

        supplier_id = request.POST.get(
            'supplier'
        )

        purchase_date = request.POST.get(
            'purchase_date'
        )

        new_status = request.POST.get(
            'status'
        )

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        if not supplier_id or not purchase_date:

            return render(
                request,
                'purchases/edit_purchase.html',
                {
                    'purchase': purchase,
                    'suppliers': suppliers,
                    'products': products,
                    'error': 'Please select a supplier and purchase date.'
                }
            )

        supplier = get_object_or_404(
            Supplier,
            id=supplier_id
        )

        with transaction.atomic():

            # -------------------------------------------------
            # SAVE OLD STATUS
            # -------------------------------------------------

            old_status = purchase.status

            # -------------------------------------------------
            # REMOVE OLD RECEIVED STOCK
            # -------------------------------------------------

            if old_status == 'Received':

                for item in purchase.items.select_related(
                    'product'
                ):

                    product = item.product

                    product.stock = max(
                        0,
                        product.stock - item.quantity
                    )

                    product.save(
                        update_fields=['stock']
                    )

            # -------------------------------------------------
            # DELETE OLD ITEMS
            # -------------------------------------------------

            purchase.items.all().delete()

            # -------------------------------------------------
            # UPDATE PURCHASE
            # -------------------------------------------------

            purchase.supplier = supplier

            purchase.purchase_date = purchase_date

            purchase.status = new_status or 'Pending'

            purchase.notes = notes

            purchase.total_amount = Decimal(
                '0.00'
            )

            purchase.save()

            # -------------------------------------------------
            # GET NEW PURCHASE ITEMS
            # -------------------------------------------------

            total_amount = Decimal(
                '0.00'
            )

            product_ids = request.POST.getlist(
                'product'
            )

            quantities = request.POST.getlist(
                'quantity[]'
            )

            cost_prices = request.POST.getlist(
                'cost_price[]'
            )

            # -------------------------------------------------
            # CREATE NEW ITEMS
            # -------------------------------------------------

            for index in range(len(product_ids)):

                product_id = product_ids[index]

                if not product_id:
                    continue

                try:

                    quantity = int(
                        quantities[index]
                    )

                    cost_price = Decimal(
                        cost_prices[index]
                    )

                except (
                    ValueError,
                    InvalidOperation,
                    IndexError
                ):

                    continue

                if quantity <= 0 or cost_price < 0:
                    continue

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                item_subtotal = (
                    Decimal(quantity)
                    * cost_price
                )

                purchase.items.create(
                    product=product,
                    quantity=quantity,
                    cost_price=cost_price,
                    subtotal=item_subtotal
                )

                total_amount += item_subtotal

                # -------------------------------------------------
                # ADD STOCK IF RECEIVED
                # -------------------------------------------------

                if purchase.status == 'Received':

                    product.stock += quantity

                    product.save(
                        update_fields=['stock']
                    )

            # -------------------------------------------------
            # SAVE TOTAL
            # -------------------------------------------------

            purchase.total_amount = total_amount

            purchase.save(
                update_fields=[
                    'total_amount',
                    'updated_at'
                ]
            )

        return redirect(
            'purchase_detail',
            pk=purchase.id
        )

    return render(
        request,
        'purchases/edit_purchase.html',
        {
            'purchase': purchase,
            'suppliers': suppliers,
            'products': products,
        }
    )


# =====================================================
# DELETE PURCHASE
# =====================================================

@login_required
def delete_purchase(request, pk):

    if not purchase_access(request):
        return redirect('home')

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    if request.method == 'POST':

        with transaction.atomic():

            # -------------------------------------------------
            # REMOVE STOCK IF PURCHASE WAS RECEIVED
            # -------------------------------------------------

            if purchase.status == 'Received':

                for item in purchase.items.select_related(
                    'product'
                ):

                    product = item.product

                    product.stock = max(
                        0,
                        product.stock - item.quantity
                    )

                    product.save(
                        update_fields=['stock']
                    )

            purchase.delete()

        return redirect(
            'purchase_list'
        )

    return render(
        request,
        'purchases/delete_purchase.html',
        {
            'purchase': purchase
        }
    )


# =====================================================
# UPDATE PURCHASE STATUS
# =====================================================

@login_required
def update_purchase_status(request, pk):

    if not purchase_access(request):
        return redirect('home')

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    if request.method == 'POST':

        new_status = request.POST.get(
            'status'
        )

        if new_status not in [
            'Pending',
            'Received',
            'Cancelled'
        ]:

            return redirect(
                'purchase_detail',
                pk=purchase.id
            )

        old_status = purchase.status

        with transaction.atomic():

            # -------------------------------------------------
            # PENDING/CANCELLED → RECEIVED
            # ADD STOCK
            # -------------------------------------------------

            if (
                old_status != 'Received'
                and new_status == 'Received'
            ):

                for item in purchase.items.select_related(
                    'product'
                ):

                    product = item.product

                    product.stock += item.quantity

                    product.save(
                        update_fields=['stock']
                    )

            # -------------------------------------------------
            # RECEIVED → PENDING/CANCELLED
            # REMOVE STOCK
            # -------------------------------------------------

            elif (
                old_status == 'Received'
                and new_status != 'Received'
            ):

                for item in purchase.items.select_related(
                    'product'
                ):

                    product = item.product

                    product.stock = max(
                        0,
                        product.stock - item.quantity
                    )

                    product.save(
                        update_fields=['stock']
                    )

            purchase.status = new_status

            purchase.save(
                update_fields=[
                    'status',
                    'updated_at'
                ]
            )

        return redirect(
            'purchase_detail',
            pk=purchase.id
        )

    return redirect(
        'purchase_detail',
        pk=purchase.id
    )

