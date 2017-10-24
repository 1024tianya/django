from django.shortcuts import render, get_object_or_404, render_to_response

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Customer, ContactInfo, CustomerTransInfo, CustomerTransGoodsInfo, PictureInfo,\
    GoodsInfo, TransInfo, TransGoodsInfo, TransGoodsCostInfo, TransCostInfo, CostInfo, ProviderInfo

from .forms import AddCustomer, ContactInfoForm, TransInfoForm, TransGoodsInfo, PictureInfo,\
    TransInfoForm, QuickAddTransInfoForm, GoodsInfoForm, ProviderInfoForm, CostInfoForm

from .db_helper import get_trans_details_list_for_customer, get_trans_detail_info, \
    get_goods_info_list, get_goods_info, get_trans_info_list, getContactList, \
    get_providers_info_list, get_provider_info, get_costs_info_list, get_cost_info


# Create your views here.
def content_index(request):
    return render(request, 'customers/index.html')


def customer_index(request):
    template = loader.get_template('customers/customersindex.html')

    try:
        # TODO: limit count of db search
        customers_list = Customer.objects.all()
    except (KeyError, CustomerTransInfo.DoesNotExist):
        customers_list = []

    customer_info_list = []
    for customer in customers_list:
        # init contact list for current customer
        contacts_display_num = 3
        contacts_list = getContactList(customer.id)
        contact_name_list = []
        if contacts_list.count() > 0:
            for contact in contacts_list:
                contact_name_list.append(contact.name_text)
                if len(contact_name_list) >= contacts_display_num:
                    break

        # get last trans info
        trans_list = get_trans_info_list(customer.id)
        trans_count = len(trans_list)

        if trans_count > 0:
            last_trans = {
                'trans_order_number_text': trans_list[0].trans_order_number_text,
                'trans_date': trans_list[0].trans_date,
            }
        else:
            last_trans = {
                'trans_order_number_text': '',
                'trans_date': '',
            }

        customer_info = {
            'customer': customer,
            'contacts': contacts_list,
            'trans_count': trans_count,
            'last_trans': last_trans,
        }

        customer_info_list.append(customer_info)

    customer_info_list.sort(key=customer_date_key, reverse=True)
    context = {
        'customer_info_list': customer_info_list,
    }

    return HttpResponse(template.render(context, request))


def customer_date_key(customer_info):
    print(customer_info)
    if customer_info['trans_count'] > 0:
        return customer_info['last_trans']['trans_date']

    return customer_info['customer'].customer_add_date.date()


def customer_detail(request, customer_id):
    try:
        customer_info = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        return render(request, 'customers/detail.html', {
            'error_message': "no customer found for " + customer_id,
        })

    print('customer_detail, customer_info:' + customer_info.customer_company_name_text)

    contact_list = getContactList(customer_id)

    print('customer_detail, contact_list:%d' %len(contact_list))
    trans_list = get_trans_info_list(customer_id)

    print('customer_detail, trans_list:%d' %len(trans_list))

    # cache to reduce db search
    goods_info_cache = []
    cost_info_cache = []

    trans_info_list = []
    for trans in trans_list:
        trans_info_list.append(get_trans_detail_info(trans, goods_info_cache, cost_info_cache))

    return render(request, 'customers/detail.html', {
        'customer_info': customer_info,
        'contact_info': contact_list,
        'trans_info_list': trans_info_list,
    })


def add_customer(request):
    if request.method == "POST":
        fr = AddCustomer(request.POST)
        if fr.is_valid():
            name = fr.cleaned_data['company_name']
            address = fr.cleaned_data['company_address']
            invoice = fr.cleaned_data['company_invoice_text']
            comment = fr.cleaned_data['company_comment']
            Customer.objects.create(customer_company_name_text=name,
                                    customer_company_address_text=address,
                                    customer_company_invoice_text=invoice,
                                    customer_comment_text=comment)
            return HttpResponseRedirect('/trans/customers/')  # 跳转
    else:
        fr = AddCustomer()
        context = {"form":fr,
               "title":"添加客户"
               }

    return render(request,'customers/addtemplate.html', context)


