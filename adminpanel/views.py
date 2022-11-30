from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache

from django.db.models import Q 

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from accounts.models import Account
from store.models import Product, Variation, ReviewRating
from orders.models import Order
from category.models import Category

from adminpanel.forms import ProductForm, CategoryForm, VariationForm



@never_cache
@login_required(login_url='manager_login')
def manager_dashboard(request):
    if request.user.is_admin:

        user_count = Account.objects.filter(is_admin=False).count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.filter(is_ordered=True).count()
        category_count = Category.objects.all().count()


        context = {
            'user_count'    : user_count,
            'product_count' : product_count,
            'order_count'   : order_count,
            'category_count' : category_count,

        }

    return render(request, 'manager/manager_dashboard.html', context)




# Manage Variation
@never_cache
@login_required(login_url='manager_login')
def manage_variation(request):
  if request.user.is_admin: 
    if request.method == 'POST':
      keyword = request.POST['keyword']
      variations = Variation.object.filter(Q(product__product_name__icontains=keyword) | Q(variation_catagory__icontains=keyword) | Q(variation_value__icontains=keyword)).order_by('id')
    
    else:
      variations = Variation.object.all().order_by('id')
    
    paginator = Paginator(variations, 5)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)
    
    context = {
      'variations': paged_variations
    }
    return render(request, 'manager/variation_management.html', context)

  else:
    return redirect('home')



@never_cache
@login_required(login_url='manager_login')
def delete_variation(request, variation_id):
    if request.user.is_admin:
        variations = Variation.object.get(id=variation_id)
        variations.delete()
        return redirect('manage_variation')

    else:
        return redirect('home')


#Add Variation
@never_cache
@login_required(login_url='manager_login')
def add_variation(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = VariationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_variation')

        else:
            form = VariationForm()

        context = {
            'form': form
        }
        return render(request, 'manager/add_variation.html', context)

    else:
        return redirect('home')



# Update Variation
@never_cache
@login_required(login_url='manager_login')
def update_variation(request, variation_id):
  if request.user.is_admin:
    variations = Variation.object.get(id=variation_id)
  
    if request.method == 'POST':
      form = VariationForm(request.POST ,instance=variations)
      if form.is_valid():
        form.save()
        return redirect('manage_variation')
    
    else:
      form = VariationForm(instance=variations)
    
    context = {
      'variations': variations,
      'form': form
    }
    return render(request, 'manager/update_variation.html', context)
  
  else:
    return redirect('home')



# My orders

@login_required(login_url='manager_login')
def admin_order(request):
  if request.user.is_admin:
    current_user = request.user
  
    if request.method == 'POST':
      keyword = request.POST['keyword']
      orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__icontains=keyword) | Q(user__email__icontains=keyword) | Q(firstname__icontains=keyword) | Q(lastname__icontains=keyword) | Q(phone_number__icontains=keyword)).order_by('-created_at')
      
    else:
      orders = Order.objects.filter(user=current_user, is_ordered=True).order_by('-created_at')
    
    paginator = Paginator(orders, 3)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
      'orders': paged_orders,
    }
    return render(request, 'manager/admin_orders.html', context)
  
  else:
    return redirect('home')




#ORDER Management
@never_cache
@login_required(login_url='manager_login')
def manage_order(request):
  if request.user.is_admin:
    if request.method == 'POST':
      keyword = request.POST['keyword']
      orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__icontains=keyword) | Q(user__email__icontains=keyword) | Q(firstname__icontains=keyword) | Q(lastname__icontains=keyword)).order_by('-order_number')
    
    else:
      orders = Order.objects.filter(is_ordered=True).order_by('-order_number')
      
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
      'orders': paged_orders
    }
    return render(request, 'manager/order_management.html', context)
  
  else:
    return redirect('home')


# Cancel Order
@never_cache
@login_required(login_url='manager_login')
def cancel_order(request, order_number):
  if request.user.is_admin:
    order = Order.objects.get(order_number=order_number)
    order.status = 'Order Cancelled'
    order.save()
    
    return redirect('manage_order')
  
  else:
    return redirect('home')



# Accept Order
@never_cache
@login_required(login_url='manager_login')
def accept_order(request, order_number):
  if request.user.is_admin:
    order = Order.objects.get(order_number=order_number)
    order.status = 'Order Accepted'
    order.save()
    
    return redirect('manage_order')
  
  else:
    return redirect('home')



# Complete Order
@never_cache
@login_required(login_url='manager_login')
def complete_order(request, order_number):
  if request.user.is_admin:
    order = Order.objects.get(order_number=order_number)
    order.status = 'Delivered Successfully'
    order.save()
    
    return redirect('manage_order')
  
  else:
    return redirect('home') 



