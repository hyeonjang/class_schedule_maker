from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import User 

class ManageView(TemplateView):
    template_name = 'ManageView.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(ManageView, self).get_context_data(**kwargs)
        users = User.objects.all()
        context['Users'] = users
        # print(context['TimeTables'])
        return context