import random
from django.db.models import Q

# Import portfolio models
from portfolio.models import Profile, Project, Skill, Education, Experience, ContactInfo


def get_answer(message: str) -> str:
    """Simple rule‑based answer generator.
    Uses the real model fields defined in the project.
    """
    message = message.lower()
    # Retrieve the singleton profile (there should be only one)
    profile = Profile.objects.first()
    if not profile:
        return "Profile information is not available."

    # Name / about
    if any(keyword in message for keyword in ["name", "who are you", "about"]):
        return f"I am {profile.name}, a {profile.title}."

    # Email / contact
    if "email" in message or "contact" in message:
        contact = ContactInfo.objects.filter(profile=profile).first()
        if contact and contact.email:
            return f"You can reach me at {contact.email}."
        return "Contact email not found."

    # Education
    if "education" in message:
        educations = Education.objects.all().order_by("-start_date")
        if not educations:
            return "No education records found."
        latest = educations.first()
        end_year = latest.end_date.year if latest.end_date else "present"
        return f"I studied {latest.degree} at {latest.institution} ({latest.start_date.year}–{end_year})."

    # Experience
    if "experience" in message or "job" in message:
        experiences = Experience.objects.all().order_by("-start_date")
        if not experiences:
            return "No experience records found."
        latest = experiences.first()
        end_year = latest.end_date.year if latest.end_date else "present"
        return f"My latest role was {latest.role} at {latest.company} ({latest.start_date.year}–{end_year})."

    # Skills
    if "skill" in message:
        skills = Skill.objects.all()
        if not skills:
            return "No skills listed."
        skill_names = ", ".join([s.name for s in skills[:5]])
        return f"Some of my skills include: {skill_names}."

    # Projects
    if "project" in message:
        projects = Project.objects.all()
        if not projects:
            return "No projects found."
        proj = random.choice(list(projects))
        # Use title and description (short description)
        desc = proj.description[:120] + ("..." if len(proj.description) > 120 else "")
        return f"One of my projects is {proj.title}: {desc}"

    # Fallback
    return "I’m happy to help! Ask me about my background, skills, education, experience, or projects."
