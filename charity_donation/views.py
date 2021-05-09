from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from charity_donation.models import Donation, Institution, Category
from charity_donation.forms import SignUpForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class LandingPage(View):
    def get(self, request):
        bag_number = Donation.objects.all().count()
        institution_number = Donation.objects.values('institution__name').distinct().count()
        institution_foundation = Institution.objects.filter(type='f').order_by('name')
        institution_organization = Institution.objects.filter(type='o').order_by('name')
        institution_local = Institution.objects.filter(type='z').order_by('name')
        print(institution_foundation)
        paginator_foundation = Paginator(institution_foundation, 5)
        print(paginator_foundation)
        print(paginator_foundation.num_pages)
        print(paginator_foundation.page_range)
        page_f = request.GET.get('page')
        print(page_f)
        foundations = paginator_foundation.get_page(page_f)
        paginator_organization = Paginator(institution_organization, 5)
        page_o = request.GET.get('page')
        organizations = paginator_organization.get_page(page_o)
        paginator_local = Paginator(institution_local, 5)
        page_l = request.GET.get('page')
        local = paginator_local.get_page(page_l)
        ctx = {
            "bag_number": bag_number,
            "institution_number": institution_number,
            "institution_foundation": institution_foundation,
            "institution_organization": institution_organization,
            "institution_local": institution_local,
            "foundations": foundations,
            "organizations": organizations,
            "local": local,
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

    def post(self, request):
        quantity = request.POST["bags"]
        institution = Institution.objects.get(pk=request.POST["organization"])
        categories = request.POST.getlist("categories")
        address = request.POST["address"]
        city = request.POST["city"]
        postcode = request.POST["postcode"]
        phone = request.POST["phone"]
        data = request.POST["data"]
        time = request.POST["time"]
        more_info = request.POST["more_info"]
        user = request.user

        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone,
            city=city,
            zip_code=postcode,
            pick_up_date=data,
            pick_up_time=time,
            pick_up_comment=more_info,
            user=user,
        )
        for category in categories:
            c = Category.objects.get(pk=category)
            donation.categories.add(c)
        donation.save()
        return render(request, "charity_donation/form-confirmation.html")


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


class UserView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by("is_taken") \
            .order_by("-pick_up_date").order_by("-pick_up_time")
        ctx = {
            "donations": donations,
        }
        return render(request, 'charity_donation/user.html', ctx)

    def post(self, request):
        donation = Donation.objects.get(id=request.POST["donation_id"])
        if "donation_not_taken" in request.POST:
            donation.is_taken = False
        elif "donation_taken" in request.POST:
            donation.is_taken = True
        donation.save()
        return redirect("user")


class UserSettings(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, 'charity_donation/user-settings.html')

    def post(self, request):
        password = request.POST["password"]
        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            if "settings_save" in request.POST:
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                username = request.POST["username"]

                if request.user.username == username:
                    user = User.objects.get(username=username)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.save()
                    return redirect("user")

                else:
                    try:
                        User.objects.get(username=username)
                    except ObjectDoesNotExist:
                        user = User.objects.get(username=request.user.username)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.username = username
                        user.save()
                        return redirect("user")
                    return redirect("user_settings")

            elif "password_save" in request.POST:
                new_password1 = request.POST["new_password1"]
                new_password2 = request.POST["new_password2"]
                if new_password1 == new_password2:
                    user.set_password(new_password2)
                    user.save()
                    login(request, user=user)
                    return redirect("user")

        else:
            return redirect("user_settings")
