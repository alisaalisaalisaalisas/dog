from django.db import models
from django.contrib.auth.models import User


class Dog(models.Model):
    """Модель собаки"""

    GENDER_CHOICES = [
        ("M", "Мальчик"),
        ("F", "Девочка"),
    ]

    SIZE_CHOICES = [
        ("S", "Маленькая"),
        ("M", "Средняя"),
        ("L", "Большая"),
    ]

    LOOKING_FOR_CHOICES = [
        ("playmate", "Друга для игр"),
        ("companion", "Компаньона"),
        ("mate", "Партнера для жизни"),
        ("friendship", "Дружбы"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dogs", verbose_name="Владелец"
    )
    name = models.CharField(max_length=100, verbose_name="Кличка")
    breed = models.CharField(max_length=100, verbose_name="Порода")
    age = models.PositiveIntegerField(verbose_name="Возраст (в годах)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, verbose_name="Размер")
    temperament = models.CharField(
        max_length=100,
        verbose_name="Характер",
        help_text="Например: дружелюбный, энергичный, спокойный",
    )
    looking_for = models.CharField(
        max_length=20,
        choices=LOOKING_FOR_CHOICES,
        verbose_name="Ищет",
        help_text="Цель знакомства",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Расскажите о вашей собаке: привычки, любимые занятия и т.д.",
    )
    photo = models.ImageField(
        upload_to="dogs/", blank=True, null=True, verbose_name="Фото"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активный профиль")

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.breed})"


class UserProfile(models.Model):
    """Расширенная модель пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    bio = models.TextField(blank=True, verbose_name="О себе")
    location = models.CharField(max_length=100, blank=True, verbose_name="Город")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


class Match(models.Model):
    """Модель для хранения мэтчей собак"""

    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принят"),
        ("declined", "Отклонен"),
    ]

    dog_from = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="matches_sent",
        verbose_name="Собака-инициатор",
    )
    dog_to = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="matches_received",
        verbose_name="Собака-цель",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Мэтч"
        verbose_name_plural = "Мэтчи"
        unique_together = ["dog_from", "dog_to"]

    def __str__(self):
        return f"{self.dog_from.name} → {self.dog_to.name}: {self.get_status_display()}"


class Message(models.Model):
    """Модель для сообщений между пользователями"""

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent",
        verbose_name="Отправитель",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_received",
        verbose_name="Получатель",
    )
    subject = models.CharField(max_length=200, verbose_name="Тема")
    content = models.TextField(verbose_name="Содержание")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"От {self.sender.username} к {self.receiver.username}: {self.subject}"


class Favorite(models.Model):
    """Модель для избранных собак"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Собака",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ["user", "dog"]

    def __str__(self):
        return f"{self.user.username} добавил в избранное {self.dog.name}"
