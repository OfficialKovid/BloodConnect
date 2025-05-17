from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return render(request, 'accounts/signup.html')
                
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone_primary=request.POST.get('phone_primary'),
                phone_secondary=request.POST.get('phone_secondary'),
                blood_type=request.POST.get('blood_type'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country='India'
            )
            login(request, user)
            return redirect('home:home')
            
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'accounts/signup.html')

@login_required
def profile_view(request):
    # Get any donation history if you have a Donation model
    donations = []  # Replace with actual donation query if you have one
    context = {
        'user': request.user,
        'donations': donations
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # Handle profile update logic
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_primary = request.POST.get('phone_primary')
        phone_secondary = request.POST.get('phone_secondary')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone_primary = phone_primary
        user.phone_secondary = phone_secondary
        user.address = address
        user.city = city
        user.state = state
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')

    return render(request, 'accounts/edit_profile.html', {'user': request.user})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        # Handle password change logic
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('accounts:change_password')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('accounts:change_password')

        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('accounts:profile')

    return render(request, 'accounts/change_password.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home:home')
