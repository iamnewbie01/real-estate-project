# members/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,PropertyForm,PropertyImageFormSet , AgentSearchForm
from .models import Agent
from django.http import HttpResponseForbidden
from .models import Property,PropertyImage,Seller

from .filters import PropertyFilter
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user has an Agent profile
            if hasattr(user, 'agent'):
                return redirect('agent_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def property_list_view(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            if form.cleaned_data['signup_option'] == 'option2':
                agent = Agent(
                    user=user,
                    license_number=form.cleaned_data['license_number'],
                    phone=form.cleaned_data['phone'],
                    city=form.cleaned_data['city']
                )
                agent.save()
                messages.success(request, 'Agent account created successfully!')
                return redirect('agent_login')
            else:
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if Agent.objects.filter(user=request.user).exists():
        return render(request, 'dashboard_agent.html')
    return render(request, 'dashboard.html')

@login_required
def agent_dashboard_view(request):
    return render(request,'dashboard_agent.html')


# def agent_signup(request):
#     if request.method == 'POST':
#         form = AgentSignUpForm(request.POST)
#         if form.is_valid():
#             agent = form.save(commit=False)
#             agent.user = request.user
#             agent.save()
#             messages.success(request, 'Agent account created successfully!')
#             return redirect('agent-login')
#     else:
#         form = AgentSignUpForm()
#     return render(request, 'agent_signup.html', {'form': form})


def agent_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                agent = Agent.objects.get(user=user)
                login(request, user)
                return redirect('agent_dashboard')
            except Agent.DoesNotExist:
                messages.error(request, 'You do not have agent access.')
                return HttpResponseForbidden("You do not have agent access.")
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'agent_login.html')

@login_required
def buy_property_view(request):
    properties = Property.objects.all()
    property_filter = PropertyFilter(request.GET, queryset=properties)
    return render(request, 'buy_property.html', {'filter': property_filter})

@login_required
def sell_property_view(request):
    if not Agent.objects.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect('/find-agent')

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        formset = PropertyImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and formset.is_valid():
            property_instance = form.save(commit=False)

            if Property.objects.filter(property_id=property_instance.property_id).exists():
                form.add_error('property_id', "This Property ID already exists. Please enter a unique ID.")
            else:
                seller, created = Seller.objects.get_or_create(user=request.user)
                property_instance.seller = seller
                property_instance.save()

                for image_form in formset:
                    if image_form.cleaned_data.get('image'):
                        image_instance = image_form.save(commit=False)
                        image_instance.property = property_instance
                        image_instance.save()

                messages.success(request, 'Property and images have been uploaded successfully.')
                return redirect('property_detail', property_id=property_instance.property_id)  # Change this to property_instance.property_id

        else:
            print(form.errors)
            print(formset.errors)
            messages.error(request, 'There were errors in your submission.')
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'sell_property.html', {'form': form, 'formset': formset})


def property_detail_view(request, property_id):
    property_instance = get_object_or_404(Property, property_id=property_id)
    images = property_instance.images.all()

    if images.exists():
        image_url = images.first().image.url
    else:
        image_url = None

    return render(request, 'property_detail.html', {
        'property': property_instance,
        'images': images,
        'image_url': image_url
    })


@login_required
def find_agent_view(request):
    if Agent.objects.filter(user=request.user).exists():
        messages.error(request, "Only regular users can access this view.")
        return redirect('dashboard') 
    agents = None
    form = AgentSearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        selected_city = form.cleaned_data['city']
        agents = Agent.objects.filter(city=selected_city)

    return render(request, 'find_agent.html', {'form': form, 'agents': agents})

def property_brochure(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    context = {'property': property}
    
    # Render the HTML template
    html = render_to_string('property_brochure.html', context)
    
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{property.address}_brochure.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response