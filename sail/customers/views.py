from django.shortcuts import render


# Create your views here.
def base_index(request):
    return render(request, 'customers/customers_index.html')


def customer_index(request):
    return render(request, 'customers/customers_index.html')


def goods_index(request):
    return render(request, 'common/error.html')


def provider_index(request):
    return render(request, 'common/error.html')


def cost_index(request):
    return render(request, 'common/error.html')


def customer_info(request):
    return render(request, 'common/error.html')


def customer_add(request):
    return render(request, 'common/error.html')


def customer_edit(request):
    return render(request, 'common/error.html')


def customer_del(request):
    return render(request, 'common/error.html')


def contact_info(request):
    return render(request, 'common/error.html')


def contact_add(request):
    return render(request, 'common/error.html')


def contact_edit(request):
    return render(request, 'common/error.html')


def contact_del(request):
    return render(request, 'common/error.html')


def trans_list(request):
    return render(request, 'common/error.html')


def trans_add(request):
    return render(request, 'common/error.html')


def trans_edit(request):
    return render(request, 'common/error.html')


def trans_del(request):
    return render(request, 'common/error.html')


def trans_goods_list(request):
    return render(request, 'common/error.html')


def trans_goods_add(request):
        return render(request, 'common/error.html')


def trans_goods_edit(request):
        return render(request, 'common/error.html')


def trans_goods_del(request):
        return render(request, 'common/error.html')


def provider_info(request):
    return render(request, 'common/error.html')


def provider_add(request):
        return render(request, 'common/error.html')


def provider_edit(request):
        return render(request, 'common/error.html')


def provider_del(request):
        return render(request, 'common/error.html')


def goods_info(request):
        return render(request, 'common/error.html')


def goods_add(request):
        return render(request, 'common/error.html')


def goods_edit(request):
        return render(request, 'common/error.html')


def goods_del(request):
        return render(request, 'common/error.html')


def cost_add(request):
        return render(request, 'common/error.html')


def cost_edit(request):
        return render(request, 'common/error.html')


def cost_del(request):
        return render(request, 'common/error.html')


def image_upload(request):
        return render(request, 'common/error.html')
