from django.shortcuts import render
from django.http import HttpResponseRedirect

from ...models import Cost

from .costs_forms import CostForm
from .costs_db import get_costs_list


def cost_index(request):
    cost_info_list = get_costs_list()

    print(cost_info_list)
    context = {
        'costs_info_list': cost_info_list,
    }
    return render(request, 'costs/costs_index.html', context)


def cost_add(request):
    print('cost_add')
    if request.method == "POST":
        fr = CostForm(request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['name']
            price = fr.cleaned_data['price']
            cost = Cost(name=name, price=price)
            cost.save()
            return HttpResponseRedirect('/costs/')  # 跳转
    else:
        fr = CostForm()
        context = {"form": fr,
                   "title": "添加成本信息"
                   }

    return render(request, 'common/add_template.html', context)


def cost_edit(request, cost_id):
    error_message = ''
    try:
        cost = Cost.objects.get(pk=cost_id)
    except (KeyError, Cost.DoesNotExist):
        error_message = '成本信息不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = CostForm(request.POST)
        if fr.is_valid():
            cost.name = fr.cleaned_data['name']
            cost.price = fr.cleaned_data['price']
            cost.save()
            return HttpResponseRedirect('/costs/')  # 跳转
    elif error_message == "":
        fr = CostForm({'name': cost.name,
                       'price': cost.price})

        context = {"form": fr,
                   "title": "修改成本信息"
                   }
    else:
        context = {"error_message": error_message}

    return render(request, 'common/add_template.html', context)


def cost_del(request, cost_id):
    error_message = ''
    try:
        cost = Cost.objects.get(pk=cost_id)
        cost.delete()
    except (KeyError, Cost.DoesNotExist):
        error_message = '成本信息不存在,请重试!'

    redirect = '/costs'

    return HttpResponseRedirect(redirect)  # 跳转

