from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(req):
    form = UserRegisterForm(req.POST or None)
    if req.method == "POST" and form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(req, f"Account has been created! You can now login")
        return redirect('login')

    return render(req, 'users/register.html', {'form': form})

@login_required
def profile(req):
    if req.method == "POST":
        u_form = UserUpdateForm(req.POST, instance=req.user)
        p_form = ProfileUpdateForm(req.POST, req.FILES, instance=req.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(req, f"Account has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=req.user)
        p_form = ProfileUpdateForm(instance=req.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(req, 'users/profile.html', context)
