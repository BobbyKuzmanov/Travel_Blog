from django.shortcuts import render
from Travel_blog.app.models import Destination, Category


def destination_list(request):
    category_id = request.GET.get('category')
    destinations = Destination.objects.all()
    
    if category_id:
        destinations = destinations.filter(category_id=category_id)
    
    categories = Category.objects.all().order_by('name')
    
    for dest in destinations:
        dest.can_delete = dest.user_id == request.user.id
    
    context = {
        'destinations': destinations,
        'categories': categories,
    }
    return render(request, 'app/destination_list.html', context)
