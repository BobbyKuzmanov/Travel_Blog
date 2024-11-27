from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Travel_blog.app.forms.delete import DeleteDestinationForm
from Travel_blog.app.models import Destination
import os


@login_required
def destination_delete(request, pk):
    # Get the destination or return 404 if not found
    destination = get_object_or_404(Destination, pk=pk)
    
    # Check if user is authorized to delete this destination
    if destination.user != request.user:
        messages.error(request, "You don't have permission to delete this story.")
        return redirect('destination details', pk=pk)
    
    if request.method == 'GET':
        context = {
            'destination': destination,
            'form': DeleteDestinationForm(instance=destination),
        }
        return render(request, 'app/destination_delete.html', context)
    else:
        # Store the image path before deletion
        image_path = destination.image.path if destination.image else None
        
        try:
            # Delete the destination (this will cascade delete related likes and comments)
            destination.delete()
            
            # Delete the image file if it exists
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            
            messages.success(request, 'Story deleted successfully.')
            return redirect('destination list')
            
        except Exception as e:
            messages.error(request, f'Error deleting story: {str(e)}')
            return redirect('destination details', pk=pk)
