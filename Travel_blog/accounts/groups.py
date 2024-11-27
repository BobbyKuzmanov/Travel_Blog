from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from Travel_blog.app.models import Destination, Comment

def create_admin_groups():
    """Create or update admin groups with appropriate permissions"""
    
    # Create SuperAdmin group
    superadmin_group, _ = Group.objects.get_or_create(name='SuperAdmin')
    
    # Create Staff group
    staff_group, _ = Group.objects.get_or_create(name='Staff')
    
    # Get content types
    destination_ct = ContentType.objects.get_for_model(Destination)
    comment_ct = ContentType.objects.get_for_model(Comment)
    
    # Define permissions for SuperAdmin (full CRUD)
    superadmin_permissions = Permission.objects.filter(
        content_type__in=[destination_ct, comment_ct]
    )
    
    # Define permissions for Staff (limited CRUD)
    staff_permissions = Permission.objects.filter(
        content_type__in=[destination_ct, comment_ct],
        codename__in=['view_destination', 'change_destination', 
                     'view_comment', 'change_comment', 'delete_comment']
    )
    
    # Assign permissions to groups
    with transaction.atomic():
        superadmin_group.permissions.set(superadmin_permissions)
        staff_group.permissions.set(staff_permissions)
        
    return superadmin_group, staff_group