def edit_customer(request, customer_id):
    error_message = ''
    try:
        customer_info = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        error_message = '客户不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = AddCustomer(request.POST)

        if fr.is_valid():
            customer_info.customer_company_name_text = fr.cleaned_data['company_name']
            customer_info.customer_company_address_text = fr.cleaned_data['company_address']
            customer_info.customer_company_invoice_text = fr.cleaned_data['company_invoice_text']
            customer_info.customer_comment_text = fr.cleaned_data['company_comment']
            customer_info.save()

            return HttpResponseRedirect('/trans/customers/')  # 跳转
    elif error_message == "":
        fr = AddCustomer({'company_name': customer_info.customer_company_name_text,
                            'company_address': customer_info.customer_company_address_text,
                            'company_invoice_text': customer_info.customer_company_invoice_text,
                            'company_comment': customer_info.customer_comment_text})

        context = {"form": fr,
                "title":"修改客户",
                "customer_info": customer_info,
        }
    else:
        context = {"error_message": error_message}

    return render(request,'customers/addtemplate.html', context)


def del_customer(request, customer_id):
    error_message = ''
    try:
        customer_info = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        error_message = '客户不存在,请重试!'

    if error_message == '':
        customer_info.delete()

    redirect = '/trans/customers'

    return HttpResponseRedirect(redirect)  # 跳转


# goods operations
def goods_index(request):
    goods_info_list = get_goods_info_list()

    return render(request, 'customers/goodsindex.html', {
        'goods_info_list': goods_info_list,
    })


def add_goods(request):
    providers_list = get_providers_info_list()

    error_message = ""
    providers_choices = []
    if len(providers_list) is 0:
        return render(request, 'customers/addtemplate.html',
                      {"title": "添加货物信息",
                       "error_message": "供应商信息不存在， 请先添加供应商信息!",
                       "redirect": "/trans/providers/add"})

    for provider in providers_list:
        providers_choices.append((provider.id, provider.company_name_text))

    if request.method == "POST":
        fr = GoodsInfoForm(providers_choices, request.POST)
        if fr.is_valid():
            provider_info = get_provider_info(fr.cleaned_data['goods_provider'])
            goods_provider = provider_info
            goods_name_text = fr.cleaned_data['goods_name_text']
            goods_price_float = fr.cleaned_data['goods_price_float']
            goods_cost_float = fr.cleaned_data['goods_cost_float']
            comment_text = fr.cleaned_data['comment_text']

            GoodsInfo.objects.create(goods_provider=goods_provider,
                                     goods_name_text=goods_name_text,
                                     goods_price_float=goods_price_float,
                                     goods_cost_float=goods_cost_float,
                                     comment_text=comment_text)
            return HttpResponseRedirect('/trans/goods/')  # 跳转
    else:
        fr = GoodsInfoForm(providers_choices)
        context = {"form": fr,
                   "title": "添加货物信息",
                   "error_message": error_message,
                   }

    return render(request, 'customers/addtemplate.html', context)


def edit_goods(request, goods_id):
    goods_info = get_goods_info(goods_id)
    if goods_info is None:
        return render(request, 'customers/addtemplate.html',
                      {"title": "修改货物信息",
                       "error_message": "货物不存在!"})

    providers_list = get_providers_info_list()
    error_message = ""
    providers_choices = []
    if len(providers_list) is 0:
        return render(request, 'customers/addtemplate.html',
                      {"title": "修改货物信息",
                       "error_message": "供应商信息不存在， 请先添加供应商信息!",
                       "redirect": "/trans/providers/add"})

    for provider in providers_list:
        providers_choices.append((provider.id, provider.company_name_text))

    if request.method == "POST":
        fr = GoodsInfoForm(providers_choices, request.POST)
        if fr.is_valid():
            provider_info = get_provider_info(fr.cleaned_data['goods_provider'])
            goods_info.goods_provider = provider_info
            goods_info.goods_name_text = fr.cleaned_data['goods_name_text']
            goods_info.goods_price_float = fr.cleaned_data['goods_price_float']
            goods_info.goods_cost_float = fr.cleaned_data['goods_cost_float']
            goods_info.comment_text = fr.cleaned_data['comment_text']
            goods_info.save()
            return HttpResponseRedirect('/trans/goods/')  # 跳转
    else:
        fr = GoodsInfoForm(providers_choices,
                           {'goods_provider': goods_info.goods_provider.id,
                            'goods_name_text': goods_info.goods_name_text,
                            'goods_price_float': goods_info.goods_price_float,
                            'goods_cost_float': goods_info.goods_cost_float,
                            'comment_text': goods_info.comment_text})
        context = {"form": fr,
                   "title": "修改货物信息",
                   "error_message": error_message,
                   }

    return render(request, 'customers/addtemplate.html', context)


def del_goods(request, goods_id):
    goods_info = get_goods_info(goods_id)
    if goods_info is not None:
        goods_info.delete()

    return HttpResponseRedirect('/trans/goods')  # 跳转


#providers operation
def provider_index(request):
    providers_info_list = get_providers_info_list()

    return render(request, 'customers/providersindex.html', {
        'providers_info_list': providers_info_list,
    })


def add_provider(request):
    if request.method == "POST":
        fr = ProviderInfoForm(request.POST)
        if fr.is_valid():
            company_name_text = fr.cleaned_data['company_name_text']
            company_address_text = fr.cleaned_data['company_address_text']
            comment_text = fr.cleaned_data['comment_text']

            ProviderInfo.objects.create(company_name_text=company_name_text,
                                        company_address_text=company_address_text,
                                        comment_text=comment_text)
            return HttpResponseRedirect('/trans/providers/')  # 跳转
    else:
        fr = ProviderInfoForm()
        context = {"form": fr,
                   "title": "添加供应商"
                   }

    return render(request, 'customers/addtemplate.html', context)


def edit_provider(request, provider_id):
    provider_info = get_provider_info(provider_id)

    print(provider_info)
    if provider_info is None:
        context = {"error_message": "供应商不存在!"}
    elif request.method == "POST":
        fr = ProviderInfoForm(request.POST)
        if fr.is_valid():
            provider_info.company_name_text = fr.cleaned_data['company_name_text']
            provider_info.company_address_text = fr.cleaned_data['company_address_text']
            provider_info.comment_text = fr.cleaned_data['comment_text']
            provider_info.save()

            return HttpResponseRedirect('/trans/providers/')  # 跳转
    else:
        print(provider_info.company_name_text)
        fr = ProviderInfoForm({'company_name_text': provider_info.company_name_text,
                               'company_address_text': provider_info.company_address_text,
                              'comment_text': provider_info.comment_text})
        context = {"form": fr,
                   "title": "添加供应商"
                   }

    return render(request, 'customers/addtemplate.html', context)


def del_provider(request, provider_id):
    try:
        provider_info = ProviderInfo.objects.get(pk=provider_id)
    except (KeyError, ProviderInfo.DoesNotExist):
        provider_info = None

    if provider_info is not None:
        provider_info.delete()

    return HttpResponseRedirect('/trans/providers')  # 跳转


#costs operation
def cost_index(request):
    costs_info_list = get_costs_info_list()

    return render(request, 'customers/costsindex.html', {
        'costs_info_list': costs_info_list,
    })


def add_cost(request):
    if request.method == "POST":
        fr = CostInfoForm(request.POST)
        if fr.is_valid():
            cost_name_text = fr.cleaned_data['cost_name_text']
            cost_price_float = fr.cleaned_data['cost_price_float']

            CostInfo.objects.create(cost_name_text=cost_name_text,
                                    cost_price_float=cost_price_float)
            return HttpResponseRedirect('/trans/costs/')  # 跳转
    else:
        fr = CostInfoForm()
        context = {"form": fr,
                   "title": "添加费用信息"
                   }

    return render(request, 'customers/addtemplate.html', context)


def edit_cost(request, cost_id):
    cost_info = get_cost_info(cost_id)

    print(cost_info)
    if cost_info is None:
        context = {"error_message": "费用类别不存在!"}
    elif request.method == "POST":
        fr = CostInfoForm(request.POST)
        if fr.is_valid():
            cost_info.cost_name_text = fr.cleaned_data['cost_name_text']
            cost_info.cost_price_float = fr.cleaned_data['cost_price_float']
            cost_info.save()

            return HttpResponseRedirect('/trans/costs/')  # 跳转
    else:
        print(cost_info.cost_name_text)
        fr = CostInfoForm({'cost_name_text': cost_info.cost_name_text,
                           'cost_price_float': cost_info.cost_price_float})
        context = {"form": fr,
                   "title": "修改费用信息"
                   }

    return render(request, 'customers/addtemplate.html', context)


def del_cost(request, cost_id):
    try:
        cost_info = CostInfo.objects.get(pk=cost_id)
    except (KeyError, ProviderInfo.DoesNotExist):
        cost_info = None

    if cost_info is not None:
        cost_info.delete()

    return HttpResponseRedirect('/trans/costs')  # 跳转


