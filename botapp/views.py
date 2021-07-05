from django.shortcuts import render, HttpResponseRedirect
import requests
from django.views import View
from django.urls import reverse
from django.http import JsonResponse


class DiscordLoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.session.get('access_token'):
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, self.template_name, locals())

    def post(self, request):
        response = {}
        try:
            api_url = 'https://discord.com/api/v8'
            client_id = request.POST.get('client_id')
            client_secret = request.POST.get('client_secret')
            data = {
                'grant_type': 'client_credentials',
                'scope': 'identify',
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            result = requests.post('%s/oauth2/token' % api_url, data, headers, auth=(client_id, client_secret))
            
            if result.status_code == 200:
                res = result.json()
                request.session['access_token'] = res.get('access_token')
                response["status"] = True
                response["message"] = "Logged in"
                response["data"] = []
            else:
                response["status"] = False
                response["message"] = "Unauthenticated"
                response["data"] = []
            return JsonResponse(response, content_type="application/json")
        except Exception as e:
            print(str(e), "exception")
            return HttpResponseRedirect(reverse('login'))


class DashboardView(View):
    template_name = "dashboard/dashboard.html"

    def get(self, request):
        if request.session.get('access_token'):

            return render(request, self.template_name, locals())
        else:
            return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    def post(self, request):
        if request.session.get('access_token'):
            request.session.pop('access_token')
        return HttpResponseRedirect(reverse('login'))
           



