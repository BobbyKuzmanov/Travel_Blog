from Travel_blog.app.forms.create import DestinationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from Travel_blog.app.models import Destination


# def destination_create(request):
#     if request.method == 'GET':
#         context = {
#             'form': DestinationForm(),
#         }
#         return render(request, 'app/destination_create.html', context)
#     else:
#         form = DestinationForm(request.POST, request.FILES)
#         form.instance.user = request.user
#         if form.is_valid():
#             form.save()
#             return redirect('destination list')
#         context = {
#             'form': form,
#         }
#         return render(request, 'app/destination_create.html', context)


class CreateDestinationView(LoginRequiredMixin, CreateView):
    template_name = 'app/destination_create.html'
    model = Destination
    form_class = DestinationForm
    success_url = reverse_lazy('destination list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
