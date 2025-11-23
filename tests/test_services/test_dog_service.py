"""
Extended tests for services/dog_service.py

Tests for dog service functions with comprehensive coverage.
"""

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from dogs.models import Dog
from services.dog_service import get_dog_for_owner, get_public_dog


@pytest.mark.unit
@pytest.mark.services
class TestGetDogForOwner:
    """Test suite for get_dog_for_owner function."""

    @pytest.fixture
    def user1(self, db):
        return User.objects.create_user(username="owner", password="pass123")

    @pytest.fixture
    def user2(self, db):
        return User.objects.create_user(username="other", password="pass123")

    @pytest.fixture
    def active_dog(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="ActiveDog",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=True,
        )

    @pytest.fixture
    def inactive_dog(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="InactiveDog",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=False,
        )

    def test_get_dog_for_owner_success(self, user1, active_dog):
        """Should return dog for correct owner."""
        dog = get_dog_for_owner(user1, active_dog.id)
        assert dog == active_dog

    def test_get_dog_for_owner_wrong_owner_raises(self, user2, active_dog):
        """Should raise PermissionDenied for wrong owner."""
        with pytest.raises(PermissionDenied):
            get_dog_for_owner(user2, active_dog.id)

    def test_get_dog_for_owner_inactive_with_active_only_raises(
        self, user1, inactive_dog
    ):
        """Should raise PermissionDenied for inactive dog when active_only=True."""
        with pytest.raises(PermissionDenied):
            get_dog_for_owner(user1, inactive_dog.id, active_only=True)

    def test_get_dog_for_owner_inactive_with_active_only_false(
        self, user1, inactive_dog
    ):
        """Should return inactive dog when active_only=False."""
        dog = get_dog_for_owner(user1, inactive_dog.id, active_only=False)
        assert dog == inactive_dog

    def test_get_dog_for_owner_nonexistent_raises(self, user1):
        """Should raise PermissionDenied for non-existent dog."""
        with pytest.raises(PermissionDenied):
            get_dog_for_owner(user1, 99999)


@pytest.mark.unit
@pytest.mark.services
class TestGetPublicDog:
    """Test suite for get_public_dog function."""

    @pytest.fixture
    def user1(self, db):
        return User.objects.create_user(username="owner", password="pass123")

    @pytest.fixture
    def active_dog(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="ActiveDog",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=True,
        )

    @pytest.fixture
    def inactive_dog(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="InactiveDog",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=False,
        )

    def test_get_public_dog_success(self, active_dog):
        """Should return active dog."""
        dog = get_public_dog(active_dog.id)
        assert dog == active_dog

    def test_get_public_dog_inactive_with_active_only_raises(self, inactive_dog):
        """Should raise DoesNotExist for inactive dog when active_only=True."""
        with pytest.raises(Dog.DoesNotExist):
            get_public_dog(inactive_dog.id, active_only=True)

    def test_get_public_dog_inactive_with_active_only_false(self, inactive_dog):
        """Should return inactive dog when active_only=False."""
        dog = get_public_dog(inactive_dog.id, active_only=False)
        assert dog == inactive_dog

    def test_get_public_dog_nonexistent_raises(self):
        """Should raise DoesNotExist for non-existent dog."""
        with pytest.raises(Dog.DoesNotExist):
            get_public_dog(99999)
