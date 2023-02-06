from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Show home/landing page"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect to stories page
            return HttpResponse("This will be stories page (redirected)")

        return render(request, "blog/landing_page.html")
