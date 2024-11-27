from Travel_blog.app.forms.create import DestinationForm
from Travel_blog.app.forms.mixin import DisabledFormMixin


class DeleteDestinationForm(DestinationForm, DisabledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DisabledFormMixin.__init__(self)