#PRODUCT Management
@never_cache
@login_required(login_url='manager_login')
def manage_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword'] 
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(slug__icontains=keyword) | Q(category__category_name__icontains=keyword)).order_by('id')

        else:
            products = Product.objects.all().order_by('id')

        paginator = Paginator(products, 4)
        page      = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products' : paged_products 
        }

        return render(request, 'manager/product_management.html', context)

    else:
        return redirect('home')




# DELETE Product
@never_cache
@login_required(login_url='manager_login')
def delete_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('manage_product')

    else:
        return redirect('home')



#ADD Product
@never_cache
@login_required(login_url='manager_login')
def add_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save() 
                return redirect('manage_product')
        else:
            form = ProductForm()
            context = {
                'form' : form
            }
            return render(request, 'manager/add_product.html', context)

    else:
        return redirect('home')


# EDIT Product
@never_cache
@login_required(login_url='manager_login')
def edit_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)

        if request.method == 'POST':
            try:
                form =ProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()

                    return redirect('manage_product')

            except Exception as e:
                raise e

        context = {
            'product' : product,
            'form' : form
        }
        return render(request, 'manager/edit_product.html', context)

    else:
        return redirect('home')



#CATEGORY Management
@never_cache
@login_required(login_url='manager_login')
def manage_category(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword']
            categories = Category.objects.filter(Q(category_name__icontains=keyword) | Q(slug__icontains=keyword)).order_by('id') 
        
        else:
            categories = Category.objects.all().order_by('id')

        paginator = Paginator(categories, 3)
        page = request.GET.get('page')
        paged_categories = paginator.get_page(page)

        context = {
            'categories': paged_categories
        }

        return render(request, 'manager/category_management.html', context)

    else:
        return redirect('home')

#ADD Category
@never_cache
@login_required(login_url='manager_login')
def add_category(request):
  if request.user.is_admin:
    form = CategoryForm()
    if request.method == 'POST':
      try:
        form = CategoryForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
          form.save()
        return redirect('manage_category')
      
      except Exception as e:
        raise e
    
    return render(request, 'manager/category_add.html', {'form': form})
  
  else:
    return redirect('home')



#DELETE Category
@never_cache
@login_required(login_url='manager_login')
def delete_category(request, category_id):
    if request.user.is_admin:
        category = Category.objects.get(id=category_id)
        category.delete()

        return redirect('manage_category')

    else:
        return redirect('home')





# USER Management
@never_cache
@login_required(login_url='manager_login')
def manage_user(request):
  if request.user.is_admin:
    if request.method == 'POST':
      keyword = request.POST['keyword']
      users = Account.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(phone_number__icontains=keyword)).order_by('id')
    
    else:
        users = Account.objects.filter(is_admin=False).order_by('id')

    paginator   = Paginator(users, 3) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users' : paged_users,
    }
    return render(request, 'manager/user_management.html', context)

  else:
    return redirect('home') 

def redirect_to_login(request):
  return redirect('manager_login')

#BAN User
@never_cache
@login_required(login_url='manager_login')
def ban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = False
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')


#UnBAN User
@never_cache
@login_required(login_url='manager_login')
def unban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')


@never_cache
def manager_login(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('manager_dashboard') 
        else:
           return redirect('home')  
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_admin:
                    login(request, user)
                    return redirect('manager_dashboard')
                else:
                    messages.warning(request, 'You are logged in a non-staff account')

            else:
                messages.error(request, 'Email or Password is incorrect')
    return render(request, 'manager/manager_signin.html')




@never_cache
def manager_logout(request):
    logout(request)
    return redirect('manager_login')



@never_cache
@login_required(login_url='manager_login')
def admin_change_password(request):
  if request.user.is_admin:
    if request.method == 'POST':
      current_user = request.user
      current_password = request.POST['current_password']
      password = request.POST['password']
      confirm_password = request.POST['confirm_password']
      
      if password == confirm_password:
        if check_password(current_password, current_user.password):
          if check_password(password, current_user.password):
            messages.warning(request, 'Current password and new password is same')
          else:
            hashed_password = make_password(password)
            current_user.password = hashed_password
            current_user.save()
            messages.success(request, 'Password changed successfully')
        else:
          messages.error(request, 'Wrong password')
      else:
        messages.error(request, 'Passwords does not match')
    
    return render(request, 'manager/admin_change_password.html')
  
  else:
    return redirect('home')


# Review Management

def review_management(request):
    reviews = ReviewRating.objects.all()
    context = {
      'reviews': reviews
    }
    return render(request, 'manager/review_management.html', context)


def review_block(request, review_id):
    print("hai")
    review = ReviewRating.objects.get(id=review_id)
    review.status = False
    review.save()
    return redirect('review_management')

def review_unblock(request, review_id):
    review = ReviewRating.objects.get(id=review_id)
    review.status= True
    review.save()
    return redirect('review_management')


def review_delete(request, review_id):
    review = ReviewRating.objects.get(id=review_id)
    review.delete()
    return redirect('review_management')
