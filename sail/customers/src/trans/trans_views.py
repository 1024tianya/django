from django.shortcuts import render
from django.http import HttpResponseRedirect

from ...models import Customer

from .customers_forms import CustomerForm
from .customers_db import get_customers_list, get_customer_with_contacts


def trans_list(request):
    # get condition from request
    customer_info_list = get_customers_list()
    context = {
        'customer_info_list': customer_info_list,
    }
    return render(request, 'trans/trans_list.html', context)


def customer_info(request, customer_id):
    customer_info = get_customer_with_contacts(customer_id)

    if customer_info is None:
        context = {
            'error_message': "客户没有找到！"
        }
    else:
        context = {
            'customer': customer_info['customer'],
            'contacts': customer_info['contacts'],
        }

    return render(request, 'customers/customers_index.html', context)


def customer_add(request):
    print('customer_add')
    if request.method == "POST":
        fr = CustomerForm(request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['company_name']
            address = fr.cleaned_data['company_address']
            invoice = fr.cleaned_data['company_invoice_text']
            comment = fr.cleaned_data['company_comment']
            customer = Customer(name=name,
                                address=address,
                                invoice=invoice,
                                comment=comment)
            customer.save()
            return HttpResponseRedirect('/customers/')  # 跳转
    else:
        fr = CustomerForm()
        context = {"form": fr,
                   "title": "添加客户"
                   }

    return render(request, 'common/add_template.html', context)


def customer_edit(request, customer_id):
    error_message = ''
    try:
        customer = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        error_message = '客户不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = CustomerForm(request.POST)
        if fr.is_valid():
            customer.name = fr.cleaned_data['company_name']
            customer.address = fr.cleaned_data['company_address']
            customer.invoice = fr.cleaned_data['company_invoice_text']
            customer.comment = fr.cleaned_data['company_comment']
            customer.save()
            return HttpResponseRedirect('/customers/')  # 跳转
    elif error_message == "":
        fr = CustomerForm({'company_name': customer.name,
                           'company_address': customer.address,
                           'company_invoice_text': customer.invoice,
                           'company_comment': customer.comment})

        context = {"form": fr,
                   "title": "修改客户",
                   "customer_info": customer,
                   }
    else:
        context = {"error_message": error_message}

    return render(request, 'common/add_template.html', context)


def customer_del(request, customer_id):
    error_message = ''
    try:
        customer = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        error_message = '客户不存在,请重试!'

    if error_message == '':
        customer.delete()

    redirect = '/customers'

    return HttpResponseRedirect(redirect)  # 跳转

