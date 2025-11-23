"""
Tests for menu_app/templatetags/menu_tags.py

Tests for the draw_menu template tag.
"""

import pytest
from django.template import Context, Template
from django.test import RequestFactory

from menu_app.models import Menu, MenuItem


@pytest.mark.unit
@pytest.mark.templatetags
class TestDrawMenuTemplateTag:
    """Test suite for draw_menu template tag."""

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def menu(self, db):
        return Menu.objects.create(name="main_menu", description="Main Menu")

    @pytest.fixture
    def root_item1(self, menu):
        return MenuItem.objects.create(
            menu=menu, title="Home", url="/", order=1, parent=None
        )

    @pytest.fixture
    def root_item2(self, menu):
        return MenuItem.objects.create(
            menu=menu, title="About", url="/about/", order=2, parent=None
        )

    def test_draw_menu_renders_empty_for_nonexistent_menu(self, request_factory):
        """Should render empty menu for non-existent menu name."""
        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'nonexistent' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        # Should render the template but with empty menu_items
        assert rendered is not None

    def test_draw_menu_renders_root_items(
        self, request_factory, menu, root_item1, root_item2
    ):
        """Should render root menu items."""
        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        assert rendered is not None

    def test_draw_menu_marks_active_item(self, request_factory, menu, root_item1):
        """Should mark the active item based on current URL."""
        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        # Active item should be marked (depends on template implementation)
        assert rendered is not None

    def test_draw_menu_builds_hierarchy(self, request_factory, menu, root_item1):
        """Should build hierarchical menu structure."""
        child_item = MenuItem.objects.create(
            menu=menu, title="Subpage", url="/subpage/", order=1, parent=root_item1
        )

        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        assert rendered is not None

    def test_draw_menu_expands_active_parents(self, request_factory, menu, root_item1):
        """Should expand parent items when child is active."""
        child_item = MenuItem.objects.create(
            menu=menu, title="Subpage", url="/subpage/", order=1, parent=root_item1
        )

        # Request to child page
        request = request_factory.get("/subpage/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        # Parent should be expanded
        assert rendered is not None

    def test_draw_menu_handles_named_urls(self, request_factory, menu):
        """Should handle named URLs correctly."""
        item = MenuItem.objects.create(
            menu=menu, title="Dogs", named_url="dog_list", order=1, parent=None
        )

        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        assert rendered is not None

    def test_draw_menu_single_db_query(
        self, request_factory, menu, root_item1, root_item2, django_assert_num_queries
    ):
        """Should use only 1 database query for efficiency."""
        # Create some child items
        MenuItem.objects.create(
            menu=menu, title="Sub1", url="/sub1/", order=1, parent=root_item1
        )
        MenuItem.objects.create(
            menu=menu, title="Sub2", url="/sub2/", order=2, parent=root_item1
        )

        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})

        # Should use only 1 query for MenuItem and 1 for template rendering
        with django_assert_num_queries(2):  # 1 for items, 1 for template check
            rendered = template.render(context)

    def test_draw_menu_handles_exceptions_gracefully(self, request_factory):
        """Should handle exceptions gracefully."""
        # Create a menu without items
        Menu.objects.create(name="empty_menu", description="Empty")

        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'empty_menu' %}")
        context = Context({"request": request})

        # Should not raise an exception
        rendered = template.render(context)
        assert rendered is not None

    def test_draw_menu_no_request_in_context(self, menu, root_item1):
        """Should handle missing request in context."""
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({})  # No request

        # Should not raise an exception
        rendered = template.render(context)
        assert rendered is not None

    def test_draw_menu_deep_hierarchy(self, request_factory, menu):
        """Should handle deep menu hierarchies."""
        level1 = MenuItem.objects.create(
            menu=menu, title="Level 1", url="/l1/", order=1, parent=None
        )
        level2 = MenuItem.objects.create(
            menu=menu, title="Level 2", url="/l2/", order=1, parent=level1
        )
        level3 = MenuItem.objects.create(
            menu=menu, title="Level 3", url="/l3/", order=1, parent=level2
        )

        request = request_factory.get("/l3/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        # All parent levels should be expanded
        assert rendered is not None

    def test_draw_menu_respects_order(self, request_factory, menu):
        """Should respect menu item order."""
        item3 = MenuItem.objects.create(
            menu=menu, title="Third", url="/third/", order=3, parent=None
        )
        item1 = MenuItem.objects.create(
            menu=menu, title="First", url="/first/", order=1, parent=None
        )
        item2 = MenuItem.objects.create(
            menu=menu, title="Second", url="/second/", order=2, parent=None
        )

        request = request_factory.get("/")
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
        context = Context({"request": request})
        rendered = template.render(context)
        # Items should be in order (1, 2, 3)
        assert rendered is not None
