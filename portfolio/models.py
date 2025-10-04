# main/models.py
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    name = models.CharField(max_length=100, default="Your Name")
    tagline = models.CharField(max_length=2000, default="Your Tagline")
    bio = models.TextField(default="Your bio goes here...")
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(default="your@email.com")
    phone = models.CharField(max_length=20, blank=True, default="")
    location = models.CharField(max_length=100, blank=True, default="")
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, default="Skill Name")
    percentage = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200, default="Project Title")
    description = models.TextField(default="Project description...")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField(blank=True, default="")
    github_link = models.URLField(blank=True, default="")
    technologies = models.CharField(max_length=200, blank=True, default="")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100, default="Client Name")
    position = models.CharField(max_length=100, blank=True, default="")
    company = models.CharField(max_length=100, blank=True, default="")
    content = models.TextField(default="Testimonial content...")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Testimonial from {self.name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="")
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name}"