# DogDating - Comprehensive Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Application Structure](#application-structure)
5. [Database Models](#database-models)
6. [Views and URL Routing](#views-and-url-routing)
7. [Forms](#forms)
8. [Services Layer](#services-layer)
9. [Template System](#template-system)
10. [Static Files and Media](#static-files-and-media)
11. [Configuration and Settings](#configuration-and-settings)
12. [Authentication and Authorization](#authentication-and-authorization)
13. [Admin Interface](#admin-interface)
14. [Management Commands](#management-commands)
15. [Testing Infrastructure](#testing-infrastructure)
16. [Docker Deployment](#docker-deployment)
17. [API Reference](#api-reference)
18. [Utility Functions](#utility-functions)
19. [Security Considerations](#security-considerations)
20. [Performance Optimizations](#performance-optimizations)

---

## Project Overview

**DogDating** is a Django-based web application that helps dog owners find compatible companions for their pets. The platform features:

- User authentication with registration, login, and password management
- Dog profile creation and management with photo uploads
- Dog matching system based on compatibility scores
- Favorites system for saving interesting dogs
- Russian language interface (LANGUAGE_CODE='ru-ru')
- Responsive design with mobile optimization
- Dark/Light theme support

### Key Features

| Feature | Description |
|---------|-------------|
| User Management | Registration, login, profile editing, password change, account deletion |
| Dog Profiles | CRUD operations with photo upload, validation, and filtering |
| Matching System | Compatibility scoring and match management (pending/accepted/declined) |
| Favorites | Add/remove dogs from favorites with AJAX support |
| Search & Filter | Filter dogs by breed, age, gender, and size |
| Pagination | All list views support pagination |
| Dynamic Menus | Configurable navigation menu system |

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Programming language |
| Django | 5.0+ | Web framework |
| PostgreSQL | 16 | Production database |
| SQLite | 3 | Development database |
| Pillow | 10.0+ | Image processing |
| Gunicorn | 21.2+ | WSGI HTTP server |

### Additional Dependencies

```
Django>=5.0,<6.0
Pillow>=10.0.0
django-environ>=0.11.2
psycopg2-binary>=2.9
gunicorn>=21.2.0
django-cors-headers>=4.3.0
whitenoise>=6.6.0
```

### Development/Testing Dependencies

```
pytest>=7.0
pytest-django>=4.5
factory-boy>=3.3
coverage>=7.0
```

---

## Project Architecture

### Directory Structure

```
dog/
├── manage.py                    # Django management script
├── requirements.txt             # Production dependencies
├── requirements-test.txt        # Test dependencies
├── Dockerfile                   # Docker build configuration
├── docker-compose.yml           # Docker Compose services
├── pyproject.toml              # Python project configuration
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (not in repo)
├── .coveragerc                 # Coverage configuration
│
├── project/                    # Django project configuration
│   ├── __init__.py
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI application
│   ├── asgi.py                 # ASGI application
│   └── settings/               # Settings package
│       ├── __init__.py         # Default exports development
│       ├── base.py             # Shared settings
│       ├── development.py      # Development overrides
│       └── production.py       # Production overrides
│
├── dogs/                       # Main application
│   ├── __init__.py
│   ├── admin.py                # Admin configuration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Form definitions
│   ├── models.py               # Database models
│   ├── urls.py                 # URL patterns
│   ├── utils.py                # Utility functions
│   ├── views.py                # View functions
│   ├── views_new.py            # Additional views
│   ├── management/
│   │   └── commands/
│   │       └── populate_data.py # Demo data population
│   ├── migrations/             # Database migrations
│   ├── static/                 # Static files
│   ├── templates/dogs/         # HTML templates
│   └── templatetags/
│       └── dogs_tags.py        # Custom template tags
│
├── menu_app/                   # Menu management application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Menu and MenuItem models
│   ├── management/
│   │   └── commands/
│   │       └── setup_menus.py  # Menu setup command
│   ├── migrations/
│   ├── templates/menu/
│   └── templatetags/
│       └── menu_tags.py        # Menu template tags
│
├── services/                   # Business logic layer
│   ├── dog_service.py          # Dog-related business logic
│   ├── favorites_service.py    # Favorites management
│   └── match_service.py        # Match management
│
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures
│   ├── factories.py            # Factory Boy factories
│   ├── test_api/
│   ├── test_db.py
│   ├── test_errors/
│   ├── test_forms/
│   ├── test_integration/
│   ├── test_models/
│   ├── test_permissions/
│   ├── test_services/
│   ├── test_templatetags/
│   ├── test_utils/
│   └── test_views/
│
├── media/                      # User-uploaded files
│   ├── dogs/                   # Dog photos
│   └── avatars/                # User avatars
│
└── staticfiles/                # Collected static files
```

---

## Application Structure

### dogs (Main Application)

The primary application handling all dog-related functionality:

- **Models**: Dog, UserProfile, Match, Message, Favorite
- **Views**: Authentication, CRUD operations, matching, favorites
- **Forms**: Registration, login, dog profile, search filters
- **Templates**: All user-facing HTML templates
- **Static**: CSS, JavaScript, images

### menu_app (Menu Management)

Handles dynamic navigation menus:

- **Models**: Menu, MenuItem (hierarchical structure)
- **Template Tags**: `draw_menu` for rendering menus
- **Commands**: `setup_menus` for initial menu configuration

### services (Business Logic Layer)

Separates business logic from views:

- **dog_service.py**: Dog ownership verification, public dog access
- **favorites_service.py**: Toggle favorites with permissions
- **match_service.py**: Match creation, acceptance, decline

---

## Database Models

### Dog Model

```python
class Dog(models.Model):
    # Choices
    GENDER_CHOICES = [("M", "Мальчик"), ("F", "Девочка")]
    SIZE_CHOICES = [("S", "Маленькая"), ("M", "Средняя"), ("L", "Большая")]
    LOOKING_FOR_CHOICES = [
        ("playmate", "Друга для игр"),
        ("companion", "Компаньона"),
        ("mate", "Партнера для жизни"),
        ("friendship", "Дружбы"),
    ]
    
    # Fields
    owner = ForeignKey(User, CASCADE, related_name="dogs")
    name = CharField(max_length=100)
    breed = CharField(max_length=100)
    age = PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    size = CharField(max_length=1, choices=SIZE_CHOICES)
    temperament = CharField(max_length=100)
    looking_for = CharField(max_length=20, choices=LOOKING_FOR_CHOICES)
    description = TextField()
    photo = ImageField(upload_to="dogs/", validators=[validate_dog_image])
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # Constraints
    constraints = [
        UniqueConstraint(fields=["owner", "name"], name="unique_dog_name_per_owner")
    ]
```

**Validation Rules:**
- Age: 0-20 years
- Photo: JPEG, PNG, WebP; max 5MB
- Name: Unique per owner

### UserProfile Model

```python
class UserProfile(models.Model):
    user = OneToOneField(User, CASCADE, related_name="profile")
    bio = TextField(blank=True)
    location = CharField(max_length=100, blank=True)
    phone = CharField(max_length=20, blank=True)
    avatar = ImageField(upload_to="avatars/", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Match Model

```python
class Match(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принят"),
        ("declined", "Отклонен"),
    ]
    
    dog_from = ForeignKey(Dog, CASCADE, related_name="matches_sent")
    dog_to = ForeignKey(Dog, CASCADE, related_name="matches_received")
    status = CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # Constraints & Indexes
    constraints = [UniqueConstraint(fields=["dog_from", "dog_to"], name="unique_match_dog_from_dog_to")]
    indexes = [
        Index(fields=["dog_from"]),
        Index(fields=["dog_to"]),
        Index(fields=["dog_from", "dog_to"]),
    ]
```

### Favorite Model

```python
class Favorite(models.Model):
    user = ForeignKey(User, CASCADE, related_name="favorite_dogs")
    dog = ForeignKey(Dog, CASCADE, related_name="favorited_by")
    created_at = DateTimeField(auto_now_add=True)
    
    # Constraints & Indexes
    constraints = [UniqueConstraint(fields=["user", "dog"], name="unique_favorite_per_user_and_dog")]
    indexes = [
        Index(fields=["user"]),
        Index(fields=["dog"]),
        Index(fields=["user", "dog"]),
    ]
```

### Message Model

```python
class Message(models.Model):
    sender = ForeignKey(User, CASCADE, related_name="messages_sent")
    receiver = ForeignKey(User, CASCADE, related_name="messages_received")
    subject = CharField(max_length=200)
    content = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

### Menu Models

```python
class Menu(models.Model):
    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)

class MenuItem(models.Model):
    menu = ForeignKey(Menu, CASCADE, related_name="items")
    parent = ForeignKey("self", CASCADE, null=True, blank=True, related_name="children")
    title = CharField(max_length=100)
    url = CharField(max_length=200, blank=True)
    named_url = CharField(max_length=100, blank=True)
    order = IntegerField(default=0)
```

---

## Views and URL Routing

### URL Patterns

| URL Pattern | View | Name | Auth Required |
|-------------|------|------|---------------|
| `/` | `landing_page` | `landing_page` | No |
| `/home/` | `home` | `home` | No |
| `/register/` | `register` | `register` | No |
| `/login/` | `user_login` | `login` | No |
| `/logout/` | `user_logout` | `logout` | No |
| `/dashboard/` | `dashboard` | `dashboard` | Yes |
| `/profile/` | `profile_view` | `profile` | Yes |
| `/profile/edit/` | `profile_edit` | `profile_edit` | Yes |
| `/change-password/` | `change_password` | `change_password` | Yes |
| `/delete-account/` | `delete_account` | `delete_account` | Yes |
| `/dogs/` | `dog_list` | `dog_list` | No |
| `/dogs/create/` | `dog_create` | `dog_create` | Yes |
| `/dogs/<pk>/` | `dog_detail` | `dog_detail` | No |
| `/dogs/<pk>/edit/` | `dog_update` | `dog_update` | Yes (owner) |
| `/dogs/<pk>/delete/` | `dog_delete` | `dog_delete` | Yes (owner) |
| `/dogs/<pk>/favorite/` | `toggle_favorite` | `toggle_favorite` | Yes |
| `/matches/` | `matches_list` | `matches_list` | Yes |
| `/favorites/` | `favorites_list` | `favorites_list` | Yes |
| `/about/` | `about` | `about` | No |
| `/breeds/` | `breeds` | `breeds` | No |
| `/events/` | `events` | `events` | No |
| `/tips/` | `tips` | `tips` | No |
| `/contacts/` | `contacts` | `contacts` | No |
| `/privacy/` | `privacy` | `privacy` | No |

### View Functions Summary

#### Authentication Views

- **`landing_page(request)`**: Home page for unauthenticated users, redirects to dashboard if logged in
- **`register(request)`**: User registration with automatic UserProfile creation
- **`user_login(request)`**: Login with "remember me" option (2-week session)
- **`user_logout(request)`**: Logout and redirect to landing page

#### Dashboard & Profile Views

- **`dashboard(request)`**: User's personal dashboard with statistics
- **`profile_view(request)`**: View user profile
- **`profile_edit(request)`**: Edit user profile
- **`change_password(request)`**: Change password with session refresh
- **`delete_account(request)`**: Delete account with password confirmation

#### Dog CRUD Views

- **`dog_list(request)`**: Paginated list with filters (12 per page)
- **`dog_detail(request, pk)`**: Dog detail with favorite status
- **`dog_create(request)`**: Create new dog profile
- **`dog_update(request, pk)`**: Edit dog (owner only)
- **`dog_delete(request, pk)`**: Delete dog (owner only)

#### Interaction Views

- **`toggle_favorite(request, pk)`**: AJAX endpoint for favorites
- **`matches_list(request)`**: Paginated matches (10 per page)
- **`favorites_list(request)`**: Paginated favorites (12 per page)

#### Error Handlers

- **`handler404(request, exception)`**: Custom 404 page
- **`handler500(request)`**: Custom 500 page

---

## Forms

### User Forms

#### UserRegistrationForm
```python
class UserRegistrationForm(UserCreationForm):
    email = EmailField(required=True)
    # Auto-creates UserProfile on save
```

#### UserLoginForm
```python
class UserLoginForm(AuthenticationForm):
    username = CharField()
    password = CharField()
    remember_me = BooleanField(required=False)
```

#### UserProfileForm
```python
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "location", "phone", "avatar"]
```

#### PasswordChangeForm
```python
class PasswordChangeForm(Form):
    old_password = CharField()
    new_password1 = CharField()
    new_password2 = CharField()
    # Validates password match
```

#### AccountDeletionForm
```python
class AccountDeletionForm(Form):
    confirm_deletion = BooleanField(required=True)
    password = CharField()
```

### Dog Forms

#### DogForm
```python
class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "breed", "age", "gender", "size", 
                  "temperament", "looking_for", "description", "photo"]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        # Auto-assigns owner
    
    def clean_age(self):
        # Validates 0-20 range
    
    def clean_photo(self):
        # Validates size (5MB) and MIME type
```

#### DogSearchForm
```python
class DogSearchForm(Form):
    breed = CharField(required=False)
    age_min = IntegerField(required=False)
    age_max = IntegerField(required=False)
    gender = ChoiceField(required=False, choices=[("", "Любой")] + GENDER_CHOICES)
    size = ChoiceField(required=False, choices=[("", "Любой")] + SIZE_CHOICES)
```

#### MatchForm
```python
class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ["dog_from", "dog_to"]
    
    def clean(self):
        # Prevents self-match
```

#### FavoriteForm
```python
class FavoriteForm(ModelForm):
    class Meta:
        model = Favorite
        fields = ["user", "dog"]
    
    def clean(self):
        # Prevents favoriting own dog
```

---

## Services Layer

### dog_service.py

```python
def get_dog_for_owner(owner, dog_id, *, active_only=True) -> Dog:
    """Returns dog owned by user or raises PermissionDenied."""
    
def get_public_dog(dog_id, *, active_only=True) -> Dog:
    """Returns publicly viewable dog or raises DoesNotExist."""
```

### favorites_service.py

```python
def toggle_favorite_for_user(user, dog_id) -> tuple[bool, str]:
    """Toggle favorite, returns (is_favorite, message).
    
    Raises:
        Dog.DoesNotExist: Dog not found
        PermissionDenied: User not authenticated
    """
```

### match_service.py

```python
def create_match_for_user(user, dog_from_id, dog_to_id) -> Match:
    """Create match, validates ownership and prevents self-match."""

def accept_match_for_user(user, match) -> bool:
    """Accept match if user owns involved dog."""

def decline_match_for_user(user, match) -> bool:
    """Decline match if user owns involved dog."""
```

---

## Template System

### Base Template Structure

```
dogs/templates/dogs/
├── base.html              # Main layout (76KB with CSS/JS)
├── landing.html           # Landing page (35KB)
├── dashboard.html         # User dashboard
├── dog_list.html          # Dogs listing with filters
├── dog_detail.html        # Dog profile view
├── dog_form.html          # Create/Edit dog
├── dog_confirm_delete.html
├── login.html
├── register.html
├── profile.html
├── profile_edit.html
├── change_password.html
├── delete_account.html
├── matches.html
├── favorites.html
├── about.html
├── breeds.html
├── events.html
├── tips.html
├── contacts.html
├── privacy.html
├── error_404.html
├── error_500.html
└── components/
    ├── guest_menu.html
    └── messages.html

menu_app/templates/menu/
├── menu.html
└── menu_item.html
```

### Custom Template Tags

#### dogs_tags.py - `get_years_string`
```python
@register.filter
def get_years_string(age):
    """Returns correct Russian plural form of 'год' (year)."""
    # 1 год, 2-4 года, 5-20 лет, 21 год, 22-24 года, 25 лет...
```

Usage:
```django
{{ dog.age }} {{ dog.age|get_years_string }}
```

#### menu_tags.py - `draw_menu`
```python
@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """Renders hierarchical menu with one DB query."""
    # Uses select_related for efficiency
    # Marks active and expanded items
```

Usage:
```django
{% load menu_tags %}
{% draw_menu "Main Menu" %}
```

---

## Static Files and Media

### Configuration

```python
# Static files (CSS, JS, images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise for production static serving
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# User-uploaded files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### Media Directory Structure

```
media/
├── dogs/          # Dog photos
└── avatars/       # User avatars
```

### Image Validation

- **Allowed types**: JPEG, PNG, WebP
- **Max size**: 5MB
- **Recommended dimensions**: 400x400 pixels

---

## Configuration and Settings

### Settings Package Structure

```python
# project/settings/__init__.py
from .development import *  # Default to development

# project/settings/base.py - Shared settings
# project/settings/development.py - DEBUG=True
# project/settings/production.py - Security settings
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Auto-generated | Django secret key |
| `DEBUG` | `False` | Debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Allowed hosts |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection |
| `EMAIL_BACKEND` | `console` | Email backend |
| `EMAIL_HOST` | Empty | SMTP host |
| `EMAIL_PORT` | `0` | SMTP port |
| `EMAIL_HOST_USER` | Empty | SMTP username |
| `EMAIL_HOST_PASSWORD` | Empty | SMTP password |
| `EMAIL_USE_TLS` | `True` | Use TLS |
| `EMAIL_USE_SSL` | `False` | Use SSL |
| `DEFAULT_FROM_EMAIL` | `DogDating <noreply@dogdating.local>` | From email |

### Production Settings (production.py)

```python
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
```

---

## Authentication and Authorization

### Login Settings

```python
LOGIN_URL = "dogs:login"
LOGIN_REDIRECT_URL = "dogs:dashboard"
LOGOUT_REDIRECT_URL = "dogs:landing_page"
```

### Session Management

- **Remember me**: 2 weeks (1209600 seconds)
- **Default**: Session cookie (expires on browser close)

### Permission Checks

| Action | Permission |
|--------|------------|
| View dog list | Public |
| View dog detail | Public |
| Create dog | Authenticated |
| Edit dog | Owner only |
| Delete dog | Owner only |
| Toggle favorite | Authenticated |
| View matches | Authenticated |
| Create match | Authenticated + owner of source dog |

### Admin Separation

The landing page automatically logs out staff users to prevent admin panel users from accessing the frontend with admin privileges.

---

## Admin Interface

### Registered Models

All models are registered with customized admin classes:

#### DogAdmin
- **List display**: name, breed, age, gender, size, owner, is_active, created_at
- **Filters**: gender, size, breed, is_active, looking_for
- **Search**: name, breed, owner__username
- **Editable**: is_active (inline)

#### UserProfileAdmin
- **List display**: user, location, phone, created_at
- **Filters**: location, created_at
- **Search**: user__username, user__email, location

#### MatchAdmin
- **List display**: dog_from, dog_to, status, created_at
- **Filters**: status, created_at
- **Search**: dog names and owner usernames

#### MessageAdmin
- **List display**: sender, receiver, subject, is_read, created_at
- **Filters**: is_read, created_at
- **Search**: usernames, subject, content

#### FavoriteAdmin
- **List display**: user, dog, created_at
- **Filters**: created_at
- **Search**: user__username, dog__name, dog__breed

---

## Management Commands

### populate_data

Populates the database with demo data:

```bash
python manage.py populate_data
```

Creates:
- Sample users
- Dog profiles with various characteristics
- Matches between dogs
- Favorite relationships

### setup_menus

Creates default navigation menus:

```bash
python manage.py setup_menus
```

Creates:
- Main navigation menu
- Guest menu for unauthenticated users
- Footer menu items

---

## Testing Infrastructure

### Test Configuration

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = project.settings
python_files = tests.py test_*.py *_tests.py
```

### Test Directory Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── factories.py                # Factory Boy factories
├── test_api/                   # API endpoint tests
├── test_db.py                  # Database operation tests
├── test_errors/                # Error handling tests
├── test_forms/                 # Form validation tests
├── test_integration/           # Integration tests
├── test_models/                # Model tests
├── test_permissions/           # Permission tests
├── test_services/              # Service layer tests
├── test_templatetags/          # Template tag tests
├── test_utils/                 # Utility function tests
├── test_views/                 # View tests
└── test_validations_and_services.py
```

### Available Fixtures (conftest.py)

#### User Fixtures
- `user` - Regular authenticated user
- `user2`, `user3` - Additional users
- `staff_user` - Staff user
- `superuser` - Superuser
- `anonymous_user` - Anonymous user

#### Client Fixtures
- `client` - Django test client
- `authenticated_client` - Logged-in client
- `staff_client` - Staff-logged client
- `admin_client` - Superuser-logged client

#### Model Fixtures
- `dog`, `dog2`, `other_dog` - Dog instances
- `inactive_dog` - Inactive dog
- `multiple_dogs` - 15 dogs for pagination
- `pending_match`, `accepted_match`, `declined_match` - Match instances
- `favorite`, `multiple_favorites` - Favorite instances
- `message`, `read_message` - Message instances
- `menu`, `menu_item`, `guest_menu` - Menu instances

#### Data Fixtures
- `valid_dog_data` - Valid dog creation data
- `valid_user_data` - Valid registration data
- `valid_login_data` - Valid login credentials
- `valid_profile_data` - Valid profile update data

#### Factory Functions
- `create_dog(owner, **kwargs)` - Create dog on demand
- `create_match(dog_from, dog_to, status)` - Create match on demand
- `create_favorite(user, dog)` - Create favorite on demand

### Factory Classes (factories.py)

```python
# User factories
UserFactory
StaffUserFactory
SuperUserFactory
UserProfileFactory

# Dog factories
DogFactory
InactiveDogFactory
PuppyFactory
SeniorDogFactory

# Relationship factories
MatchFactory
PendingMatchFactory
AcceptedMatchFactory
DeclinedMatchFactory
FavoriteFactory

# Message factories
MessageFactory
ReadMessageFactory

# Menu factories
MenuFactory
MenuItemFactory
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with pytest
pytest

# Run with coverage
coverage run -m pytest
coverage report
coverage html
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=project.settings.production

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
```

### Docker Compose Services

```yaml
services:
  web:
    build: .
    ports: ["8000:8000"]
    environment:
      - DJANGO_SETTINGS_MODULE=project.settings.production
      - DATABASE_URL=postgres://dogdating_user:dogdating_password@db:5432/dogdating
    volumes:
      - ./media:/app/media
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=dogdating
      - POSTGRES_USER=dogdating_user
      - POSTGRES_PASSWORD=dogdating_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports: ["5432:5432"]

volumes:
  postgres_data:
```

### Deployment Commands

```bash
# Build and start
docker compose up --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Populate demo data
docker compose exec web python manage.py setup_menus
docker compose exec web python manage.py populate_data
```

---

## API Reference

The application primarily uses server-rendered HTML. AJAX endpoints:

### Toggle Favorite

```
POST /dogs/<pk>/favorite/

Response (JSON):
{
    "is_favorite": boolean,
    "message": string
}

Errors:
- 403 Forbidden: Not authenticated or POST method required
- 404 Not Found: Dog not found
```

---

## Utility Functions

### Dog Compatibility (utils.py)

#### calculate_dog_compatibility_score(dog1, dog2)

Calculates compatibility score (0-100) based on:

| Factor | Max Points | Criteria |
|--------|------------|----------|
| Age | 25 | Closer age = higher score |
| Size | 20 | Same/similar size preferred |
| Gender | 15 | Different genders score higher |
| Looking for | 20 | Matching goals preferred |
| Breed | 5 | Same breed bonus |
| Temperament | 15 | Keyword matching |

#### get_compatible_dogs(user_dog, exclude_matches=True)

Returns dogs sorted by compatibility score (minimum 30% threshold).

#### Match Utilities

- `create_match(dog_from, dog_to)` - Create new match
- `accept_match(match)` - Accept match
- `decline_match(match)` - Decline match
- `get_mutual_matches(user)` - Get accepted matches
- `get_pending_matches(user)` - Get pending matches
- `get_match_statistics(user)` - Get match counts by status

### Image Utilities

#### optimize_image(image_field, max_width=800, max_height=600, quality=85)

Resizes and compresses uploaded images.

#### create_default_dog_image()

Creates placeholder dog image (400x300, dog emoji).

#### create_default_avatar()

Creates placeholder avatar (200x200, user emoji).

---

## Security Considerations

### Input Validation

- All forms use Django's built-in validation
- Image uploads validated for size and MIME type
- Age restricted to 0-20 range
- Email uniqueness enforced

### CSRF Protection

- All POST forms include CSRF token
- AJAX requests require CSRF token in headers

### Authentication

- Passwords validated against common patterns
- Session-based authentication
- Staff users separated from regular users on frontend

### Data Protection

- Cascading deletes preserve data integrity
- Owner-only access for edit/delete operations
- Service layer validates all permissions

### Production Security

- HTTPS enforced via SECURE_SSL_REDIRECT
- HSTS enabled with preload
- Secure cookies in production
- Debug mode disabled

---

## Performance Optimizations

### Database

- **Indexes**: Strategic indexes on foreign keys and frequently queried fields
- **select_related**: Used in list views to reduce queries
- **Pagination**: All list views paginated (10-12 items)

### Static Files

- **WhiteNoise**: Serves static files efficiently in production
- **Compressed storage**: CSS/JS compressed automatically

### Queries

- Menu system uses single query with `select_related`
- Dog lists use `select_related("owner")` to avoid N+1

### Caching Opportunities

- Menu rendering could be cached
- Compatibility scores could be pre-calculated
- User statistics could be cached

---

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repository>
cd dog

# Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py setup_menus
python manage.py populate_data

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Production with Docker

```bash
# Build and start
docker compose up --build -d

# Initial setup
docker compose exec web python manage.py migrate
docker compose exec web python manage.py setup_menus
docker compose exec web python manage.py createsuperuser
```

### Access Points

- Main site: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

---

## Appendix: Russian Translations

The interface uses Russian language. Key translations:

| English | Russian |
|---------|---------|
| Dog | Собака |
| Male | Мальчик |
| Female | Девочка |
| Small | Маленькая |
| Medium | Средняя |
| Large | Большая |
| Playmate | Друга для игр |
| Companion | Компаньона |
| Partner | Партнера для жизни |
| Friendship | Дружбы |
| Match | Мэтч |
| Pending | Ожидает |
| Accepted | Принят |
| Declined | Отклонен |
| Favorite | Избранное |
| Dashboard | Личный кабинет |
| Profile | Профиль |

---

*Documentation generated for DogDating v1.0*
