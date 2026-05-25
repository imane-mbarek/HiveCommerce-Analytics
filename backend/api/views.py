from django.http import JsonResponse


def health_check(_request):
    return JsonResponse({"status": "ok", "service": "HiveCommerce backend"})


def project_info(_request):
    return JsonResponse(
        {
            "name": "HiveCommerce Analytics",
            "description": "Backend API for the Big Data e-commerce analytics project.",
            "modules": ["data", "hive", "python", "dashboard"],
        }
    )

