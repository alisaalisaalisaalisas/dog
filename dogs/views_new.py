# Дополнительные views для menu приложения
from django.shortcuts import render


def premium(request):
    """Премиум подписка"""
    return render(request, "dogs/premium.html", {"page_title": "Премиум подписка"})


def meetings(request):
    """Организация встреч"""
    return render(request, "dogs/meetings.html", {"page_title": "Организация встреч"})


def contacts(request):
    """Контакты"""
    return render(request, "dogs/contacts.html", {"page_title": "Контакты"})


def privacy(request):
    """Политика конфиденциальности"""
    return render(
        request, "dogs/privacy.html", {"page_title": "Политика конфиденциальности"}
    )
