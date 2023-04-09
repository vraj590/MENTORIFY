# Import necessary modules
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobListing, MentorshipProgram, SkillAssessment, Blog, UserSkill
from .forms import SkillAssessmentForm
from .recommendation_system import get_recommendations

# View function for homepage
def home(request):
    return render(request, 'home.html')

# View function for explore page
@login_required
def explore(request):
    job_listings = JobListing.objects.all()
    mentorship_programs = MentorshipProgram.objects.all()
    skill_assessments = SkillAssessment.objects.filter(user=request.user)
    recommendations = get_recommendations(request.user)
    return render(request, 'explore.html', {'job_listings': job_listings, 'mentorship_programs': mentorship_programs,
                                            'skill_assessments': skill_assessments, 'recommendations': recommendations})

# View function for job listing page
@login_required
def job_listing(request):
    job_listings = JobListing.objects.all()
    return render(request, 'job_listing.html', {'job_listings': job_listings})

# View function for mentorship program page
@login_required
def mentorship_program(request):
    mentorship_programs = MentorshipProgram.objects.all()
    return render(request, 'mentorship_program.html', {'mentorship_programs': mentorship_programs})

# View function for blog page
def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})

# View function for taking a skill assessment
@login_required
def take_skill_assessment(request):
    if request.method == 'POST':
        form = SkillAssessmentForm(request.POST)
        if form.is_valid():
            skill_assessment = form.save(commit=False)
            skill_assessment.user = request.user
            skill_assessment.save()
            return redirect('explore')
    else:
        form = SkillAssessmentForm()
    return render(request, 'take_skill_assessment.html', {'form': form})

# View function for saving user's skills
@login_required
def save_user_skill(request):
    if request.method == 'POST':
        user_skill = UserSkill(user=request.user)
        user_skill.skill_name = request.POST.get('skill_name')
        user_skill.skill_level = request.POST.get('skill_level')
        user_skill.save()
        return redirect('profile')
    else:
        return render(request, 'save_user_skill.html')

# View function for user profile
@login_required
def profile(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    skill_assessments = SkillAssessment.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_skills': user_skills, 'skill_assessments': skill_assessments})
