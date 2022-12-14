import json

from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from ads.models import Ad, Category
from avito import settings
from users.models import User


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('-price')
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_object = paginator.get_page(page)
        result = []
        for ad in page_object:
            result.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author.username,
                'category': ad.category.name if ad.category else 'Без категории',
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'image': ad.image.url if ad.image else 'Без картинки',
            })
        return JsonResponse({
            'items': result,
            'page': page_object.number,
            'total': page_object.paginator.count},
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, id=data['author_id'])
        category = get_object_or_404(Category, id=data['category_id'])

        new_ad = Ad.objects.create(
            name=data['name'],
            author=author,
            category=category,
            price=data['price'],
            description=data['description'],
            is_published=data['is_published'] if 'is_published' in data else False,
            image=data['image'] if 'image' in data else ''
        )

        return JsonResponse({
            'id': new_ad.id,
            'name': new_ad.name,
            'author': new_ad.author.username,
            'category': new_ad.category.name,
            'price': new_ad.price,
            'description': new_ad.description,
            'is_published': new_ad.is_published,
            'image': new_ad.image.url if 'image' in data else 'Без картинки'
        },
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryUpdateView(UpdateView):
#     model = Category
#     fields = ['name']
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         data = json.loads(request.body)
#         self.object.name = data['name']
#         self.object.save()
#         return JsonResponse(
#             {'id': self.object.id, 'name': self.object.name},
#             safe=False,
#             json_dumps_params={'ensure_ascii': False}
#         )
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class CategoryDeleteView(DeleteView):
#     model = Category
#     success_url = '/'
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({'status': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.username,
            'category': self.object.category.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url
        },
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'category': ad.category.name if ad.category else 'Без категории',
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else 'Без картинки'
        },
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )
