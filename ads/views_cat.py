import json

from django.http import JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ads.models import Category


def root(request):
    return JsonResponse({'status': 'ok'})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        result = []
        for cat in categories:
            result.append({'id': cat.id, 'name': cat.name})
        return JsonResponse(
            result,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    def post(self, request):
        data = json.loads(request.body)
        name_category = Category.objects.create(name=data['name'])
        return JsonResponse({
            'id': name_category.id,
            'name': name_category.name},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cat = Category.objects.create(name=data['name'])
        return JsonResponse(
            {'id': cat.id, 'name': cat.name},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()
        return JsonResponse(
            {'id': self.object.id, 'name': self.object.name},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            'id': cat.id,
            'name': cat.name},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )
