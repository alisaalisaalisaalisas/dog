from django import template
from django.template.loader import get_template
from menu_app.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """
    Template tag для отрисовки меню.
    Использует только 1 запрос к БД благодаря select_related и prefetch_related.
    """
    try:
        # Получаем текущий URL из контекста
        request = context.get("request")
        current_url = request.path if request else ""

        # Один запрос к БД для получения всех пунктов меню
        menu_items = (
            MenuItem.objects.filter(menu__name=menu_name)
            .select_related("parent", "menu")
            .order_by("order", "id")
        )

        if not menu_items.exists():
            template = get_template("menu/menu.html")
            return template.render({"menu_items": []}, request)

        # Строим структуру меню в памяти
        menu_dict = {}
        root_items = []

        # Первый проход: создаем словарь всех элементов
        for item in menu_items:
            menu_dict[item.id] = {
                "item": item,
                "children": [],
                "is_active": False,
                "is_expanded": False,
                "url": item.get_url(),
            }

        # Второй проход: строим иерархию
        for item in menu_items:
            item_data = menu_dict[item.id]
            # Проверяем, является ли пункт активным
            item_data["is_active"] = item_data["url"] == current_url

            if item.parent_id:
                if item.parent_id in menu_dict:
                    menu_dict[item.parent_id]["children"].append(item_data)
            else:
                root_items.append(item_data)

        # Находим активный элемент и его путь
        active_item = None

        def find_active_item(items):
            for item_data in items:
                if item_data["is_active"]:
                    return item_data
                # Рекурсивно ищем в дочерних элементах
                found = find_active_item(item_data["children"])
                if found:
                    return found
            return None

        active_item = find_active_item(root_items)

        # Собираем все элементы в правильном порядке для определения "выше"
        def collect_all_items(items, result=None):
            if result is None:
                result = []
            for item_data in items:
                result.append(item_data)
                collect_all_items(item_data["children"], result)
            return result

        all_items_in_order = collect_all_items(root_items)

        # Определяем, какие пункты должны быть развернуты
        def mark_expanded_items(items, parent_active=False, found_active=False):
            has_any_active = False
            for item_data in items:
                children = item_data["children"]

                # Проверяем, есть ли активные дети
                has_active_child = any(
                    mark_expanded_items([child], item_data["is_active"], found_active)
                    for child in children
                )

                # Определяем позицию текущего элемента
                current_index = (
                    all_items_in_order.index(item_data)
                    if item_data in all_items_in_order
                    else -1
                )
                active_index = (
                    all_items_in_order.index(active_item)
                    if active_item and active_item in all_items_in_order
                    else -1
                )

                # Разворачиваем пункт если:
                # 1. Все элементы выше активного (индекс меньше активного)
                # 2. Он сам активный
                # 3. Первый уровень под активным (parent_active)
                should_expand = (
                    (
                        current_index >= 0
                        and active_index >= 0
                        and current_index < active_index
                    )  # Все выше активного
                    or item_data["is_active"]  # Сам активный
                    or has_active_child  # Есть активные потомки
                    or parent_active  # Первый уровень под активным
                )

                if should_expand:
                    item_data["is_expanded"] = True

                # Отмечаем, что этот пункт или его потомок активный
                if item_data["is_active"] or has_active_child:
                    has_any_active = True

            return has_any_active

        # Отмечаем развернутые элементы
        for item in root_items:
            mark_expanded_items([item])

        # Рендерим шаблон вручную
        template = get_template("menu/menu.html")
        return template.render({"menu_items": root_items}, request)

    except Exception:
        template = get_template("menu/menu.html")
        return template.render({"menu_items": []}, request)
