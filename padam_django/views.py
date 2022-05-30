from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/bs_planner/')
    return response
