from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from django.http import HttpRequest

from django import forms

from django.views import View
from .utils import ImageLocalStorage

from .models import Product

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: JVM FakeName",
            }
        )

        return context


class ContactPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "title": "Contact us - Online Store",
                "subtitle": "Contact us",
                "description": "This is a contact page ...",
                "author": "Developed by: JVM FakeName",
            }
        )

        return context




class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}

        viewData["title"] = "Products - Online Store"

        viewData["subtitle"] = "List of products"

        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]
        except IndexError:
            return redirect("/")

        viewData["title"] = product["name"] + " - Online Store"

        viewData["subtitle"] = product["name"] + " - Product information"

        viewData["product"] = product

        viewData["expensive"] = product["price"] > 100

        return render(request, self.template_name, viewData)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError(
                "El valor debería ser un `float` positivo :(", "invalid"
            )
        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()

        viewData = {}

        viewData["title"] = "Create product"

        viewData["form"] = form

        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "products/confim.html")

        else:
            viewData = {}

            viewData["title"] = "Create product"

            viewData["form"] = form

            return render(request, self.template_name, viewData)


class SuccessView(View):
    template_name = "products/confirm.html"

    def post(self, request):
        return render(request, self.template_name, {})


class CartView(View):
    template_name = "cart/index.html"

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {"name": "Tv samsung", "price": "1000"}
        products[11] = {"name": "Iphone", "price": "2000"}

        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get("cart_product_data", {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view

        view_data = {
            "title": "Cart - Online Store",
            "subtitle": "Shopping Cart",
            "products": products,
            "cart_products": cart_products,
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Get cart products from session and add the new product

        cart_product_data = request.session.get("cart_product_data", {})
        cart_product_data[product_id] = product_id
        request.session["cart_product_data"] = cart_product_data
        return redirect("cart_index")


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if "cart_product_data" in request.session:
            del request.session["cart_product_data"]
        return redirect("cart_index")


def ImageViewFactory(image_storage: ImageLocalStorage):
    class ImageView(View):
        template_name = "images/index.html"

        def get(self, request):
            image_url = request.session.get("image_url", "")

            return render(request, self.template_name, {"image_url": image_url})

        def post(self, request: HttpRequest):
            image_url = image_storage.store(request)

            request.session["image_url"] = image_url

            return redirect("image_index")

    return ImageView
