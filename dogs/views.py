from django.shortcuts import render


def home(request):
    """Главная страница"""
    return render(request, "dogs/home.html")


def register_dog(request):
    """Регистрация собаки"""
    return render(
        request,
        "dogs/home.html",
        {
            "page_title": "Регистрация собаки",
            "message": "Здесь будет форма регистрации собаки",
        },
    )


def matches(request):
    """Страница подбора пар"""
    return render(
        request,
        "dogs/home.html",
        {
            "page_title": "Найти пару",
            "message": "Здесь будут анкеты собак для знакомства",
        },
    )


def about(request):
    """О сервисе"""
    return render(
        request,
        "dogs/home.html",
        {"page_title": "О сервисе", "message": "Информация о сервисе DogDating"},
    )


def breeds(request):
    """Породы"""
    return render(
        request,
        "dogs/home.html",
        {"page_title": "Породы собак", "message": "Каталог пород собак"},
    )


def events(request):
    """Мероприятия"""
    return render(
        request,
        "dogs/home.html",
        {"page_title": "Мероприятия", "message": "Календарь мероприятий для собак"},
    )


def tips(request):
    """Советы"""
    return render(
        request,
        "dogs/home.html",
        {"page_title": "Полезные советы", "message": "Советы по уходу за собаками"},
    )


def dog_profile(request, dog_id):
    """Профиль собаки"""
    return render(
        request,
        "dogs/home.html",
        {
            "page_title": f"Профиль собаки #{dog_id}",
            "message": f"Здесь будет информация о собаке с ID: {dog_id}",
            "dog_id": dog_id,
        },
    )
