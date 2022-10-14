from django.shortcuts import render

# Main views
def homepage(request):
    return render(request=request, template_name='main/home.html')

