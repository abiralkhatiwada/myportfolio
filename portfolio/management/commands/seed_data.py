from django.core.management.base import BaseCommand
from portfolio.models import Profile, Skill, Project, BlogPost


class Command(BaseCommand):
    help = "Seed the database with initial portfolio data"

    def handle(self, *args, **options):
        # Create Profile
        if not Profile.objects.exists():
            Profile.objects.create(
                name="Abiral Khatiwada",
                title="Flutter Developer | AI Enthusiast",
                bio="I'm a passionate Flutter developer and AI enthusiast who loves turning "
                    "creative ideas into functional apps. My goal is to blend mobile development "
                    "with artificial intelligence to deliver smarter user experiences.",
                tagline="Building intelligent, beautiful, and user-friendly apps that make life easier.",
                email="abiralkhatiwada37@gmail.com",
                github="https://github.com/abiralkhatiwada",
                linkedin="https://www.linkedin.com/in/abiral-khatiwada-/",
            )
            self.stdout.write(self.style.SUCCESS("✓ Profile created"))
        else:
            self.stdout.write("Profile already exists, skipping.")

        # Create Skills
        skills = ["Flutter", "Python", "Django", "Firebase", "Git", "Dart", "Machine Learning", "PostgreSQL"]
        for i, name in enumerate(skills):
            Skill.objects.get_or_create(name=name, defaults={"order": i})
        self.stdout.write(self.style.SUCCESS(f"✓ {len(skills)} skills ensured"))

        # Create Projects
        projects_data = [
            {"title": "AI Chat App", "description": "A smart chat app built using Flutter and OpenAI API.", "link_text": "GitHub →"},
            {"title": "Image Classifier", "description": "Deep learning model integrated into a mobile app for real-time recognition.", "link_text": "View Code →"},
            {"title": "Expense Tracker", "description": "A Flutter + Firebase app to visualize and manage daily expenses.", "link_text": "Demo →"},
        ]
        for i, data in enumerate(projects_data):
            Project.objects.get_or_create(title=data["title"], defaults={**data, "order": i})
        self.stdout.write(self.style.SUCCESS(f"✓ {len(projects_data)} projects ensured"))

        # Create a sample blog post
        if not BlogPost.objects.exists():
            BlogPost.objects.create(
                title="Welcome to My Blog",
                slug="welcome-to-my-blog",
                excerpt="This is my first blog post! I'll be sharing my journey as a developer, tutorials, and insights about Flutter, AI, and more.",
                content=(
                    "Hello and welcome to my blog!\n\n"
                    "I'm excited to start sharing my thoughts, experiences, and tutorials here. "
                    "As a Flutter developer and AI enthusiast, I'll be covering topics like:\n\n"
                    "- Building beautiful mobile apps with Flutter\n"
                    "- Integrating AI and machine learning into applications\n"
                    "- Tips and tricks for Python and Django development\n"
                    "- My journey as a developer\n\n"
                    "Stay tuned for more content. Feel free to reach out if you have any topics "
                    "you'd like me to cover!\n\n"
                    "Thanks for reading!"
                ),
                is_published=True,
            )
            self.stdout.write(self.style.SUCCESS("✓ Sample blog post created"))
        else:
            self.stdout.write("Blog posts already exist, skipping.")

        self.stdout.write(self.style.SUCCESS("\n✅ Database seeded successfully!"))
