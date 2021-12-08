from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Notebook, Smartphone

# Create your views here
def hello(request):
	return HttpResponse("Hello world")

def test_view(request):
	return render(request,'base.html',{})

class ProductDetailView(DetailView):
	
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
