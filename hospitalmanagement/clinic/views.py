from django.shortcuts import render
from .models import Appointment
from django.views.generic import View,CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



# Create your views here.
from django.shortcuts import render, redirect
from .forms import AppointmentForm,RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User






class SignupView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account created")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)

class SigninView(View):
    model=User
    template_name="login.html"
    form_class=LoginForm

    def get(self,request,*args,**kargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            usname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=usname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("signin")
            messages.error(request,"invalid credential")
            return render(request,self.template_name,{"form":form})

def signin_required(fn):
    def wrapper(request,*args,**kargs):
        if not request.user.is_authenticated:
            messages.error(request,"you must login to perform this action")
            return redirect("signin")
        return fn(request,*args,**kargs)
    return wrapper


@login_required(login_url='signin')
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_appointment')  # Replace 'success' with the URL name for the success page
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})