# contact operation
def add_contact(request, customer_id):
    if request.method == "POST":
        fr = ContactInfoForm(request.POST)
        if fr.is_valid():
            customer = Customer.objects.get(id=customer_id)

            contact = ContactInfo()
            contact.customer = customer
            contact.name_text = fr.cleaned_data['name_text']
            contact.address_text = fr.cleaned_data['address_text']
            contact.mobile1_text = fr.cleaned_data['mobile1_text']
            contact.mobile2_text = fr.cleaned_data['mobile2_text']
            contact.phone1_text = fr.cleaned_data['phone1_text']
            contact.phone2_text = fr.cleaned_data['phone2_text']
            contact.email = fr.cleaned_data['email']
            contact.comment_text = fr.cleaned_data['comment_text']
            contact.save()

            return HttpResponseRedirect('/trans/customers/' + customer_id)  # 跳转
    else:
        fr = ContactInfoForm()  # 定义HostAddForm()给变量fr，其实这里是空值来的，
        context = {"form":fr,
               "title":"添加联系人"
               }

    return render(request,'customers/addtemplate.html', context)


def edit_contact(request, contact_id):
    error_message = ''
    try:
        contact = ContactInfo.objects.get(id=contact_id)
    except (KeyError, ContactInfo.DoesNotExist):
        error_message = '客户不存在,请重试!'

    if error_message == '' and request.method == "POST":
        fr = ContactInfoForm(request.POST)

        redirect = '/trans/customers/' + str(contact.customer.id)

        if fr.is_valid():
            contact.name_text = fr.cleaned_data['name_text']
            contact.address_text = fr.cleaned_data['address_text']
            contact.mobile1_text = fr.cleaned_data['mobile1_text']
            contact.mobile2_text = fr.cleaned_data['mobile2_text']
            contact.phone1_text = fr.cleaned_data['phone1_text']
            contact.phone2_text = fr.cleaned_data['phone2_text']
            contact.email = fr.cleaned_data['email']
            contact.comment_text = fr.cleaned_data['comment_text']
            contact.save()

        return HttpResponseRedirect(redirect)  # 跳转
    elif error_message == "":
            fr = ContactInfoForm({'name_text': contact.name_text,
                              'address_text': contact.address_text,
                              'mobile1_text': contact.mobile1_text,
                              'mobile2_text': contact.mobile2_text,
                              'phone1_text': contact.phone1_text,
                              'phone2_text': contact.phone2_text,
                              'email': contact.email,
                              'comment_text': contact.comment_text})

            context = {"form": fr,
                       "title": "添加联系人"
                       }
    else:
            context = {"error_message": error_message}

    return render(request, 'customers/addtemplate.html', context)


def del_contact(request, contact_id):
    error_message = ''
    try:
        contact = ContactInfo.objects.get(id=contact_id)
    except (KeyError, ContactInfo.DoesNotExist):
        error_message = '客户不存在,请重试!'

    redirect = '/trans/customers/' + str(contact.customer.id)

    if error_message == '':
        contact.delete()

    return HttpResponseRedirect(redirect)  # 跳转


def trans_list_of_customer(request, customer_id):
    trans_info_list = get_trans_details_list_for_customer(customer_id)

    return render(request, 'customers/transinfolist.html', {
        'customer_id': customer_id,
        'trans_info_list': trans_info_list,
    })


def add_trans(request, customer_id):
    message = ''
    contacts = getContactList(customer_id)
    print(contacts)

    if len(contacts) is 0:
        context = {"title": "添加交易信息",
                   "message": "联系人信息不存在，请先添加联系人信息!",
                   "redirect": "/trans/customers/contact/add"
                   }
        return render(request, 'customers/addtemplate.html', context)

    choices = []
    if len(contacts) > 0:
        for contact in contacts:
            choices.append((contact.name_text, contact.name_text))

    if request.method == "POST":
        fr = TransInfoForm(choices, request.POST)

        print(choices)
        #print(fr)
        if fr.is_valid():
            try:
                customer_key = Customer.objects.get(id=customer_id)
            except (KeyError, Customer.DoesNotExist):
                return HttpResponseRedirect('/trans/customers/')  # 跳转

            trans = TransInfo()
            trans.customer_key = customer_key
            trans.trans_name_text = ""
            trans.trans_order_number_text = fr.cleaned_data['trans_order_number_text']
            #trans.contact_key = fr.cleaned_data['contact_key']
            print(fr.cleaned_data['contact_key'])

            try:
                contact = ContactInfo.objects.get(customer=customer_id, name_text=fr.cleaned_data['contact_key'])
                trans.contact_key = contact
            except (KeyError, ContactInfo.DoesNotExist):
                contact = None

            print(contact)

            trans.trans_fax_int = fr.cleaned_data['trans_fax_int']
            trans.trans_date = fr.cleaned_data['trans_date']
            trans.goods_delivery_date = fr.cleaned_data['goods_delivery_date']
            trans.comment_text = fr.cleaned_data['comment_text']
            trans.save()

            return HttpResponseRedirect('/trans/customers/' + customer_id)  # 跳转
    else:
        fr = TransInfoForm(choices)

    context = {"form": fr,
               "title": "添加交易信息",
               "message": message
               }

    print(choices)

    return render(request, 'customers/addtemplate.html', context)


