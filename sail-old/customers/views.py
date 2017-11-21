from django.shortcuts import render, get_object_or_404, render_to_response

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Customer, ContactInfo, PictureInfo,\
    GoodsInfo, TransInfo, TransGoodsInfo, TransGoodsCostInfo, TransCostInfo, CostInfo, ProviderInfo

from .forms import AddCustomer, ContactInfoForm, TransInfoForm, TransGoodsInfoForm, GoodsPictureForm,\
    TransInfoForm, QuickAddTransInfoForm, GoodsInfoForm, ProviderInfoForm, CostInfoForm

from .db_helper import get_trans_details_list_for_customer, get_trans_detail_info, \
    get_goods_info_list, get_goods_info, get_trans_info_list, getContactList, \
    get_providers_info_list, get_provider_info, get_costs_info_list, get_cost_info, \
    find_disabled_trans_record, find_disabled_transgoods_record, get_trans_cost_list, \
    get_transgoods_cost_list

# image upload import

from django.conf import settings
from django.http import HttpResponseRedirect


# Create your views here.
def content_index(request):
    return render(request, 'customers/error.html')


def customer_index(request):
    template = loader.get_template('customers/customersindex.html')

    try:
        # TODO: limit count of db search
        customers_list = Customer.objects.all()
    except (KeyError, Customer.DoesNotExist):
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

    trans_info_list = []
    for trans in trans_list:
        trans_info_list.append(get_trans_detail_info(trans, goods_info_cache))

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

    return render(request,'customers/add_template.html', context)


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

    return render(request,'customers/add_template.html', context)


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

    return render(request, 'customers/goods_index.html', {
        'goods_info_list': goods_info_list,
    })


