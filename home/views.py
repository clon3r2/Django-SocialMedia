from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass