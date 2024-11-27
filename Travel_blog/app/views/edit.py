from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from Travel_blog.app.forms.edit import EditDestinationForm
from Travel_blog.app.models import Destination


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
        form = EditDestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination details', destination.pk)
        else:
            context = {
                'destination': destination,
                'form': form,
            }
            return render(request, 'app/destination_edit.html', context)
