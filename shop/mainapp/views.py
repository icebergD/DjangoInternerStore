from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, View

from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin

# Create your views here
def hello(request):
	return HttpResponse("Hello world")

class BaseView(View):
	def get(self, request, *args, **kwargs):
		customer = Customer.objects.get(user=request.user)
		cart = Cart.objects.get(owner=customer)
		categories = Category.objects.get_category_for_dropdown_menu()
		products = LatestProducts.objects.get_products_for_main_page(
			'notebook','smartphone', with_respect_to='smartphone'
		)
		context = {
			'categories': categories,
			'products': products,
			'cart': cart
		}
		return render(request,'base.html',context )


class ProductDetailView(CategoryDetailMixin, DetailView):
	
	CT_MODEL_MODEL_CLASS = {
		'notebook': Notebook,
		'smartphone': Smartphone
	}

	def dispatch(self, request, *args, **kwargs):
		self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
		self.queryset = self.model._base_manager.all()
		return super().dispatch(request, *args, **kwargs)

	context_object_name = 'product'
	template_name = 'product_detail.html'
	slug_url_kwarg = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['ct_model'] = self.model._meta.model_name
		return context


class CategoryDetailView(CategoryDetailMixin, DetailView):

	model = Category
	queryset = Category.objects.all()
	context_object_name = 'category'
	template_name = 'category_detail.html'
	slug_url_kwarg = 'slug'


class AddToCartView(View):

	def get(self, request, *args, **kwargs):
		ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
		customer = Customer.objects.get(user=request.user)
		cart = Cart.objects.get(owner=customer, in_order=False)
		content_type = ContentType.objects.get(model=ct_model)
		product = content_type.model_class().objects.get(slug=product_slug)
		cart_product, created = CartProduct.objects.get_or_create(
			user=cart.owner, cart=cart, content_type=content_type, object_id=product.id, final_price=product.price
		)
		cart.products.add(cart_product)
		return HttpResponseRedirect('/cart/')

class CartView(View):

	def get(self, request, *args, **kwargs):
		
		customer = Customer.objects.get(user=request.user)
		cart = Cart.objects.get(owner=customer)
		categories = Category.objects.get_category_for_dropdown_menu()
		context = {
			'cart': cart,
			'categories': categories
		}
		return render(request,'cart.html',context)