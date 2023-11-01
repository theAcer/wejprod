from django.shortcuts import render

app_name = 'chat'

def user_list(request):
    return render(request, 'user_list.html')