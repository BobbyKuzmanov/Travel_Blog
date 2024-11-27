from django.shortcuts import render, redirect
from Travel_blog.app.forms.comment import CommentForm
from Travel_blog.app.forms.create import DestinationForm
from Travel_blog.app.models import Destination, Comment


def destination_details(request, pk):
    destination = Destination.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            'destination': destination,
            'form': DestinationForm if request.user.is_authenticated else None,
            'comment_form': CommentForm if request.user.is_authenticated else None,
            'can_delete': request.user.is_authenticated and destination.user_id == request.user.id,
            'can_comment': request.user.is_authenticated and destination.user_id != request.user.id,
            'can_like': request.user.is_authenticated and destination.user_id != request.user.id,
            'has_likes': request.user.is_authenticated and destination.like_set.filter(user_id=request.user.id).exists(),
        }
        return render(request, 'app/destination_details.html', context)

    # Require login for POST (comments)
    if not request.user.is_authenticated:
        return redirect('signin user')

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(comment=form.cleaned_data['comment'])
        comment.destination = destination
        comment.user = request.user
        comment.save()
        destination.comment_set.add(comment)

        return redirect('destination details', pk)

    context = {
        'destination': destination,
        'form': form
    }
    return render(request, 'app/destination_details.html', context)
