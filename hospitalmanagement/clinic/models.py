from django.db import models
from django.contrib import admin
from django.core.mail import send_mail

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Assuming a ForeignKey relation with the Department model
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    qualification = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')}"
    



class Appointment(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField(null=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    password=models.CharField(max_length=15,default='Password@123')

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time_slot}"





class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status']
    actions = ['approve_appointment', 'reject_appointment']

    def approve_appointment(self, request, queryset):
        queryset.update(status='approved')
        for appointment in queryset:
            self.send_approval_email(appointment)
    approve_appointment.short_description = 'Approve selected appointments'

    def reject_appointment(self, request, queryset):
        queryset.update(status='rejected')
        for appointment in queryset:
            self.send_rejection_email(appointment)
    reject_appointment.short_description = 'Reject selected appointments'

    def send_approval_email(self, appointment):
        if appointment.status == 'approved':
            subject = 'Appointment Approved'
            message = 'Your appointment has been approved. Thank you!'
            from_email = 'munapm1@gmail.com.com'  # Replace with your email address
            recipient_list = [appointment.email]
            send_mail(subject, message, from_email, recipient_list)

    def send_rejection_email(self, appointment):
        if appointment.status == 'rejected':
            subject = 'Appointment Rejected'
            message = 'Your appointment has been rejected. Please contact us for further information.'
            from_email = 'munapm1@gmail.com'  # Replace with your email address
            recipient_list = [appointment.email]
            send_mail(subject, message, from_email, recipient_list)




