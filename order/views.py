from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import form_szkolenie_wstepne, RegisterForm1, form_szkolenia_okresowe, form_szkolenie_pp, form_szkolenie_opp, \
    form_szkolenie_inst_opp, form_audyt, form_ocena_ryzyka
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, FormView
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import szkolenie_wstepne, szkolenie_okresowe, szkolenie_pp, szkolenie_opp, szkolenie_inst_opp, audyt, \
    ocena_ryzyka


def index(request):
    return render(request, "base.html")


def kontakt(request):
    return render(request, "kontakt.html")


def szkolenia(request):
    return render(request, "szkolenia.html")


def ocena(request):
    return render(request, "ocena.html")


def pomoc(request):
    return render(request, "pomoc.html")


def wypadek(request):
    return render(request, "wypadek.html")


def doradztwo(request):
    return render(request, "doradztwo.html")


# def orderservice(request):
#     if request.method == "POST":
#         form = ExampleForm(request.POST, initial={'creator': request.user})
#         if form.is_valid():
#             form.save()
#             return redirect("/kontakt/")
#         else:
#             return redirect("/ocena/")
#     else:
#         form = ExampleForm(initial={'creator': request.user})
#     return render(request, "szkolenie_wstepne.html", {"method": request.method, "form": form})

class szkolenie_wstepne_view(LoginRequiredMixin, FormView):
    form_class = form_szkolenie_wstepne
    template_name = "szkolenie_wstepne.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = szkolenie_wstepne.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie szkolenia wst??pnego w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie szkolenia wst??pnego'
        msg_for_admin = '''
        
                <h3>Z??o??enie zam??wienia na szkolenie wst??pne<h3>
                
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk niebezpiecznych: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk kierowniczych: %s
                
                ''' % (self.request.POST["imie"], self.request.POST["nazwisko"], self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"],
                       self.request.POST["liczba_osob"],
                       self.request.POST["niebezpiecznie_czy_nie"], self.request.POST["kierownicze_czy_nie"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                
                %s dzi??kujemy za z??o??enie zam??wienia na szkolenie wst??pne w firmie ALT-BHP.
                
                Szczeg????y Twojego zam??wienia:

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk niebezpiecznych: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk kierowniczych: %s
                
                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"], self.request.POST["liczba_osob"],
                       self.request.POST["niebezpiecznie_czy_nie"], self.request.POST["kierownicze_czy_nie"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class szkolenie_okresowe_view(LoginRequiredMixin, FormView):
    form_class = form_szkolenia_okresowe
    template_name = "szkolenie_okresowe.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = szkolenie_okresowe.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie szkolenia okresowego w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie szkolenia okresowego'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na szkolenie okresowe<h3>
                
                Rodzaj szkolenia: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk niebezpiecznych: %s

                ''' % (self.request.POST["rodzaj_szkolenia"], self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"],
                       self.request.POST["liczba_osob"],
                       self.request.POST["niebezpiecznie_czy_nie"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na szkolenie okresowe w firmie ALT-BHP.

                Szczeg????y Twojego zam??wienia:

                Rodzaj szkolenia: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s
                Czy szkolenie b??dzie przeprowadzane dla stanowisk niebezpiecznych: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["rodzaj_szkolenia"], self.request.POST["imie"],
                       self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"], self.request.POST["liczba_osob"],
                       self.request.POST["niebezpiecznie_czy_nie"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class szkolenie_pp_view(LoginRequiredMixin, FormView):
    form_class = form_szkolenie_pp
    template_name = "szkolenie_pp.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = szkolenie_pp.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie szkolenia z pierwszej pomocy w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie szkolenia z pierwszej pomocy'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na szkolenie z pierwszej pomocy<h3>

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s

                ''' % (self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"],
                       self.request.POST["liczba_osob"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na szkolenie z pierwszej pomocy przedmedycznej w firmie ALT-BHP.

                Szczeg????y Twojego zam??wienia:

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["imie"],
                       self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"], self.request.POST["liczba_osob"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class szkolenie_opp_view(LoginRequiredMixin, FormView):
    form_class = form_szkolenie_opp
    template_name = "szkolenie_opp.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = szkolenie_opp.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie szkolenia z ochrony przeciwpo??arowej w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie szkolenia z ochrony przeciwpo??arowej'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na szkolenie z ochrony przeciwpo??arowej<h3>

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s

                ''' % (self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"],
                       self.request.POST["liczba_osob"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na szkolenie z ochrony przeciwpo??arowej w firmie ALT-BHP.

                Szczeg????y Twojego zam??wienia:

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s
                Ilo???? os??b: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["imie"],
                       self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"], self.request.POST["liczba_osob"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class szkolenie_inst_opp_view(LoginRequiredMixin, FormView):
    form_class = form_szkolenie_inst_opp
    template_name = "szkolenie_inst_opp.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = szkolenie_inst_opp.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie instrukcji przeciwpo??arowej w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie instrukcji przeciwpo??arowej'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na instrukcje przeciwpo??arow??<h3>

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                ''' % (self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na instrukcje przeciwpo??arow?? w firmie ALT-BHP.

                Szczeg????y Twojego zam??wienia:

                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["imie"],
                       self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class audyt_view(LoginRequiredMixin, FormView):
    form_class = form_audyt
    template_name = "audyt.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = audyt.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie na przeprowadzenie audyt??w w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie na przeprowadzenie audyt??w'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na przeprowadzenie audyt??w<h3>

                Rodzaj audytu: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                ''' % (self.request.POST["rodzaj_audytu"], self.request.POST["imie"], self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"],
                       self.request.POST["numer_nip"], self.request.POST["numer_telefonu"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na przeprowadzenie audyt??w w serwisie ALT-BHP.

                Szczeg????y Twojego zam??wienia:
                
                Rodzaj audytu: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (self.request.POST["imie"], self.request.POST["rodzaj_audytu"], self.request.POST["imie"],
                       self.request.POST["nazwisko"],
                       self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
                       self.request.POST["numer_telefonu"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


class ocena_ryzyka_view(LoginRequiredMixin, FormView):
    form_class = form_ocena_ryzyka
    template_name = "order_ocena_ryzyka.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['creator'] = ocena_ryzyka.objects.filter(creator=request.user)
        return self.render_to_response(context)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = self.request.user
        form.data = datetime.now().date()
        form.save()
        client_address = self.request.POST["email"]
        admin_address = 'djangowebproject@gmail.com'
        subject_for_client = 'Pomy??lnie z??o??one zam??wienie na sporz??dzenie oceny ryzyka zawodowego na dane stanowisko w serwisie ALT-BHP'
        subject_for_admin = 'Nowe zam??wienie na sporz??dzenie oceny ryzyka zawodowego'
        msg_for_admin = '''

                <h3>Z??o??enie zam??wienia na sporz??dzenie oceny ryzyka zawodowego<h3>

                Stanowisko: %s
                Kod zawodu: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                ''' % (
            self.request.POST["wybor_stanowiska"], self.request.POST["kod_zawodu"], self.request.POST["imie"],
            self.request.POST["nazwisko"],
            self.request.POST["nazwa_firmy"],
            self.request.POST["numer_nip"], self.request.POST["numer_telefonu"])
        msg_for_client = '''

                <h3>Witamy!<h3>
                %s dzi??kujemy za z??o??enie zam??wienia na sporz??dzenie oceny ryzyka zawodowego na dane stanowisko w serwisie ALT-BHP.

                Szczeg????y Twojego zam??wienia:

                Stanowisko: %s
                Kod zawodu: %s
                Imi??: %s
                Nazwisko: %s
                Nazwa firmy: %s
                NIP: %s
                Numer telefonu: %s

                Wkr??tce nasz pracownik skontaktuje si?? w celu ustalenia terminu.

                ''' % (
            self.request.POST["imie"], self.request.POST["wybor_stanowiska"], self.request.POST["kod_zawodu"],
            self.request.POST["imie"],
            self.request.POST["nazwisko"],
            self.request.POST["nazwa_firmy"], self.request.POST["numer_nip"],
            self.request.POST["numer_telefonu"])
        from_email = 'ALT-BHP@elk.pl'
        send_mail(subject_for_client, msg_for_client, from_email, [client_address])
        send_mail(subject_for_admin, msg_for_admin, from_email, [admin_address])
        return redirect("/zamowienie/koniec")


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def profile_wstepne(request):
    orders = szkolenie_wstepne.objects.filter(creator=request.user)
    return render(request, 'profile_wstepne.html', {'orders': orders})


@login_required
def profile_okresowe(request):
    orders_okresowe = szkolenie_okresowe.objects.filter(creator=request.user)
    return render(request, 'profile_okresowe.html', {'orders_okresowe': orders_okresowe})


@login_required
def profile_pp(request):
    orders_pp = szkolenie_pp.objects.filter(creator=request.user)
    return render(request, 'profile_pp.html', {'orders_pp': orders_pp})


@login_required
def profile_opp(request):
    orders_opp = szkolenie_opp.objects.filter(creator=request.user)
    return render(request, 'profile_opp.html', {'orders_opp': orders_opp})


@login_required
def profile_inst_opp(request):
    orders_inst_opp = szkolenie_inst_opp.objects.filter(creator=request.user)
    return render(request, 'profile_inst_opp.html', {'orders_inst_opp': orders_inst_opp})


@login_required
def profile_audyt(request):
    orders_audyt = audyt.objects.filter(creator=request.user)
    return render(request, 'profile_audyt.html', {'orders_audyt': orders_audyt})


@login_required
def profile_ocena_ryzyka(request):
    orders_ocena_ryzyka = ocena_ryzyka.objects.filter(creator=request.user)
    return render(request, 'profile_ocena_ryzyka.html', {'orders_ocena_ryzyka': orders_ocena_ryzyka})


@login_required
def success_order(request):
    return render(request, "success_order.html")


def orderserv(request):
    return render(request, "orderserv.html")


def success_reg(request):
    return render(request, "success_reg.html")


class Register(CreateView):
    form_class = RegisterForm1
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data.get("username"),
                            password=form.cleaned_data.get("password1"))
        login(self.request, user)

        client_address = form.cleaned_data.get("email")
        subject = 'Pomy??lna rejestracja w serwisie ALT-BHP'
        from_email = 'ALT-BHP@elk.pl'
        html_msg = render_to_string('email_temp.html', {'context': 'values'})
        plain_message = strip_tags(html_msg)
        send_mail(subject, plain_message, from_email, [client_address], html_message=html_msg)

        return redirect("/register/success/")
