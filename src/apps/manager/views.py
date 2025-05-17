from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from apps.accounts.models import User
from apps.donors.models import BloodRequest

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin, login_url='accounts:login')
def dashboard(request):
    # Get basic stats
    total_donors = User.objects.count()
    total_requests = BloodRequest.objects.count()
    
    # Since is_fulfilled might not exist yet
    try:
        pending_requests = BloodRequest.objects.filter(is_fulfilled=False).count()
    except:
        pending_requests = total_requests  # Assume all are pending if field doesn't exist
    
    total_cities = User.objects.values('city').distinct().count()

    # Get blood type distribution
    blood_distribution = User.objects.values('blood_type').annotate(
        count=Count('id')
    ).order_by('blood_type')
    blood_distribution = {item['blood_type']: item['count'] for item in blood_distribution}

    # Get recent blood requests
    recent_requests = BloodRequest.objects.all().order_by('-created_at')[:10]

    context = {
        'total_donors': total_donors,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'total_cities': total_cities,
        'blood_distribution': blood_distribution,
        'recent_requests': recent_requests,
    }

    return render(request, 'manager/Dashboard.html', context)
