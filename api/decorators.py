from django.contrib.auth.decorators import user_passes_test

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

manager_required = user_passes_test(is_manager)


def is_delivery_crew(user):
    return user.groups.filter(name="Delivery crew").exists()

delivery_crew_required = user_passes_test(is_delivery_crew)