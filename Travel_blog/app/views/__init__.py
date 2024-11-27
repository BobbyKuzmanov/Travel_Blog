from Travel_blog.app.views.create import CreateDestinationView
from Travel_blog.app.views.edit import destination_edit
from Travel_blog.app.views.delete import destination_delete
from Travel_blog.app.views.details import destination_details
from Travel_blog.app.views.list import destination_list
from Travel_blog.app.views.likes import destination_likes

__all__ = [
    'CreateDestinationView',
    'destination_edit',
    'destination_delete',
    'destination_details',
    'destination_list',
    'destination_likes',
]