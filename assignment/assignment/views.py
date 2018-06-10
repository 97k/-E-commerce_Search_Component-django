from django.views.generic import TemplateView

class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePage, self).get_context_data(*args, **kwargs)
        context['title'] = "Hi!, I am Aditya Kaushik"
        context['content'] = 'This is a small module as an assignment for the internship <br><br> Go to /products for all the products'
        return context
