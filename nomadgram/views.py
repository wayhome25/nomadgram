import os

from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import View


class ReactAppView(View):

    def get(self, request):
        try:
            with open(os.path.join(str(settings.ROOT_DIR), 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())
        except:
            return HttpResponse(
                """index.html not found! build your React app !!""",
                status=501
            )
