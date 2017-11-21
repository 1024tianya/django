from django.shortcuts import render
from django.http import HttpResponseRedirect

from ...models import Provider

from .providers_forms import ProviderForm
from .providers_db import get_providers_list


def provider_index(request):
    providers_list = get_providers_list()
    context = {
        'providers_info_list': providers_list,
    }
    return render(request, 'providers/providers_index.html', context)


def provider_info(request, provider_id):
    context = {
        'customer_info_list': '',
    }
    return render(request, 'customers/customers_index.html', context)


def provider_add(request):
    print('provider_add')
    if request.method == "POST":
        fr = ProviderForm(request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['name']
            address = fr.cleaned_data['address']
            comment = fr.cleaned_data['comment']
            provider = Provider(name=name,
                                address=address,
                                comment=comment)
            provider.save()
            return HttpResponseRedirect('/providers/')  # 跳转
    else:
        fr = ProviderForm()
        context = {"form": fr,
                   "title": "添加供应商"
                   }

    return render(request, 'common/add_template.html', context)


def provider_edit(request, provider_id):
    error_message = ''
    try:
        provider = Provider.objects.get(pk=provider_id)
    except (KeyError, Provider.DoesNotExist):
        error_message = '供应商不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = ProviderForm(request.POST)
        if fr.is_valid():
            provider.name = fr.cleaned_data['name']
            provider.address = fr.cleaned_data['address']
            provider.comment = fr.cleaned_data['comment']
            provider.save()
            return HttpResponseRedirect('/providers/')  # 跳转
    elif error_message == "":
        fr = ProviderForm({'name': provider.name,
                           'address': provider.address,
                           'comment': provider.comment})

        context = {"form": fr,
                   "title": "修改供应商信息",
                   "customer_info": provider,
                   }
    else:
        context = {"error_message": error_message}

    return render(request, 'common/add_template.html', context)


def provider_del(request, provider_id):
    error_message = ''
    try:
        provider = Provider.objects.get(pk=provider_id)
        provider.delete()
    except (KeyError, Provider.DoesNotExist):
        error_message = '供应商不存在,请重试!'

    redirect = '/providers'

    return HttpResponseRedirect(redirect)  # 跳转

