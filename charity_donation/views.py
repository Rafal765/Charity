from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from charity_donation.models import Donation, Institution, Category
from charity_donation.forms import SignUpForm


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


class AddDonation(View):
    def get(self, request):
        return render(request, 'charity_donation/form.html')


class Login(View):
    def get(self, request):
        return render(request, 'charity_donation/login.html')


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

