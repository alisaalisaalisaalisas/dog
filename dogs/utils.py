import os
import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count, Q
from PIL import Image

from .models import Dog, Favorite, Match


def calculate_dog_compatibility_score(dog1, dog2):
    """
    Рассчитывает совместимость между двумя собаками на основе различных факторов.

    Returns score from 0 to 100 where 100 is perfect match.
    """
    if dog1.id == dog2.id:
        return 0  # Собака не может быть совместима с собой

    score = 0
    max_score = 100

    # Возрастная совместимость (25 points max)
    age_diff = abs(dog1.age - dog2.age)
    if age_diff <= 1:
        score += 25
    elif age_diff <= 3:
        score += 20
    elif age_diff <= 5:
        score += 15
    elif age_diff <= 8:
        score += 10
    else:
        score += 5

    # Размерная совместимость (20 points max)
    size_compatibility = {
        ("S", "S"): 20,
        ("S", "M"): 15,
        ("S", "L"): 5,
        ("M", "S"): 15,
        ("M", "M"): 20,
        ("M", "L"): 15,
        ("L", "S"): 5,
        ("L", "M"): 15,
        ("L", "L"): 20,
    }
    score += size_compatibility.get((dog1.size, dog2.size), 10)

    # Половая совместимость (15 points max)
    if dog1.gender != dog2.gender:
        score += 15  # Разные полы - лучше для размножения/игры
    else:
        score += 10  # Одинаковые пола - хорошо для дружбы

    # Совместимость по целям знакомства (20 points max)
    compatible_goals = {
        ("playmate", "playmate"): 20,
        ("companion", "companion"): 20,
        ("mate", "mate"): 20,
        ("friendship", "friendship"): 20,
        ("playmate", "companion"): 15,
        ("companion", "playmate"): 15,
        ("playmate", "friendship"): 15,
        ("friendship", "playmate"): 15,
        ("companion", "friendship"): 15,
        ("friendship", "companion"): 15,
    }
    score += compatible_goals.get((dog1.looking_for, dog2.looking_for), 10)

    # Порода (5 points max) - небольшой бонус за одинаковые породы
    if dog1.breed.lower() == dog2.breed.lower():
        score += 5

    # Характер (15 points max) - анализ ключевых слов в описании характера
    temperament_keywords = {
        "дружелюбный": ["дружелюбный", "дружелюбная", "общительный", "общительная"],
        "энергичный": [
            "энергичный",
            "энергичная",
            "активный",
            "активная",
            "игривый",
            "игривая",
        ],
        "спокойный": [
            "спокойный",
            "спокойная",
            "мирный",
            "мирная",
            "уравновешенный",
            "уравновешенная",
        ],
        "защитный": ["защитный", "защитная", "сторожевой", "сторожевая"],
        "послушный": ["послушный", "послушная", "управляемый", "управляемая"],
    }

    temperament_score = 0
    for dog1_word in temperament_keywords.keys():
        if dog1_word in dog1.temperament.lower():
            for dog2_word in temperament_keywords.keys():
                if dog2_word in dog2.temperament.lower():
                    if dog1_word == dog2_word:
                        temperament_score += 7.5
                    elif dog1_word in ["дружелюбный", "энергичный"] and dog2_word in [
                        "дружелюбный",
                        "энергичный",
                    ]:
                        temperament_score += 5

    score += min(temperament_score, 15)

    return min(score, max_score)


def get_compatible_dogs(user_dog, exclude_matches=True):
    """
    Возвращает список совместимых собак для данной собаки пользователя.

    Args:
        user_dog: Dog объект собаки пользователя
        exclude_matches: Исключать ли уже существующие мэтчи

    Returns:
        QuerySet отсортированных по совместимости Dog объектов
    """
    # Начинаем со всех активных собак, кроме текущей
    compatible_dogs = Dog.objects.filter(is_active=True).exclude(id=user_dog.id)

    # Исключаем собак владельца
    compatible_dogs = compatible_dogs.exclude(owner=user_dog.owner)

    # Фильтруем по возрасту (не слишком большая разница)
    compatible_dogs = compatible_dogs.filter(
        age__gte=max(0, user_dog.age - 10), age__lte=user_dog.age + 10
    )

    # Исключаем уже существующие мэтчи если нужно
    if exclude_matches:
        existing_matches = Match.objects.filter(
            Q(dog_from=user_dog) | Q(dog_to=user_dog)
        ).values_list("dog_from_id", "dog_to_id")

        matched_dog_ids = set()
        for match in existing_matches:
            if match[0] == user_dog.id:
                matched_dog_ids.add(match[1])
            else:
                matched_dog_ids.add(match[0])

        compatible_dogs = compatible_dogs.exclude(id__in=matched_dog_ids)

    # Вычисляем совместимость для каждой собаки
    compatible_dogs_with_scores = []
    for dog in compatible_dogs:
        score = calculate_dog_compatibility_score(user_dog, dog)
        if score >= 30:  # Минимальный порог совместимости
            compatible_dogs_with_scores.append((dog, score))

    # Сортируем по убыванию совместимости
    compatible_dogs_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Возвращаем только Dog объекты, отсортированные по совместимости
    return [dog for dog, score in compatible_dogs_with_scores]


def create_match(dog_from, dog_to):
    """
    Создает новый мэтч между двумя собаками.

    Returns:
        Match объект или None если мэтч уже существует
    """
    # Проверяем, не существует ли уже мэтч
    existing_match = Match.objects.filter(
        Q(dog_from=dog_from, dog_to=dog_to) | Q(dog_from=dog_to, dog_to=dog_from)
    ).first()

    if existing_match:
        return existing_match

    # Создаем новый мэтч
    match = Match.objects.create(dog_from=dog_from, dog_to=dog_to, status="pending")

    return match


