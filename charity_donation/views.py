from django.views import View
from django.shortcuts import render
from charity_donation.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request):
        bag_number = Donation.objects.all().count()
        institution_number = Institution.objects.all().count()
        ctx = {
            "bag_number": bag_number,
            "institution_number": institution_number
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
