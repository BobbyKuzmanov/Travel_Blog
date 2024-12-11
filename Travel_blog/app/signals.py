from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.apps import apps
import os


@receiver(pre_delete, sender='auth.User')
def cleanup_user_destinations(sender, instance, **kwargs):
    """
    Signal to clean up destination images when a user is deleted
    """
    # Get the Destination model
    Destination = apps.get_model('app', 'Destination')

    # Get all destinations for this user
    destinations = Destination.objects.filter(user=instance)

    # Delete all destination images
    for destination in destinations:
        if destination.image:
            if os.path.isfile(destination.image.path):
                try:
                    os.remove(destination.image.path)
                except Exception as e:
                    print(f"Error deleting destination image: {e}")
