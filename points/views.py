
from django.shortcuts import render
from .models import Kid
from .forms import KidForm

def kids_list(request):
    form = KidForm()
    if request.method == 'POST':
        form = KidForm(request.POST)
        if form.is_valid():
            form.save()
        form = KidForm()
    kids = Kid.objects.all()
    return render(request, 'points/kids_list.html', {'kids': kids, 'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a specific page based on user role.
            if user.is_staff:
                return redirect('admin_home')
            if user.is_superuser:  # Check if user is a superuser
                return redirect('add_points')

            else:
                return redirect('kids_points')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'points/home.html', {'error': 'Invalid login'})
    else:
        return render(request, 'points/home.html')



from django.shortcuts import render

# ... your other views ...

def admin_home(request):
    return render(request, 'points/admin_home.html')






from django.shortcuts import render, redirect
from .models import Kid
from .forms import AddPointsForm  # טופס שנוצר למטרה זו

def add_points(request):
    if request.method == 'POST':
        form = AddPointsForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            points_to_add = form.cleaned_data['points']
            try:
                kid = Kid.objects.get(barcode=barcode)
                kid.points += points_to_add
                kid.points_history += points_to_add  # עדכון שדה ה-points_history
                kid.save()
                return redirect('add_points')  # מניח שזה השם של הview שמציג את רשימת הילדים
            except Kid.DoesNotExist:
                form.add_error('barcode', 'Barcode not found')
    else:
        form = AddPointsForm()

    return render(request, 'points/add_points.html', {'form': form})




from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Kid
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = pd.read_excel(file, engine='openpyxl')
            for index, row in data.iterrows():
                try:
                    kid, created = Kid.objects.get_or_create(
                        name=row['name'], 
                        defaults={
                            'barcode':row['barcode'],
                            'group':row['group']  
                        }
                    )
                    if not created:
                        kid.barcode=row['barcode']
                        kid.group=row['group']  # הוספתי שדה 'group' כאן גם כן
                        kid.save()
                except IntegrityError:
                    return render(request, 'upload.html', {'form': form, 'error_message': 'Error: Duplicate barcode found.'})
            return redirect('kids_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})




def kids_list(request):
    form = KidForm()
    upload_form = UploadFileForm()  # Initial form
    if request.method == 'POST':
        form = KidForm(request.POST)
        if form.is_valid():
            form.save()
        form = KidForm()

        upload_form = UploadFileForm(request.POST, request.FILES)  # Update form with files
        if upload_form.is_valid():
            file = request.FILES['file']
            data = pd.read_excel(file, engine='openpyxl')
            for index, row in data.iterrows():
                try:
                    kid, created = Kid.objects.get_or_create(
                        name=row['name'], 
                        defaults={
                            'barcode':row['barcode'],
                            'group':row['group']  # הוספתי שדה 'group' לברירות המחדל
                        }
                    )
                    if not created:
                        kid.barcode=row['barcode']
                        kid.group=row['group']  # הוספתי שדה 'group' כאן גם כן
                        kid.save()
                except IntegrityError:
                    return render(request, 'points/kids_list.html', {'form': form, 'upload_form': upload_form, 'error_message': 'Error: Duplicate barcode found.'})
            return redirect('kids_list')
    else:
        form = KidForm()

    kids = Kid.objects.all()
    return render(request, 'points/kids_list.html', {'kids': kids, 'form': form, 'upload_form': upload_form})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Kid
from .forms import KidForm

def kid_edit(request, kid_id):
    kid = get_object_or_404(Kid, pk=kid_id)
    if request.method == "POST":
        form = KidForm(request.POST, instance=kid)
        if form.is_valid():
            form.save()
            return redirect('kids_list')
    else:
        form = KidForm(instance=kid)
    return render(request, 'points/kid_edit.html', {'form': form})

def kid_delete(request, kid_id):
    kid = get_object_or_404(Kid, pk=kid_id)
    if request.method == "POST":
        kid.delete()
        return redirect('kids_list')
    return render(request, 'points/kid_confirm_delete.html', {'kid': kid})

def kid_delete_multiple(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        Kid.objects.filter(id__in=ids).delete()
    return redirect('kids_list')


def kid_delete_multiple(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        kids = Kid.objects.filter(id__in=ids)
        if 'confirm' in request.POST:
            kids.delete()
            return redirect('kids_list')
        else:
            return render(request, 'points/kid_confirm_delete_multiple.html', {'kids': kids})
    else:
        return redirect('kids_list')





from django.db.models import Avg, Count

def kids_points_view(request):
    kids = Kid.objects.all()
    kids_points_history = []
    for kid in kids:
        kid_points = {
            'kid': kid,
            'points_history': kid.points_history,
            'total_points': kid.points
        }
        kids_points_history.append(kid_points)

    # Calculation of average points for each group
    group_points_avg = Kid.objects.values('group').annotate(average_points=Avg('points_history'))

    # Calculation of number of kids in each group
    group_counts = Kid.objects.values('group').annotate(count=Count('id'))

    # Add the count of kids to the average points dictionary
    for group in group_points_avg:
        for g in group_counts:
            if g['group'] == group['group']:
                group['count'] = g['count']

    # Sort the groups by average points
    sorted_groups = sorted(group_points_avg, key=lambda g: g['average_points'], reverse=True)

    # Add a rank to each group
    for i, group in enumerate(sorted_groups, 1):
        group['rank'] = i

    return render(request, 'points/kids_points.html', {'kids_points_history': kids_points_history, 'group_points': sorted_groups})



def deduct_points_view(request, kid_id, amount):
    kid = get_object_or_404(Kid, pk=kid_id)
    try:
        kid.deduct_points(amount)
        messages.success(request, f'{amount} points deducted from {kid.name}')
    except ValueError:
        messages.error(request, f'{kid.name} has insufficient points')
    return redirect('kids_list')

from .forms import NewUserForm
from django.contrib.auth import login



from django.contrib import messages

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("add_points")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="points/register.html", context={"register_form":form})




from django.shortcuts import render
from django.contrib.auth.models import User

def user_list(request):
    users = User.objects.all()
    return render(request, 'points/user_list.html', {'users': users})





from django.shortcuts import render

def index(request):
    return render(request, 'points/index.html')

from .models import Product, DollarToPoint
from django.views.generic.list import ListView
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'points/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()
        context['rate'] = DollarToPoint.objects.first().rate
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)








from django.views.generic.edit import CreateView, UpdateView
from .models import Product
from .forms import ProductForm

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'points/product_form.html'
    success_url = '/store/'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'points/product_edit.html'
    success_url = '/store/'



# views.py
from django.views.generic.edit import UpdateView
from .models import DollarToPoint

class RateUpdateView(UpdateView):
    model = DollarToPoint
    fields = ['rate']
    template_name = 'points/rate_edit.html'
    success_url = '/store/'
    
    def get_object(self):
        return DollarToPoint.objects.first()





from django.shortcuts import render, redirect
from .models import Kid
from .forms import CheckoutForm

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data.get('barcode')
            kid = Kid.objects.filter(barcode=barcode).first()
            if not kid:
                form.add_error('barcode', 'Kid not found.')
                return render(request, 'points/checkout.html', {'form': form})
            points_type = form.cleaned_data.get('points_type') 
            request.session['point_type'] = points_type
            return redirect('kid_account', kid_id=kid.id)
    else:
        form = CheckoutForm()
    return render(request, 'points/checkout.html', {'form': form})




from .forms import PurchaseForm ,AddCashForm
from .models import Kid, DollarToPoint, Product, Purchase 
from django.contrib import messages



def kid_account(request, kid_id):
    kid = get_object_or_404(Kid, pk=kid_id)
    points_type = request.session.get('point_type', 'points')  # default to regular points if not found in session
    purchases = Purchase.objects.filter(kid=kid).order_by('-date')  # get all purchases by the kid

    purchase_form = PurchaseForm(request.POST or None)
    add_cash_form = AddCashForm(request.POST or None)

    if 'submit-purchase' in request.POST and purchase_form.is_valid():
        barcode = purchase_form.cleaned_data.get('product_barcode')
        try:
            product = Product.objects.get(barcode=barcode)
            if points_type == 'points' and kid.points >= product.points_value:
                kid.points -= product.points_value
                Purchase.objects.create(kid=kid, product=product)  # create new Purchase
                kid.save()
                purchase_form = PurchaseForm()
            elif points_type == 'points_from_cash' and kid.points_from_cash >= product.points_value:
                kid.points_from_cash -= product.points_value
                Purchase.objects.create(kid=kid, product=product)  # create new Purchase
                kid.save()
                purchase_form = PurchaseForm()
            else:
                if points_type == 'points':
                    messages.error(request, 'Not enough points')
                    purchase_form = PurchaseForm()
                elif points_type == 'points_from_cash':
                    messages.error(request, 'Not enough points from cash')
                    purchase_form = PurchaseForm()
        except Product.DoesNotExist:
            messages.error(request, 'Product not found')
            purchase_form = PurchaseForm()
    elif 'submit-add-cash' in request.POST:
        if add_cash_form.is_valid():
            amount = add_cash_form.cleaned_data.get('amount')
            dollar_to_point = DollarToPoint.objects.latest('rate')  # get the latest conversion rate
            points = amount * dollar_to_point.rate  # convert the amount to points
            kid.points_from_cash += points
            kid.save()
            add_cash_form = AddCashForm()  # reset the form
        else:
            messages.error(request, 'No amount entered')


    return render(request, 'points/kid_account.html', {'kid': kid, 'purchase_form': purchase_form, 'add_cash_form': add_cash_form, 'points_type': points_type, 'purchases': purchases})




def add_to_cart(request, kid_id, product_id):
    kid = get_object_or_404(Kid, pk=kid_id)
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            Purchase.objects.create(kid=kid, product=product)
            # Here you can subtract the product points from kid's points
            # You will need to handle the case when the kid doesn't have enough points

            return redirect('kid_account', kid_id=kid.id)  

    else:
        form = PurchaseForm()

    return render(request, 'points/add_to_cart.html', {'form': form})






