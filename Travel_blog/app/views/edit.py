from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from Travel_blog.app.forms.edit import EditDestinationForm
from Travel_blog.app.models import Destination
import os

@login_required
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    
    # SuperAdmin can edit any destination
    if request.user.groups.filter(name='SuperAdmin').exists():
        pass  # Allow full access
    # Staff can edit but not delete
    elif request.user.groups.filter(name='Staff').exists():
        pass  # Allow edit access
    # Regular users can only edit their own content
    elif destination.user != request.user:
        messages.error(request, "You don't have permission to edit this story.")
        return redirect('destination details', pk=pk)
        
    if request.method == 'GET':
        context = {
            'destination': destination,
            'form': EditDestinationForm(instance=destination),
        }
        return render(request, 'app/destination_edit.html', context)
    else:
        old_image_path = destination.image.path if destination.image else None
        form = EditDestinationForm(request.POST, request.FILES, instance=destination)
        
        if form.is_valid():
            # Check if a new image was uploaded
            if 'image' in request.FILES:
                # Delete old image if it exists
                if old_image_path and os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception as e:
                        messages.warning(request, f"Could not remove old image: {str(e)}")
            
            form.save()
            messages.success(request, "Story updated successfully!")
            return redirect('destination details', destination.pk)
        else:
            context = {
                'destination': destination,
                'form': form,
            }
            return render(request, 'app/destination_edit.html', context)
