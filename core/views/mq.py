from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.tasks import statistic, send_message


class TestStatisticView(LoginRequiredMixin, View):
    template = None
    login_url = 'login'

    def get(self, request):
        statistic.apply_async(queue='worker')
        return HttpResponse('worker queue run')


class TestSenderView(LoginRequiredMixin, View):
    template = None
    login_url = 'login'

    def get(self, request):
        send_message.apply_async(args=['some_message',], queue='sender')
        return HttpResponse('sender queue run')
