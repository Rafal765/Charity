from django.views import View
from django.shortcuts import render
from charity_donation.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        bag_number = Donation.objects.all().count()
        institution_number = Institution.objects.all().count()
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
        return render(request, 'charity_donation/register.html')
