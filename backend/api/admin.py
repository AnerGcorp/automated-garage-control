from django.forms import TextInput, Textarea
from django.db import models
from django.contrib import admin
from .models import Soldier, BeenMilitaryBase, CloseRelative, Officer, \
    CarModel, Duty, CarMovement

# Register your models here.
class MilitaryBaseAdminInline(admin.TabularInline):
    model = BeenMilitaryBase
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'30'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

class CloseRelativeAdminInline(admin.TabularInline):
    model = CloseRelative
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'30'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):
    inlines = (MilitaryBaseAdminInline, CloseRelativeAdminInline)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

class OfficerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

class CarModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

class DutyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

class CarMovementAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

# admin.site.register(Soldier, SoldierAdmin)
admin.site.register(Officer, OfficerAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Duty, DutyAdmin)
admin.site.register(CarMovement, CarMovementAdmin)