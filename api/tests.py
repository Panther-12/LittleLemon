from django.test import TestCase
from .models import MenuItems, Category

# Create your tests here.
class MenuItemTestCase(TestCase):
    def test_create_menu_item(self):
        category = Category.objects.get(pk=1)
        item = MenuItems.objects.create(name="test1", price=3.40, description="test1", inventory=3, category=category)
        self.assertEqual(item, "test1")