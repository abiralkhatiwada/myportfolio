import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import get_answer

@csrf_exempt
def chatbot_api(request):
    """Simple JSON API endpoint for the portfolio chatbot.
    Expects a POST request with a JSON body: {"message": "..."}
    Returns: {"answer": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    answer = get_answer(message)
    return JsonResponse({"answer": answer})
