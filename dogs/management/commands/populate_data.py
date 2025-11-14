"""
Django management command to populate the database with example data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dogs.models import Dog, UserProfile, Match, Favorite, Message
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Populate database with example data for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=10,
            help="Number of users to create",
        )
        parser.add_argument(
            "--dogs",
            type=int,
            default=25,
            help="Number of dogs to create",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before populating",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            self.clear_data()

        num_users = options["users"]
        num_dogs = options["dogs"]

        self.stdout.write(
            self.style.SUCCESS(f"Creating {num_users} users and {num_dogs} dogs...")
        )

        # Create users
        users = self.create_users(num_users)

        # Create user profiles
        self.create_user_profiles(users)

        # Create dogs
        dogs = self.create_dogs(users, num_dogs)

        # Create matches
        self.create_matches(dogs)

        # Create favorites
        self.create_favorites(users, dogs)

        # Create messages
        self.create_messages(users, dogs)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated database with:\n"
                f"  - {len(users)} users\n"
                f"  - {len(dogs)} dogs\n"
                f"  - Some matches, favorites, and messages"
            )
        )

    def clear_data(self):
        """Clear all existing data"""
        Match.objects.all().delete()
        Favorite.objects.all().delete()
        Message.objects.all().delete()
        Dog.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All data cleared."))

    def create_users(self, count):
        """Create example users"""
        users = []
        first_names = [
            "Анна",
            "Алексей",
            "Мария",
            "Дмитрий",
            "Елена",
            "Сергей",
            "Ольга",
            "Михаил",
            "Татьяна",
            "Владимир",
            "Ирина",
            "Павел",
            "Наталья",
            "Андрей",
            "Светлана",
            "Виктор",
            "Юлия",
            "Роман",
        ]
        last_names = [
            "Иванова",
            "Петров",
            "Сидорова",
            "Козлов",
            "Смирнова",
            "Лебедев",
            "Новикова",
            "Морозов",
            "Волкова",
            "Попов",
            "Соколова",
            "Егоров",
            "Виноградова",
            "Борисов",
            "Тарасова",
            "Комаров",
            "Орлова",
            "Кузнецов",
        ]

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}_{last_name.lower()}_{i}"
            email = f"{username}@example.com"

            user = User.objects.create_user(
                username=username,
                email=email,
                password="testpass123",
                first_name=first_name,
                last_name=last_name,
                date_joined=timezone.now()
                - timezone.timedelta(days=random.randint(1, 365)),
            )
            users.append(user)

        return users

    def create_user_profiles(self, users):
        """Create user profiles"""
        locations = [
            "Москва",
            "Санкт-Петербург",
            "Екатеринбург",
            "Новосибирск",
            "Казань",
            "Нижний Новгород",
            "Челябинск",
            "Самара",
        ]
        bios = [
            "Люблю проводить время с собакой на свежем воздухе.",
            "Активный образ жизни, ищем друзей для прогулок.",
            "Забочусь о своей собаке и хочу найти ей компанию.",
            "Опытный собаковод, готов поделиться советами.",
            "Любим играть в парке и знакомиться с другими собаками.",
            "Ищем спокойных собак для дружеских встреч.",
        ]

        for user in users:
            UserProfile.objects.create(
                user=user,
                bio=random.choice(bios),
                location=random.choice(locations),
                phone=f"+7{random.randint(9000000000, 9999999999)}",
            )

    def create_dogs(self, users, count):
        """Create example dogs"""
        dogs = []
        breeds = [
            "Лабрадор",
            "Овчарка",
            "Хаски",
            "Золотистый ретривер",
            "Немецкая овчарка",
            "Доберман",
            "Ротвейлер",
            "Бульдог",
            "Спаниель",
            "Такса",
            "Чихуахуа",
            "Мопс",
            "Бигль",
            "Корги",
            "Питбуль",
            "Алабай",
            "Шпиц",
            "Пудель",
        ]
        temperaments = [
            "дружелюбный, энергичный",
            "спокойный, послушный",
            "игривый, активный",
            "защитный, преданный",
            "дружелюбный, спокойный",
            "энергичный, игривый",
            "добрый, общительный",
            "спокойный, уравновешенный",
        ]
        descriptions = [
            "Очень дружелюбная собака, любит играть с другими собаками.",
            "Спокойная и послушная, хорошо ладит с детьми.",
            "Активная собака, нуждается в регулярных прогулках.",
            "Защитная собака, но очень добрая с знакомыми.",
            "Игривая и веселая, всегда готова к новым знакомствам.",
            "Спокойная собака, предпочитает неторопливые прогулки.",
            "Очень общительная, любит встречать новых друзей.",
            "Умная и обучаемая, знает основные команды.",
        ]

        for i in range(count):
            user = random.choice(users)
            dog = Dog.objects.create(
                owner=user,
                name=f"Дог{i+1}",
                breed=random.choice(breeds),
                age=random.randint(1, 12),
                gender=random.choice(["M", "F"]),
                size=random.choice(["S", "M", "L"]),
                temperament=random.choice(temperaments),
                looking_for=random.choice(
                    ["playmate", "companion", "mate", "friendship"]
                ),
                description=random.choice(descriptions),
                created_at=timezone.now()
                - timezone.timedelta(days=random.randint(1, 100)),
                is_active=True,
            )
            dogs.append(dog)

        return dogs

    def create_matches(self, dogs):
        """Create example matches between dogs"""
        match_count = min(len(dogs) // 2, 20)  # Create reasonable number of matches

        for _ in range(match_count):
            dog1, dog2 = random.sample(dogs, 2)

            # Don't match dogs from same owner
            if dog1.owner == dog2.owner:
                continue

            # Create match in one direction
            match, created = Match.objects.get_or_create(
                dog_from=dog1,
                dog_to=dog2,
                defaults={
                    "status": random.choice(["pending", "accepted", "declined"]),
                    "created_at": timezone.now()
                    - timezone.timedelta(days=random.randint(1, 30)),
                },
            )

            # Sometimes create reciprocal matches
            if random.random() < 0.3:
                Match.objects.get_or_create(
                    dog_from=dog2,
                    dog_to=dog1,
                    defaults={
                        "status": random.choice(["pending", "accepted", "declined"]),
                        "created_at": timezone.now()
                        - timezone.timedelta(days=random.randint(1, 30)),
                    },
                )

    def create_favorites(self, users, dogs):
        """Create example favorites"""
        for user in users[:5]:  # Only first 5 users get favorites for demo
            favorite_dogs = random.sample(dogs, min(3, len(dogs)))
            for dog in favorite_dogs:
                if dog.owner != user:  # Can't favorite own dog
                    Favorite.objects.get_or_create(
                        user=user,
                        dog=dog,
                        defaults={
                            "created_at": timezone.now()
                            - timezone.timedelta(days=random.randint(1, 20))
                        },
                    )

    def create_messages(self, users, dogs):
        """Create example messages between users"""
        # Get users who have matching dogs
        matches = Match.objects.filter(status="accepted")

        subjects = [
            "Знакомство наших собак",
            "Встреча в парке",
            "Общие прогулки",
            "Приглашение на игру",
            "Обсуждение пород",
            "Советы по дрессировке",
        ]

        contents = [
            "Привет! Хотел бы познакомить наших собак. Они могли бы стать хорошими друзьями.",
            "Моя собака очень дружелюбная и любит играть. Может, встретимся в ближайшие выходные?",
            "Видел вашу собаку в списке. Хотел бы обсудить возможность совместных прогулок.",
            "Приглашаю наших собак на игру в парке. Они точно найдут общий язык!",
            "Интересно узнать о вашем опыте с этой породой. Может, пообщаемся?",
            "Хотел бы поделиться некоторыми советами по дрессировке. Как вам идея?",
        ]

        for match in matches[:10]:  # Limit to first 10 matches
            sender = match.dog_from.owner
            receiver = match.dog_to.owner

            # Create 1-2 messages per accepted match
            for _ in range(random.randint(1, 2)):
                Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    subject=random.choice(subjects),
                    content=random.choice(contents),
                    is_read=random.choice([True, False]),
                    created_at=timezone.now()
                    - timezone.timedelta(days=random.randint(1, 7)),
                )
