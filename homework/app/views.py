from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required


User = get_user_model()


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


def unified_view(request):
    if request.method == "GET":
        return JsonResponse({"message": "GET request"})
    elif request.method == "POST":
        return redirect(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlrIHJvbGw%3D"
        )  # Редирект на внешний URL


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        # Проверяем, существует ли пользователь с таким именем
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        # Создаем пользователя
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created", "user_id": user.id}, status=201)
    elif request.method == "GET":
        # Отображаем HTML-форму для регистрации
        return render(request, 'register.html')
    else:
        return JsonResponse({"error": "Only GET or POST methods are allowed"}, status=405)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Возвращаем JSON с сообщением об успешном входе
            return JsonResponse({"message": "Login successful"})
        else:
            # Возвращаем JSON с ошибкой
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    elif request.method == "GET":
        return render(request, 'login.html')
    else:
        return JsonResponse({"error": "Only GET or POST methods are allowed"}, status=405)


def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def user_crud(request, pk=None):
    if request.method == "GET":
        if pk:
            # Получаем данные одного пользователя
            try:
                user = User.objects.get(pk=pk)
                data = {"username": user.username, "email": user.email}
                return JsonResponse(data)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
        else:
            return render(request, 'user_crud.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return JsonResponse({"message": "User created"}, status=201)
    elif request.method == "PUT":
        try:
            user = User.objects.get(pk=pk)
            user.username = request.POST.get("username", user.username)
            user.email = request.POST.get("email", user.email)
            user.save()
            return JsonResponse({"message": "User updated"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    elif request.method == "DELETE":
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({"message": "User deleted"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


def reset_password_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f"/reset-password/{uid}/{token}/")
            send_mail(
                "Password Reset",
                f"Click the link to reset your password: {reset_url}",
                "nikostdjango@yandex.ru",
                [email],
                fail_silently=False,
            )
            return JsonResponse({"message": "Password reset email sent successfully."})
        else:
            return JsonResponse({"error": "User not found"}, status=404)
    return render(request, "reset_password_request.html")


def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Декодируем uid
        user = User.objects.get(pk=uid)  # Находим пользователя
        if default_token_generator.check_token(user, token):  # Проверяем токен
            if request.method == "POST":
                new_password = request.POST.get("new_password")  # Получаем новый пароль
                user.set_password(new_password)  # Устанавливаем новый пароль
                user.save()  # Сохраняем пользователя
                return render(request, "password_reset_success.html")
            # Если метод GET, отображаем форму для ввода нового пароля
            return render(request, "reset_password_confirm.html")
        return JsonResponse({"error": "Invalid token"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return JsonResponse({"message": "Account deleted"})
    elif request.method == "GET":
        # Отображаем HTML-шаблон для подтверждения удаления аккаунта
        return render(request, 'myapp/delete_account.html')
    return JsonResponse({"error": "Only GET or POST methods are allowed"}, status=405)


def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.save()
        return JsonResponse({"message": "Profile updated"})
    elif request.method == "GET":
        return render(request, 'myapp/edit_profile.html', {'user': request.user})
    return JsonResponse({"error": "Only GET or POST methods are allowed"}, status=405)


@login_required  # Только авторизованные пользователи могут просматривать профиль
def profile_view(request):
    user = request.user  # Получаем текущего пользователя
    context = {
        'username': user.username,
        'email': user.email,
    }
    return render(request, 'profile.html', context)
