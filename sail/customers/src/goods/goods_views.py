from django.shortcuts import render
from django.http import HttpResponseRedirect

from ...models import Goods, Provider

from .goods_forms import GoodsForm
from .goods_db import get_goods_list
from ..providers.providers_db import get_providers_choices


def goods_index(request):
    goods_info_list = get_goods_list()
    context = {
        'goods_info_list': goods_info_list,
    }

    print(goods_info_list)
    return render(request, 'goods/goods_index.html', context)


def goods_info(request, goods_id):
    context = {}
    return render(request, 'goods/goods_index.html', context)


def goods_add(request):
    print('goods_add')
    providers_list = get_providers_choices()
    if request.method == "POST":
        fr = GoodsForm(providers_list, request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['name']
            buying_price = fr.cleaned_data['buying_price']
            price = fr.cleaned_data['price']
            comment = fr.cleaned_data['comment']

            goods = Goods(name=name,
                          buying_price=buying_price,
                          price=price,
                          comment=comment)

            try:
                provider = Provider.objects.get(id=fr.cleaned_data['goods_provider'])
                goods.provider = provider
            except (KeyError, Provider.DoesNotExist):
                goods.provider = None

            goods.save()
            return HttpResponseRedirect('/goods/')  # 跳转
    else:
        fr = GoodsForm(providers_list)
        context = {"form": fr,
                   "title": "添加货物"
                   }

    return render(request, 'common/add_template.html', context)


def goods_edit(request, goods_id):
    providers_list = get_providers_choices()

    error_message = ''
    try:
        goods = Goods.objects.get(pk=goods_id)
    except (KeyError, Goods.DoesNotExist):
        error_message = '货物不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = GoodsForm(providers_list, request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['name']
            buying_price = fr.cleaned_data['buying_price']
            price = fr.cleaned_data['price']
            comment = fr.cleaned_data['comment']

            goods.name = name
            goods.buying_price = buying_price
            goods.price = price
            goods.comment = comment
            try:
                provider = Provider.objects.get(id=fr.cleaned_data['goods_provider'])
                goods.provider = provider
            except (KeyError, Provider.DoesNotExist):
                goods.provider = None

            goods.save()
            return HttpResponseRedirect('/goods/')  # 跳转
    elif error_message == "":
        fr = GoodsForm(providers_list, initial={'name': goods.name,
                        'buying_price': goods.buying_price,
                        'price': goods.price,
                        'provider': goods.provider.id,
                        'comment': goods.comment})

        context = {"form": fr,
                   "title": "修改货物",
                   }
    else:
        context = {"error_message": error_message}

    return render(request, 'common/add_template.html', context)


def goods_del(request, goods_id):
    error_message = ''
    try:
        goods = Goods.objects.get(pk=goods_id)
        goods.delete()
    except (KeyError, Goods.DoesNotExist):
        error_message = '货物不存在,请重试!'

    redirect = '/goods'

    return HttpResponseRedirect(redirect)  # 跳转