def edit_trans(request, trans_id):
    error_message = ''
    message = ''
    try:
        trans = CustomerTransInfo.objects.get(id=trans_id)
    except (KeyError, CustomerTransInfo.DoesNotExist):
        error_message = '客户不存在,请重试!'

    print(trans)

    if error_message == '' and request.method == "POST":
        fr = TransInfoForm(request.POST)

        print(fr)
        redirect = '/customers/' + str(trans.customer_id)

        print(fr.is_valid())
        if fr.is_valid():
            trans.trans_name_text = fr.cleaned_data['trans_name_text']
            print(trans.trans_name_text)
            trans.trans_handler_name_text = fr.cleaned_data['trans_handler_name_text']
            trans.trans_total_num_int = fr.cleaned_data['trans_total_num_int']
            trans.trans_payment_int = fr.cleaned_data['trans_payment_int']
            trans.trans_fax_int = fr.cleaned_data['trans_fax_int']
            trans.trans_expenses_int = fr.cleaned_data['trans_expenses_int']
            trans.trans_other_charge_int = fr.cleaned_data['trans_other_charge_int']
            trans.trans_date = fr.cleaned_data['trans_date']
            trans.trans_delivery_date = fr.cleaned_data['trans_delivery_date']
            trans.trans_order_number_text = fr.cleaned_data['trans_order_number_text']
            trans.trans_comment_text = fr.cleaned_data['trans_comment_text']
            trans.save()
            return HttpResponseRedirect(redirect)  # 跳转

        context = {"form": fr,
                   "title": "修改交易信息",
                   "message": message
                   }
    elif error_message == "":
        fr = TransInfoForm(initial={'trans_name_text': trans.trans_name_text,
                              'trans_handler_name_text': trans.trans_handler_name_text,
                              'trans_total_num_int': trans.trans_total_num_int,
                              'trans_payment_int': trans.trans_payment_int,
                              'trans_fax_int': trans.trans_fax_int,
                              'trans_expenses_int': trans.trans_expenses_int,
                              'trans_other_charge_int': trans.trans_other_charge_int,
                              'trans_date': trans.trans_date,
                              'trans_delivery_date': trans.trans_delivery_date,
                              'trans_order_number_text': trans.trans_order_number_text,
                              'trans_comment_text': trans.trans_comment_text})

        print(fr)
        contacts = getContactList(trans.customer.id)
        print(contacts)

        if len(contacts) > 0:
            fr.fields['trans_handler_name_text'].widget.choices = contacts
        else:
            message = "联系人不存在，请添加！"

        context = {"form": fr,
                   "title": "修改交易信息",
                   "message": message
                   }
    else:
        context = {"error_message": error_message}

    return render(request, 'customers/addtemplate.html', context)


def add_picture(request, trans_id):
    if request.method == "POST":
        fr = PictureInfo(request.POST)
        if fr.is_valid():
            trans = CustomerTransInfo.objects.get(id=trans_id)
            picture = PictureInfo()
            picture.customer_trans_info = trans
            picture.trans_goods_picture_name_text = fr.cleaned_data['trans_goods_picture_name_text']
            picture.trans_goods_picture_path_text = fr.cleaned_data['trans_goods_picture_path_text']
            picture.save()

            return HttpResponseRedirect('/customers/%d' %trans.customer_id)  # 跳转
    else:
        fr = PictureInfo()
        context = {"form":fr,
               "title":"添加图片"
               }

    return render(request,'customers/addtemplate.html', context)


