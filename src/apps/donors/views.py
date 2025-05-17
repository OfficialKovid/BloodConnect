from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BloodRequest
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from .utils import get_all_states, get_cities_for_state, STATES_CITIES

def donor_register(request):
    if request.method == 'POST':
        # Handle form submission later
        pass
    return render(request, 'donors/donor.html')

def receiver_request(request):
    if request.method == 'POST':
        try:
            blood_request = BloodRequest(
                patient_name=request.POST['patient_name'],
                hospital_name=request.POST['hospital_name'],
                contact_number=request.POST['contact_number'],
                blood_group=request.POST['blood_group'],
                state=request.POST['state'],
                city=request.POST['city'],
                required_date=request.POST['required_date'],
                additional_notes=request.POST.get('additional_notes', '')
            )
            blood_request.save()
            
            return render(request, 'donors/request_success.html', {
                'reference_number': blood_request.reference_number,
                'patient_name': blood_request.patient_name,
                'blood_group': blood_request.blood_group,
                'required_date': blood_request.required_date
            })
        except Exception as e:
            messages.error(request, "An error occurred while processing your request. Please try again.")
            return redirect('donors:receiver')

    context = {
        'states': get_all_states(),
        'states_cities_json': STATES_CITIES
    }
    return render(request, 'donors/receiver.html', context)

def list_donors(request):
    donors = User.objects.filter(is_active=True)
    
    blood_group = request.GET.get('blood_group')
    state = request.GET.get('state')
    city = request.GET.get('city')
    
    if blood_group:
        donors = donors.filter(blood_type=blood_group)
    if state:
        donors = donors.filter(state=state)
    if city:
        donors = donors.filter(city=city)
    
    context = {
        'donors': donors,
        'states': get_all_states(),
        'cities': get_cities_for_state(state) if state else [],
        'selected_state': state,
        'selected_city': city,
        'selected_blood_group': blood_group,
        'states_cities_json': STATES_CITIES  # For JavaScript use
    }
    
    return render(request, 'donors/List_donor.html', context)

def list_blood_requests(request):
    today = timezone.now().date()
    
    # Get ALL pending requests first without any date filtering
    requests = BloodRequest.objects.filter(status='PENDING')
    
    # Get filter parameters
    blood_group = request.GET.get('blood_group')
    state = request.GET.get('state')
    city = request.GET.get('city')
    
    # Apply filters
    if blood_group:
        requests = requests.filter(blood_group=blood_group)
    if state:
        requests = requests.filter(state=state)
    if city:
        requests = requests.filter(city=city)

    # Now split into urgent and regular after filtering
    urgent_requests = requests.filter(
        required_date__gte=today,
        required_date__lte=today + timedelta(days=3)
    )
    
    # Get regular requests (all requests that are not urgent)
    regular_requests = requests.filter(required_date__gt=today + timedelta(days=3))
    
    # Add debug messages
    print(f"Debug - Total Pending: {requests.count()}")
    print(f"Debug - Regular: {regular_requests.count()}")
    print(f"Debug - Urgent: {urgent_requests.count()}")
    
    context = {
        'requests': requests.order_by('-created_at'),  # Show all requests for now
        'states': get_all_states(),
        'cities': get_cities_for_state(state) if state else [],
        'selected_blood_group': blood_group,
        'selected_state': state,
        'selected_city': city,
        'states_cities_json': STATES_CITIES
    }
    
    return render(request, 'donors/list_blood_request.html', context)

def urgent_requests(request):
    today = timezone.now().date()
    
    # Get urgent requests (requests for today and next 3 days)
    urgent_requests = BloodRequest.objects.filter(
        status='PENDING',
        required_date__gte=today,
        required_date__lte=today + timedelta(days=3)
    ).order_by('required_date')

    # Add days_until property to each request - using blood_req instead of request as variable name
    for blood_req in urgent_requests:
        blood_req.days_until = (blood_req.required_date - today).days

    # Get filter parameters from GET request
    blood_group = request.GET.get('blood_group')
    state = request.GET.get('state')
    city = request.GET.get('city')

    # Apply filters if provided
    if blood_group:
        urgent_requests = urgent_requests.filter(blood_group=blood_group)
    if state:
        urgent_requests = urgent_requests.filter(state=state)
    if city:
        urgent_requests = urgent_requests.filter(city=city)

    context = {
        'urgent_requests': urgent_requests,
        'states': get_all_states(),
        'cities': get_cities_for_state(state) if state else [],
        'selected_blood_group': blood_group,
        'selected_state': state,
        'selected_city': city,
        'states_cities_json': STATES_CITIES
    }
    
    return render(request, 'donors/urgent_req_list.html', context)