def add_goods(request):
    providers_list = get_providers_info_list()

    error_message = ""
    providers_choices = []
    if len(providers_list) is 0:
        return render(request, 'customers/add_template.html',
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
            goods_name_text = fr.cleaned_data["name"]
            goods_price_float = fr.cleaned_data["price"]
            goods_cost_float = fr.cleaned_data["buying_price"]
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

    return render(request, 'customers/add_template.html', context)


def edit_goods(request, goods_id):
    goods_info = get_goods_info(goods_id)
    if goods_info is None:
        return render(request, 'customers/add_template.html',
                      {"title": "修改货物信息",
                       "error_message": "货物不存在!"})

    providers_list = get_providers_info_list()
    error_message = ""
    providers_choices = []
    if len(providers_list) is 0:
        return render(request, 'customers/add_template.html',
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
            goods_info.goods_name_text = fr.cleaned_data["name"]
            goods_info.goods_price_float = fr.cleaned_data["price"]
            goods_info.goods_cost_float = fr.cleaned_data["buying_price"]
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

    return render(request, 'customers/add_template.html', context)


def del_goods(request, goods_id):
    goods_info = get_goods_info(goods_id)
    if goods_info is not None:
        goods_info.delete()

    return HttpResponseRedirect('/trans/goods')  # 跳转


def image_upload(request, goods_id):
    if request.method == 'POST':
        form = GoodsPictureForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/success/url/')
    else:
        form = GoodsPictureForm()
    return render(request, 'customers/image_upload.html', {'form': form})

#
# def goods_image_view(FormView):
#     form_class = GoodsPictureForm
#     template_name = 'image_upload.html'
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         #files = request.FILES.getlist('file_field')
#         if form.is_valid():
#             form.save()
#             #for f in files:
#             #    ...  # Do something with each file.
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#
#     def handle_upload_image(file, file_name):
#         with open(MEDIA_URL, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)


#providers operation
def provider_index(request):
    providers_info_list = get_providers_info_list()

    return render(request, 'customers/providers_index.html', {
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

    return render(request, 'customers/add_template.html', context)


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

    return render(request, 'customers/add_template.html', context)


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

    return render(request, 'customers/costs_index.html', {
        'costs_info_list': costs_info_list,
    })


def add_cost(request):
    if request.method == "POST":
        fr = CostInfoForm(request.POST)
        if fr.is_valid():
            cost_name_text = fr.cleaned_data["name"]
            cost_price_float = fr.cleaned_data["price"]

            CostInfo.objects.create(cost_name_text=cost_name_text,
                                    cost_price_float=cost_price_float)
            return HttpResponseRedirect('/trans/costs/')  # 跳转
    else:
        fr = CostInfoForm()
        context = {"form": fr,
                   "title": "添加费用信息"
                   }

    return render(request, 'customers/add_template.html', context)


def add_cost_direct(request):
    trans_id = request.GET.get('trans_id', -1)
    transgoods_id = request.GET.get('transgoods_id', -1)
    cost_id = request.GET.get('cost_id', -1)
    cost_name = request.GET.get('cost_name', "")
    cost_value = request.GET.get('cost_value', -1)

    print("add_cost_direct:" + str(trans_id))
    message = ''
    if cost_id is not -1:
        try:
            cost = CostInfo.objects.get(id=cost_id)
        except (KeyError, TransInfo.DoesNotExist):
            cost = None
    else:
        cost = None

    if cost is not None:
        if cost_value is not -1 and cost_name is not "":
            if cost.cost_name_text == cost_name and cost.cost_price_float == cost_value:
                cost_name = ''
                cost_value = 0
            else:
                cost = None

    if cost is None and cost_value is not -1 and cost_name is not "":
        cost = CostInfo()
        cost.cost_name_text = cost_name
        cost.cost_price_float = cost_value
        cost.save()
    else:
        message = '费用信息错误'

    redirect = None
    if trans_id is not -1:
        try:
            trans = TransInfo.objects.get(id=trans_id)
        except (KeyError, TransInfo.DoesNotExist):
            trans = None
            message = '交易信息不存在！'

        if trans is not None and cost is not None:
            transgoods_cost = TransCostInfo()
            transgoods_cost.cost_key = cost
            transgoods_cost.trans_info_key = trans
            transgoods_cost.save()
            redirect = "/trans/customers/trans/edit/" + str(trans_id)
    elif transgoods_id is not -1:
        try:
            transgoods = TransGoodsInfo.objects.get(id=transgoods_id)
        except (KeyError, TransGoodsInfo.DoesNotExist):
            trans = None
            message = '信息不存在！'

        if transgoods is not None and cost is not None:
            transgoods_cost = TransGoodsCostInfo()
            transgoods_cost.cost_key = cost
            transgoods_cost.trans_goods_info_key = transgoods
            transgoods_cost.save()
            redirect = "/trans/customers/transgoods/edit/" + str(transgoods_id)
    else:
        message = "交易信息或交易货物信息不存在"

    if redirect is not None:
        return HttpResponseRedirect(redirect)  # 跳转

    context = {
        'message': message
    }

    #return render(request, 'customers/add_template.html', context)
    return HttpResponse(status=406)


def edit_cost(request, cost_id):
    cost_info = get_cost_info(cost_id)

    print(cost_info)
    if cost_info is None:
        context = {"error_message": "费用类别不存在!"}
    elif request.method == "POST":
        fr = CostInfoForm(request.POST)
        if fr.is_valid():
            cost_info.cost_name_text = fr.cleaned_data["name"]
            cost_info.cost_price_float = fr.cleaned_data["price"]
            cost_info.save()

            return HttpResponseRedirect('/trans/costs/')  # 跳转
    else:
        print(cost_info.cost_name_text)
        fr = CostInfoForm({'cost_name_text': cost_info.cost_name_text,
                           'cost_price_float': cost_info.cost_price_float})
        context = {"form": fr,
                   "title": "修改费用信息"
                   }

    return render(request, 'customers/add_template.html', context)


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

    return render(request,'customers/add_template.html', context)


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

    return render(request, 'customers/add_template.html', context)


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
    try:
        customer_key = Customer.objects.get(id=customer_id)
    except (KeyError, Customer.DoesNotExist):
        context = {"title": "添加交易信息",
                   "message": "客户不存在，请先添加联系人信息!",
                   "redirect": "/trans/customers/"
                   }
        return render(request, 'customers/add_template.html', context)

    contacts = getContactList(customer_key.id)
    if len(contacts) == 0:
        context = {"title": "添加交易信息",
                   "message": "联系人信息不存在，请先添加联系人信息!",
                   "redirect": "/trans/customers/"
                   }
        return render(request, 'customers/add_template.html', context)

    trans = find_disabled_trans_record(customer_key, contacts)

    return HttpResponseRedirect('/trans/customers/trans/edit/' + str(trans.id))  # 跳转


def edit_trans(request, trans_id):
    try:
        trans = TransInfo.objects.get(id=trans_id)
    except (KeyError, TransInfo.DoesNotExist):
        context = {"title": "编辑交易信息",
                   "message": "交易不存在,请重试!",
                   "redirect": "/trans/customers/contact/add"
                   }
        return render(request, 'customers/add_template.html', context)

    message = ''
    contacts = getContactList(trans.customer_key.id)
    print(contacts)

    if len(contacts) is 0:
        context = {"title": "编辑交易信息",
                   "message": "联系人信息不存在，请先添加联系人信息!",
                   "redirect": "/trans/customers/contact/add"
                   }
        return render(request, 'customers/add_template.html', context)

    goods_info_list = get_goods_info_list()

    if len(goods_info_list) is 0:
        context = {"title": "编辑交易信息",
                   "message": "货物信息不存在，请先添加货物信息!",
                   "redirect": "/trans/goods/add"
                   }
        return render(request, 'customers/add_template.html', context)

    contacts_choices = []
    for contact in contacts:
        contacts_choices.append((contact.id, contact.name_text))

    goods_choices = []
    sep = '-'
    for goods_info in goods_info_list:
        info_list = []
        info_list.append(goods_info.goods_provider.company_name_text)
        info_list.append(goods_info.goods_name_text)
        info_list.append(str(goods_info.goods_cost_float) + '(进货价)')
        goods_choices.append((goods_info.id, sep.join(info_list)))

    print(contacts_choices)
    print(goods_choices)

    if request.method == "POST":
        fr = TransInfoForm(contacts_choices, goods_choices, request.POST)

        print(fr)
        redirect = '/trans/customers/' + str(trans.customer_key.id)

        print(fr.is_valid())
        if fr.is_valid():
            trans.enabled_key = 1
            trans.trans_name_text = fr.cleaned_data['trans_name_text']
            trans.trans_order_number_text = fr.cleaned_data['trans_order_number_text']
            print(fr.cleaned_data['trans_handler_name_text'])
            trans.contract_name_text = fr.cleaned_data['contract_name_text']

            try:
                contact = ContactInfo.objects.get(id=fr.cleaned_data['trans_handler_name_text'])
                trans.contact_key = contact
            except (KeyError, ContactInfo.DoesNotExist):
                contact = None

            trans.trans_fax_int = fr.cleaned_data['trans_fax_int']
            trans.trans_payment_float = fr.cleaned_data['trans_payment_float']
            trans.trans_reduction_float = fr.cleaned_data['trans_reduction_float']
            trans.trans_date = fr.cleaned_data['trans_date']
            trans.goods_delivery_date = fr.cleaned_data['trans_delivery_date']
            trans.comment_text = fr.cleaned_data['comment_text']
            trans.save()
            return HttpResponseRedirect(redirect)  # 跳转

        context = {"form": fr,
                   "title": "编辑交易信息",
                   "message": message
                   }
    else:
        fr = TransInfoForm(contacts_choices, goods_choices, initial={
            'trans_name_text': trans.trans_name_text,
            'trans_order_number_text': trans.trans_order_number_text,
            'contract_name_text': trans.contract_name_text,
            'contact_key': trans.contact_key.id,
            'trans_fax_int': trans.trans_fax_int,
            'trans_payment_float': trans.trans_payment_float,
            'trans_reduction_float': trans.trans_reduction_float,
            'trans_date': trans.trans_date,
            'goods_delivery_date': trans.goods_delivery_date,
            'comment_text': trans.comment_text})

        trans_cost_list = get_trans_cost_list(trans.id)
        cost_list = get_costs_info_list()

        print(fr)
        context = {"form": fr,
                   "title": "编辑交易信息",
                   "message": message,
                   "cost_list": cost_list,
                   "extra_info": "trans_id",
                   "extra_id": str(trans_id),
                   "extra_cost_list": trans_cost_list
                   }

    return render(request, 'customers/add_template.html', context)


def del_trans(request, trans_id):
    try:
        trans = TransInfo.objects.get(id=trans_id)
    except (KeyError, TransInfo.DoesNotExist):
        context = {"title": "删除交易信息",
                   "message": "交易不存在,请重试!",
                   "redirect": "/trans/customers/contact/add"
                   }
        return render(request, 'customers/add_template.html', context)

    redirect = '/trans/customers/' + str(trans.customer_key.id)
    trans.delete()
    return HttpResponseRedirect(redirect)  # 跳转


def del_trans_cost(request, trans_cost_id):
    try:
        trans_cost_info = TransCostInfo.objects.get(id=trans_cost_id)
    except (KeyError, TransCostInfo.DoesNotExist):
        trans_cost_info = None

    if trans_cost_info is not None:
        redirect = '/trans/customers/trans/edit/' + str(trans_cost_info.trans_info_key.id)
        trans_cost_info.delete()
    else:
        context = {
                   "message": "花费记录不存在!"
                   }
        return render(request, 'customers/add_template.html', context)

    return HttpResponseRedirect(redirect)  # 跳转


def add_transgoods(request, trans_id):
    try:
        trans = TransInfo.objects.get(id=trans_id)
    except (KeyError, TransInfo.DoesNotExist):
        context = {"title": "添加交易物品信息",
                   "message": "交易不存在,请重试!",
                   "redirect": "/trans/customers/contact/add"
                   }
        return render(request, 'customers/add_template.html', context)

    goods_info_list = get_goods_info_list()
    if len(goods_info_list) is 0:
        context = {"title": "添加交易物品信息",
                   "message": "货物信息不存在，请先添加货物信息!",
                   "redirect": "/trans/goods/add"
                   }
        return render(request, 'customers/add_template.html', context)

    transgoods = find_disabled_transgoods_record(trans, goods_info_list)

    return HttpResponseRedirect('/trans/customers/transgoods/edit/' + str(transgoods.id))  # 跳转


def edit_transgoods(request, transgoods_id):
    try:
        transgoods = TransGoodsInfo.objects.filter(id=transgoods_id)[0]
    except (KeyError, TransGoodsInfo.DoesNotExist):
        context = {"title": "编辑交易物品信息",
                   "message": "交易物品不存在,请重试!",
                   "redirect": "/trans/customers/"
                   }
        return render(request, 'customers/add_template.html', context)

    goods_info_list = get_goods_info_list()

    if len(goods_info_list) is 0:
        context = {"title": "编辑交易物品信息",
                   "message": "货物信息不存在，请先添加货物信息!",
                   "redirect": "/trans/goods/add"
                   }
        return render(request, 'customers/add_template.html', context)

    goods_choices = []
    sep = '-'
    for goods_info in goods_info_list:
        info_list = []
        info_list.append(goods_info.goods_provider.company_name_text)
        info_list.append(goods_info.goods_name_text)
        info_list.append(str(goods_info.goods_cost_float) + '(进货价)')
        goods_choices.append((goods_info.id, sep.join(info_list)))

    if request.method == "POST":
        fr = TransGoodsInfoForm(goods_choices, request.POST)
        if fr.is_valid():
            try:
                goods = GoodsInfo.objects.get(id=fr.cleaned_data['goods_key'])
                transgoods.goods_key = goods
            except (KeyError, GoodsInfo.DoesNotExist):
                contact = None

            transgoods.enabled_key = 1
            transgoods.num_int = fr.cleaned_data['num_int']
            transgoods.price_float = fr.cleaned_data['price_float']
            transgoods.price_quoted_float = fr.cleaned_data['price_quoted_float']
            transgoods.goods_color_text = fr.cleaned_data['goods_color_text']
            transgoods.comment_text = fr.cleaned_data['comment_text']
            transgoods.save()

            print("transgoods:")
            print(transgoods)

            return HttpResponseRedirect('/trans/customers/' + str(transgoods.trans_key.customer_key.id))  # 跳转
    else:
        fr = TransGoodsInfoForm(goods_choices, initial={
            'goods_key': transgoods.goods_key.id,
            'num_int': transgoods.num_int,
            'price_float': transgoods.price_float,
            'price_quoted_float': transgoods.price_quoted_float,
            'goods_color_text': transgoods.goods_color_text,
            'comment_text': transgoods.comment_text,
        })

        cost_list = get_costs_info_list()
        transgoods_cost_list = get_transgoods_cost_list(transgoods_id)
        context = {"form": fr,
                   "title": "编辑交易物品信息",
                   "message": "",
                   "cost_list": cost_list,
                   "extra_info": "transgoods_id",
                   "extra_id": str(transgoods_id),
                   "extra_cost_list": transgoods_cost_list
                   }

    return render(request, 'customers/add_template.html', context)


def del_transgoods(request, transgoods_id):
    try:
        transgoods = TransGoodsInfo.objects.filter(id=transgoods_id)[0]
    except (KeyError, TransGoodsInfo.DoesNotExist):
        context = {"title": "删除交易物品信息",
                   "message": "交易物品不存在,请重试!",
                   "redirect": "/trans/customers/"
                   }
        return render(request, 'customers/add_template.html', context)

    redirect = '/trans/customers/' + str(transgoods.trans_key.customer_key.id)
    transgoods.delete()
    return HttpResponseRedirect(redirect)  # 跳转


def del_transgoods_cost(request, transgoods_cost_id):
    try:
        transgoods_cost_info = TransGoodsCostInfo.objects.get(id=transgoods_cost_id)
    except (KeyError, TransGoodsCostInfo.DoesNotExist):
        transgoods_cost_info = None

    if transgoods_cost_info is not None:
        redirect = '/trans/customers/transgoods/edit/' + str(transgoods_cost_info.trans_goods_info_key.trans_key.id)
        transgoods_cost_info.delete()
    else:
        context = {
                   "message": "花费记录不存在!"
                   }
        return render(request, 'customers/add_template.html', context)

    return HttpResponseRedirect(redirect)  # 跳转


def add_picture(request, trans_id):
    if request.method == "POST":
        fr = PictureInfo(request.POST)
        if fr.is_valid():
            trans = TransInfo.objects.get(id=trans_id)
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

    return render(request,'customers/add_template.html', context)


