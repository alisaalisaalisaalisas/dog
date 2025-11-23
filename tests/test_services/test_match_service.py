"""
Extended tests for services/match_service.py

Tests for match service functions with comprehensive coverage.
"""

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from dogs.models import Dog, Match
from services.match_service import (
    accept_match_for_user,
    create_match_for_user,
    decline_match_for_user,
)


@pytest.mark.unit
@pytest.mark.services
class TestCreateMatchForUser:
    """Test suite for create_match_for_user function."""

    @pytest.fixture
    def user1(self, db):
        return User.objects.create_user(username="user1", password="pass123")

    @pytest.fixture
    def user2(self, db):
        return User.objects.create_user(username="user2", password="pass123")

    @pytest.fixture
    def dog1(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="Dog1",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    @pytest.fixture
    def dog2(self, user2):
        return Dog.objects.create(
            owner=user2,
            name="Dog2",
            age=3,
            breed="Breed",
            gender="F",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    def test_create_match_success(self, user1, dog1, dog2):
        """Should create a match successfully."""
        match = create_match_for_user(user1, dog1.id, dog2.id)
        assert match is not None
        assert match.dog_from == dog1
        assert match.dog_to == dog2

    def test_create_match_wrong_owner_raises_permission_denied(self, user2, dog1, dog2):
        """Should raise PermissionDenied if user doesn't own source dog."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user2, dog1.id, dog2.id)

    def test_create_match_same_dog_raises_permission_denied(self, user1, dog1):
        """Should raise PermissionDenied for self-match."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user1, dog1.id, dog1.id)

    def test_create_match_both_owned_by_user_raises_permission_denied(self, user1):
        """Should raise PermissionDenied if both dogs owned by same user."""
        dog1 = Dog.objects.create(
            owner=user1,
            name="Dog1",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )
        dog2 = Dog.objects.create(
            owner=user1,
            name="Dog2",
            age=3,
            breed="Breed",
            gender="F",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

        with pytest.raises(PermissionDenied):
            create_match_for_user(user1, dog1.id, dog2.id)

    def test_create_match_inactive_source_dog_raises(self, user1, user2, dog2):
        """Should raise PermissionDenied for inactive source dog."""
        inactive_dog = Dog.objects.create(
            owner=user1,
            name="Inactive",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=False,
        )

        with pytest.raises(PermissionDenied):
            create_match_for_user(user1, inactive_dog.id, dog2.id)

    def test_create_match_inactive_target_dog_raises(self, user1, user2, dog1):
        """Should raise DoesNotExist for inactive target dog."""
        inactive_dog = Dog.objects.create(
            owner=user2,
            name="Inactive",
            age=3,
            breed="Breed",
            gender="F",
            size="M",
            temperament="friendly",
            looking_for="playmate",
            is_active=False,
        )

        with pytest.raises(Dog.DoesNotExist):
            create_match_for_user(user1, dog1.id, inactive_dog.id)

    def test_create_match_nonexistent_source_dog(self, user1, dog2):
        """Should raise PermissionDenied for non-existent source dog."""
        with pytest.raises(PermissionDenied):
            create_match_for_user(user1, 99999, dog2.id)

    def test_create_match_nonexistent_target_dog(self, user1, dog1):
        """Should raise DoesNotExist for non-existent target dog."""
        with pytest.raises(Dog.DoesNotExist):
            create_match_for_user(user1, dog1.id, 99999)


@pytest.mark.unit
@pytest.mark.services
class TestAcceptMatchForUser:
    """Test suite for accept_match_for_user function."""

    @pytest.fixture
    def user1(self, db):
        return User.objects.create_user(username="user1", password="pass123")

    @pytest.fixture
    def user2(self, db):
        return User.objects.create_user(username="user2", password="pass123")

    @pytest.fixture
    def user3(self, db):
        return User.objects.create_user(username="user3", password="pass123")

    @pytest.fixture
    def dog1(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="Dog1",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    @pytest.fixture
    def dog2(self, user2):
        return Dog.objects.create(
            owner=user2,
            name="Dog2",
            age=3,
            breed="Breed",
            gender="F",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    def test_accept_match_as_source_owner(self, user1, dog1, dog2):
        """Should allow source dog owner to accept match."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        result = accept_match_for_user(user1, match)
        assert result is True
        match.refresh_from_db()
        assert match.status == "accepted"

    def test_accept_match_as_target_owner(self, user2, dog1, dog2):
        """Should allow target dog owner to accept match."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        result = accept_match_for_user(user2, match)
        assert result is True
        match.refresh_from_db()
        assert match.status == "accepted"

    def test_accept_match_as_non_owner_raises(self, user3, dog1, dog2):
        """Should raise PermissionDenied if user owns neither dog."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        with pytest.raises(PermissionDenied):
            accept_match_for_user(user3, match)


@pytest.mark.unit
@pytest.mark.services  
class TestDeclineMatchForUser:
    """Test suite for decline_match_for_user function."""

    @pytest.fixture
    def user1(self, db):
        return User.objects.create_user(username="user1", password="pass123")

    @pytest.fixture
    def user2(self, db):
        return User.objects.create_user(username="user2", password="pass123")

    @pytest.fixture
    def user3(self, db):
        return User.objects.create_user(username="user3", password="pass123")

    @pytest.fixture
    def dog1(self, user1):
        return Dog.objects.create(
            owner=user1,
            name="Dog1",
            age=3,
            breed="Breed",
            gender="M",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    @pytest.fixture
    def dog2(self, user2):
        return Dog.objects.create(
            owner=user2,
            name="Dog2",
            age=3,
            breed="Breed",
            gender="F",
            size="M",
            temperament="friendly",
            looking_for="playmate",
        )

    def test_decline_match_as_source_owner(self, user1, dog1, dog2):
        """Should allow source dog owner to decline match."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        result = decline_match_for_user(user1, match)
        assert result is True
        match.refresh_from_db()
        assert match.status == "declined"

    def test_decline_match_as_target_owner(self, user2, dog1, dog2):
        """Should allow target dog owner to decline match."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        result = decline_match_for_user(user2, match)
        assert result is True
        match.refresh_from_db()
        assert match.status == "declined"

    def test_decline_match_as_non_owner_raises(self, user3, dog1, dog2):
        """Should raise PermissionDenied if user owns neither dog."""
        match = Match.objects.create(dog_from=dog1, dog_to=dog2, status="pending")
        with pytest.raises(PermissionDenied):
            decline_match_for_user(user3, match)
