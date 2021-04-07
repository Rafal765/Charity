from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from charity_donation.models import Donation, Institution, Category
from charity_donation.forms import SignUpForm, LoginForm


class LandingPage(View):
    def get(self, request):
        bag_number = Donation.objects.all().count()
        institution_number = Donation.objects.values('institution__name').distinct().count()
        institution_foundation = Institution.objects.filter(type='f').order_by('name')
        institution_organization = Institution.objects.filter(type='o').order_by('name')
        institution_local = Institution.objects.filter(type='z').order_by('name')
        ctx = {
            "bag_number": bag_number,
            "institution_number": institution_number,
            "institution_foundation": institution_foundation,
            "institution_organization": institution_organization,
            "institution_local": institution_local,
        }
        return render(request, 'charity_donation/index.html', ctx)


class AddDonation(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            "categories": categories,
            "institutions": institutions,
        }
        return render(request, 'charity_donation/form.html', ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'charity_donation/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("landing_page")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("landing_page")


class Register(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'charity_donation/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../login#login')
        return render(request, 'charity_donation/register.html', {'form': form})


class UserView(View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        ctx = {
            "donations": donations,
        }
        return render(request, 'charity_donation/user.html', ctx)


#class DonationFormView(View):
#    def get(self, request):
#        form = SignUpForm()
#        return render(request, 'charity_donation/register.html', {'form': form})
#
#    def post(self, request):
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('../login#login')
#        return render(request, 'charity_donation/register.html', {'form': form})