from django.views.generic import ListView
from Travel_blog.app.models import Destination, Category


class DestinationListView(ListView):
    model = Destination
    template_name = 'app/destination_list.html'
    context_object_name = 'destinations'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Add can_delete attribute to each destination
        for dest in queryset:
            dest.can_delete = dest.user_id == self.request.user.id

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        return context
