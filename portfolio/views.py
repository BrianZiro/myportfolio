from django.shortcuts import render, redirect
from .models import Profile, Skill, Project, ContactMessage, Testimonial
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
import google.generativeai as genai
import json,os

# Create your views here.
# Home / Landing Page
def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    return render(request, 'portfolio/home.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects
    })

# Contact form
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        return redirect('contact')
    return render(request, 'portfolio/contact.html')

def about(request):
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, 'portfolio/aboutme.html', context)

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'portfolio/projects.html', context)

def skills(request):
    skills = Skill.objects.all()
    context = {
        'skills': skills,
    }
    return render(request, 'portfolio/skills.html', context)

def testimonials(request):
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/testimonials.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification (optional)
        try:
            send_mail(
                f'Portfolio Contact: {subject}',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except:
            pass
        
        return JsonResponse({'success': True})
    
    return render(request, 'portfolio/contact.html')


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Load the knowledge base once
KNOWLEDGE_FILE = os.path.join(settings.BASE_DIR, "portfolio", "knowledge.json")
with open(KNOWLEDGE_FILE, "r") as f:
    KNOWLEDGE = json.load(f)

def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"reply": "⚠️ Only POST requests allowed"})

    try:
        data = json.loads(request.body)
        user_msg = data.get("message", "").strip().lower()
    except:
        return JsonResponse({"reply": "⚠️ Invalid request"})

    # Check knowledge base
    reply = None

    # Mapping keywords to fields
    if any(keyword in user_msg for keyword in ["who", "brian", "bio", "about"]):
        reply = KNOWLEDGE.get("bio")
    elif "skill" in user_msg:
        skills = KNOWLEDGE.get("skills", {})
        tech_skills = ", ".join(skills.get("technical", []))
        soft_skills = ", ".join(skills.get("soft_skills", []))
        reply = f"Technical skills: {tech_skills}\nSoft skills: {soft_skills}"
    elif "project" in user_msg or "work" in user_msg:
        projects = KNOWLEDGE.get("projects", [])
        reply = "Here are some projects:\n" + "\n".join([f"- {p['name']}: {p['description']}" for p in projects])
    elif "achievement" in user_msg or "award" in user_msg or "success" in user_msg:
        achievements = KNOWLEDGE.get("achievements", [])
        reply = "Achievements:\n" + "\n".join([f"- {a}" for a in achievements])
    elif "goal" in user_msg or "aspiration" in user_msg:
        goals = KNOWLEDGE.get("goals", [])
        reply = "Goals:\n" + "\n".join([f"- {g}" for g in goals])
    elif "community" in user_msg or "project" in user_msg:
        community = KNOWLEDGE.get("community_projects", [])
        if community:
            reply = "Community Projects:\n" + "\n".join([f"- {c['name']}: {c['description']}" for c in community])
        else:
            reply = "No community projects found."
    elif "personality" in user_msg or "trait" in user_msg:
        traits = KNOWLEDGE.get("personality_traits", [])
        reply = "Personality Traits:\n" + "\n".join([f"- {t}" for t in traits])
    elif "fun fact" in user_msg or "fun" in user_msg:
        fun = KNOWLEDGE.get("fun_facts", [])
        reply = "Fun Facts:\n" + "\n".join([f"- {f}" for f in fun])
    else:
        reply = None  # Not found in knowledge base

    # If not found, fallback to Gemini
    if not reply:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                content={
                    "parts": [
                        {"text": user_msg}
                    ]
                }
            )
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error generating response: {str(e)}"

    return JsonResponse({"reply": reply})