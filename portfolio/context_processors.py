from .models import Profile, Education, Experience


def portfolio_globals(request):
    profile = Profile.objects.first()
    return {
        "profile": profile,
        "education_list": Education.objects.all(),
        "experience_list": Experience.objects.all(),
    }
