"""Home Page View."""


from django.shortcuts import render


def home_view(request):
    """View for homepage."""
    context = {'greeting': 'Hello World'}
    return render(
        request,
        'imagersite/home.html',
        context=context
    )

