from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


def get_view(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a GET request"})


def get_view2(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a get request 2"})


@csrf_exempt
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


def unified_view(request):
    if request.method == "GET":
        return JsonResponse({"message": "GET request"})
    elif request.method == "POST":
        return redirect(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlrIHJvbGw%3D"
        )  # Редирект на внешний URL


@csrf_exempt  # Добавил потому что при тестах через curl требует csrf
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        # Проверяем, существует ли пользователь с таким именем
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Создаем пользователя
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User created', 'user_id': user.id}, status=201)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Logged in'})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})
