from django.contrib import admin


# Register your models here.

from .models import Department
from .models import Doctor
from .models import TimeSlot,Appointment,AppointmentAdmin



admin.site.register(Department)


admin.site.register(Doctor)



admin.site.register(TimeSlot)
admin.site.register(Appointment,AppointmentAdmin)







