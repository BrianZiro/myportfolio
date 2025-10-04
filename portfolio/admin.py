from django.contrib import admin
from .models import Profile, Skill, Project, ContactMessage, Testimonial

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(ContactMessage)
admin.site.register(Testimonial)