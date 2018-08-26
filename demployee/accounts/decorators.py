from django.urls import reverse
from django.http import HttpResponseRedirect

def login_check(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            #return to home page url
            return HttpResponseRedirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func