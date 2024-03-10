# Home
from home.models import Carousel, Category


def view_cart(request):
    cart = request.session.get('cart', {})
    return {
        'cart':cart,
    }


def view_carousel(request):
    carousel = Carousel.objects.filter(is_hide=False)
    return {
        'carousel':carousel,
    }


def view_category(request):
    categories = Category.objects.all()
    return {
        'categories':categories,
    }