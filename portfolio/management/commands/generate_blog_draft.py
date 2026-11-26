import json
import os
import time
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from google import genai
from google.genai import types

from portfolio.models import BlogPost

MODEL_NAME = "gemini-3.5-flash-lite"

# Four total attempts: initial request + three retries.
MAX_ATTEMPTS = 4

# Wait 10, 20, and 40 seconds between retries.
INITIAL_RETRY_DELAY = 10


class Command(BaseCommand):
    help = "Generate an AI-written blog article and save it for review."

    def is_retryable_error(self, exc):
        """Identify temporary API errors that may succeed on retry."""
        error_message = str(exc).lower()

        retryable_codes = {
            "408",
            "429",
            "500",
            "502",
            "503",
            "504",
        }

        retryable_messages = (
            "unavailable",
            "resource_exhausted",
            "too many requests",
            "high demand",
            "temporarily unavailable",
            "deadline_exceeded",
            "timeout",
            "timed out",
            "connection reset",
            "connection aborted",
            "remote disconnected",
            "internal server error",
            "bad gateway",
            "service unavailable",
            "gateway timeout",
        )

        # Check common HTTP/API status attributes.
        status_values = [
            getattr(exc, "code", None),
            getattr(exc, "status_code", None),
        ]

        response = getattr(exc, "response", None)
        if response is not None:
            status_values.append(getattr(response, "status_code", None))

        for status in status_values:
            if status is not None and str(status).lower() in retryable_codes:
                return True

        # Check the error message.
        if any(code in error_message for code in retryable_codes):
            return True

        if any(msg in error_message for msg in retryable_messages):
            return True

        return False

    def generate_article(self, client, prompt):
        """Request an article from Gemini with automatic retries."""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                self.stdout.write(
                    f"Generating article... (Attempt {attempt}/{MAX_ATTEMPTS})"
                )

                return client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.7,
                        max_output_tokens=8192,
                    ),
                )

            except Exception as exc:
                # Do not retry permanent errors such as invalid API keys.
                if not self.is_retryable_error(exc):
                    raise CommandError(f"Gemini API request failed: {exc}")

                # Stop after the final attempt.
                if attempt == MAX_ATTEMPTS:
                    raise CommandError(
                        f"Gemini API request failed after "
                        f"{MAX_ATTEMPTS} attempts: {exc}"
                    )

                wait_time = INITIAL_RETRY_DELAY * (2 ** (attempt - 1))
                self.stdout.write(
                    self.style.WARNING(
                        f"Gemini is temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                )
                time.sleep(wait_time)

        raise CommandError("Gemini article generation failed.")

    def handle(self, *args, **options):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise CommandError(
                "GEMINI_API_KEY is missing. Check your environment configuration."
            )

        # Limit AI generation to two articles in any seven-day period.
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_drafts = BlogPost.objects.filter(
            ai_generated=True,
            created_at__gte=seven_days_ago,
        ).count()

        if recent_drafts >= 2:
            self.stdout.write(
                self.style.WARNING(
                    "Weekly limit reached. Two AI-generated articles "
                    "already exist within the last seven days."
                )
            )
            return

        self.stdout.write("Connecting to Gemini...")
        client = genai.Client(api_key=api_key)

        prompt = """
You are an experienced technology writer and programming educator.

Your task is to independently choose ONE useful, interesting, and
practical blog topic for an international audience.

WEBSITE CONTEXT:
The website belongs to a developer interested in Python, Django,
web development, React, Flutter, AI, databases, and software engineering.

TOPIC REQUIREMENTS:
- Choose a topic that people genuinely search for.
- Prefer practical tutorials, technical explanations, and useful guides.
- Avoid generic motivational articles and shallow listicles.
- Avoid repeating common beginner topics without a fresh angle.
- Choose a topic suitable for an English-language developer blog.
- Do not invent recent news, statistics, benchmarks, or sources.
- Do not claim that code has been tested unless it actually has.

ARTICLE REQUIREMENTS:
- Write a detailed, genuinely useful article of approximately
  1,200–1,600 words.
- Use clear, natural English.
- Organize the article with descriptive Markdown headings.
- Include practical examples and code snippets when relevant.
- Explain code rather than simply displaying it.
- Include an introduction and a meaningful conclusion.
- Avoid keyword stuffing and repetitive paragraphs.
- Do not use HTML.
- Do not include image links or fabricated citations.

SEO REQUIREMENTS:
- Create a clear, natural article title.
- Write an engaging excerpt under 500 characters.
- Write an SEO title.
- Write a meta description under 160 characters.
- Provide 5–10 relevant keywords.

Return ONLY valid JSON with exactly these keys:
{
    "title": "Article title",
    "excerpt": "Short article summary",
    "seo_title": "SEO title",
    "meta_description": "SEO description",
    "keywords": "keyword one, keyword two",
    "content": "Complete Markdown article"
}
"""

        self.stdout.write("Asking Gemini to prepare an article...")

        # Generate the article, retrying temporary API failures.
        response = self.generate_article(client, prompt)
        if not response.text:
            raise CommandError("Gemini returned an empty response.")

        try:
            article = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise CommandError("Gemini did not return valid JSON.") from exc

        if not isinstance(article, dict):
            raise CommandError("Gemini returned an invalid article format.")

        required_fields = [
            "title",
            "excerpt",
            "seo_title",
            "meta_description",
            "keywords",
            "content",
        ]

        for field in required_fields:
            value = article.get(field)
            if not isinstance(value, str) or not value.strip():
                raise CommandError(
                    f"Generated article is missing a valid '{field}' field."
                )

        title = article["title"].strip()[:300]
        excerpt = article["excerpt"].strip()[:500]
        seo_title = article["seo_title"].strip()[:300]
        meta_description = article["meta_description"].strip()[:160]
        keywords = article["keywords"].strip()[:500]
        content = article["content"].strip()

        if len(content) < 1000:
            raise CommandError(
                "Generated article is unexpectedly short. No draft was saved."
            )

        base_slug = slugify(title)[:290].strip("-")
        if not base_slug:
            raise CommandError("Could not create a valid slug from the title.")

        with transaction.atomic():
            slug = base_slug
            suffix = 2

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug[:280]}-{suffix}"
                suffix += 1

            post = BlogPost.objects.create(
                title=title,
                slug=slug,
                excerpt=excerpt,
                seo_title=seo_title,
                meta_description=meta_description,
                keywords=keywords,
                content=content,
                status="pending_review",
                is_published=False,
                ai_generated=True,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created article draft: {post.title}"
            )
        )
        self.stdout.write(f"Slug: {post.slug}")
        self.stdout.write("Status: Pending Review")
        self.stdout.write("Published: No")