from Travel_blog.app.forms.create import DestinationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from Travel_blog.app.models import Destination


class CreateDestinationView(LoginRequiredMixin, CreateView):
    template_name = 'app/destination_create.html'
    model = Destination
    form_class = DestinationForm
    success_url = reverse_lazy('destination list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
