from django.http import JsonResponse



def get_view(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a GET request"})


def get_view2(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a get request 2"})


def post_view(request):
    if request.method == "POST":
        # Получаем данные из POST-запроса
        data = request.POST
        name = data.get("name")
        age = data.get("age")

        if name and age:
            return JsonResponse({"message": f"Hello, {name}! You are {age} years old."})
        else:
            return JsonResponse({"error": "Name and age are required."}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