def accept_match(match):
    """
    Принимает мэтч. Если мэтч был взаимным, создает статус 'accepted'.

    Returns:
        True если мэтч принят успешно, False иначе
    """
    if match.status != "pending":
        return False

    # Проверяем обратный мэтч
    reverse_match = Match.objects.filter(
        dog_from=match.dog_to, dog_to=match.dog_from
    ).first()

    if reverse_match and reverse_match.status == "pending":
        # Взаимная симпатия!
        match.status = "accepted"
        reverse_match.status = "accepted"
        match.save()
        reverse_match.save()
    else:
        # Простое принятие
        match.status = "accepted"
        match.save()

    return True


def decline_match(match):
    """
    Отклоняет мэтч.

    Returns:
        True если мэтч отклонен успешно, False иначе
    """
    if match.status != "pending":
        return False

    match.status = "declined"
    match.save()

    return True


def get_mutual_matches(user):
    """
    Возвращает список взаимных мэтчей (статус 'accepted') для пользователя.

    Returns:
        QuerySet Match объектов со статусом 'accepted'
    """
    return Match.objects.filter(
        Q(dog_from__owner=user) | Q(dog_to__owner=user), status="accepted"
    ).select_related("dog_from", "dog_to", "dog_from__owner", "dog_to__owner")


def get_pending_matches(user):
    """
    Возвращает список ожидающих мэтчей для пользователя.

    Returns:
        QuerySet Match объектов со статусом 'pending'
    """
    return Match.objects.filter(
        Q(dog_from__owner=user) | Q(dog_to__owner=user), status="pending"
    ).select_related("dog_from", "dog_to", "dog_from__owner", "dog_to__owner")


def get_match_statistics(user):
    """
    Возвращает статистику мэтчей для пользователя.

    Returns:
        dict с количеством различных типов мэтчей
    """
    user_dogs = Dog.objects.filter(owner=user)
    if not user_dogs.exists():
        return {
            "pending_sent": 0,
            "pending_received": 0,
            "accepted": 0,
            "declined": 0,
            "total": 0,
        }

    user_dog_ids = user_dogs.values_list("id", flat=True)

    # Статистика по статусам
    pending_sent = Match.objects.filter(
        dog_from_id__in=user_dog_ids, status="pending"
    ).count()
    pending_received = Match.objects.filter(
        dog_to_id__in=user_dog_ids, status="pending"
    ).count()
    accepted = Match.objects.filter(
        Q(dog_from_id__in=user_dog_ids) | Q(dog_to_id__in=user_dog_ids),
        status="accepted",
    ).count()
    declined = Match.objects.filter(
        Q(dog_from_id__in=user_dog_ids) | Q(dog_to_id__in=user_dog_ids),
        status="declined",
    ).count()

    return {
        "pending_sent": pending_sent,
        "pending_received": pending_received,
        "accepted": accepted,
        "declined": declined,
        "total": pending_sent + pending_received + accepted + declined,
    }


# Image Optimization and Default Image Functions
def optimize_image(image_field, max_width=800, max_height=600, quality=85):
    """
    Optimize uploaded image by resizing and compressing

    Args:
        image_field: Django ImageField instance
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)

    Returns:
        Optimized image file
    """
    if not image_field or not hasattr(image_field, "path"):
        return None

    try:
        # Open the image
        image = Image.open(image_field)

        # Convert to RGB if necessary (for JPEG)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Calculate new size maintaining aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Create a new image with optimized dimensions
        output = BytesIO()

        # Save optimized image
        image.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        # Create new filename
        name, ext = os.path.splitext(image_field.name)
        new_filename = f"{name}_{uuid.uuid4().hex[:8]}.jpg"

        # Create new InMemoryUploadedFile
        return InMemoryUploadedFile(
            output,
            "ImageField",
            new_filename,
            "image/jpeg",
            len(output.getvalue()),
            None,
        )
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return image_field


def create_default_dog_image():
    """
    Create a default dog image placeholder

    Returns:
        ContentFile with default dog image data
    """
    # Create a simple placeholder image
    img = Image.new("RGB", (400, 300), color="#e2e8f0")

    # Add text
    from PIL import ImageDraw, ImageFont

    draw = ImageDraw.Draw(img)

    try:
        # Try to use a larger font
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        try:
            # Fallback to default font
            font = ImageFont.load_default()
        except:
            font = None

    # Add text in center
    text = "🐕"
    if font:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width, text_height = 100, 100

    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    draw.text((x, y), text, fill="#64748b", font=font)

    # Save to BytesIO
    output = BytesIO()
    img.save(output, format="PNG", quality=90)
    output.seek(0)

    return ContentFile(output.getvalue(), name="default_dog.png")


def create_default_avatar():
    """
    Create a default user avatar placeholder

    Returns:
        ContentFile with default avatar image data
    """
    # Create a simple placeholder avatar
    img = Image.new("RGB", (200, 200), color="#f1f5f9")

    # Add text
    from PIL import ImageDraw, ImageFont

    draw = ImageDraw.Draw(img)

    try:
        # Try to use a larger font
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        try:
            # Fallback to default font
            font = ImageFont.load_default()
        except:
            font = None

    # Add text in center
    text = "👤"
    if font:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width, text_height = 50, 50

    x = (200 - text_width) // 2
    y = (200 - text_height) // 2
    draw.text((x, y), text, fill="#64748b", font=font)

    # Save to BytesIO
    output = BytesIO()
    img.save(output, format="PNG", quality=90)
    output.seek(0)

    return ContentFile(output.getvalue(), name="default_avatar.png")
