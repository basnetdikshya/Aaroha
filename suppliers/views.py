from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Supplier


# =========================================================
# SUPPLIER ACCESS CHECK
# =========================================================

def supplier_access(request):

    if request.user.is_superuser:
        return True

    try:
        profile = request.user.userprofile
    except Exception:
        return False

    return profile.role in ['owner', 'staff']


# =========================================================
# SUPPLIER LIST
# =========================================================

@login_required
def supplier_list(request):

    if not supplier_access(request):
        return redirect('home')

    suppliers = Supplier.objects.all().order_by('-created_at')

    return render(
        request,
        'suppliers/supplier_list.html',
        {
            'suppliers': suppliers
        }
    )


# =========================================================
# ADD SUPPLIER
# =========================================================


@login_required
def add_supplier(request):

    if not supplier_access(request):
        return redirect('home')

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        status = request.POST.get('status', 'Active').strip()

        Supplier.objects.create(
            name=name,
            company_name=company_name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            status=status
        )

        return redirect('supplier_list')

    return render(
        request,
        'suppliers/add_supplier.html'
    )





# =========================================================
# SUPPLIER DETAIL
# =========================================================

@login_required
def supplier_detail(request, pk):

    if not supplier_access(request):
        return redirect('home')

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    return render(
        request,
        'suppliers/supplier_detail.html',
        {
            'supplier': supplier
        }
    )


# =========================================================
# EDIT SUPPLIER
# =========================================================

@login_required
def edit_supplier(request, pk):

    if not supplier_access(request):
        return redirect('home')

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == 'POST':

        supplier.name = request.POST.get('name')
        supplier.company_name = request.POST.get('company_name')
        supplier.phone = request.POST.get('phone')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.city = request.POST.get('city')
        supplier.status = request.POST.get('status')

        supplier.save()

        return redirect(
            'supplier_detail',
            pk=supplier.pk
        )

    return render(
        request,
        'suppliers/edit_supplier.html',
        {
            'supplier': supplier
        }
    )


# =========================================================
# DELETE SUPPLIER
# =========================================================

@login_required
def delete_supplier(request, pk):

    if not supplier_access(request):
        return redirect('home')

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == 'POST':

        supplier.delete()

        return redirect('supplier_list')

    return render(
        request,
        'suppliers/delete_supplier.html',
        {
            'supplier': supplier
        }
    )

