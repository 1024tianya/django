from .models import Customer, ContactInfo, CustomerTransInfo, CustomerTransGoodsInfo, PictureInfo
from .models import GoodsInfo, TransInfo, TransGoodsInfo, TransGoodsCostInfo, TransCostInfo, CostInfo, ProviderInfo


def get_goods_info_list():
    try:
        goods_info_list = GoodsInfo.objects.all()
    except (KeyError, GoodsInfo.DoesNotExist):
        goods_info_list = []

    return goods_info_list


def get_goods_info(goods_id):
    try:
        goods_info_list = GoodsInfo.objects.filter(id=goods_id)
    except (KeyError, GoodsInfo.DoesNotExist):
        return None

    print(goods_info_list)
    return goods_info_list[0]


def get_providers_info_list():
    try:
        providers_info_list = ProviderInfo.objects.all()
    except (KeyError, ProviderInfo.DoesNotExist):
        providers_info_list = []

    return providers_info_list


def get_provider_info(provider_id):
    try:
        provider_info = ProviderInfo.objects.filter(id=provider_id)
    except (KeyError, ProviderInfo.DoesNotExist):
        return None

    return provider_info[0]


def get_costs_info_list():
    try:
        costs_info_list = CostInfo.objects.all()
    except (KeyError, CostInfo.DoesNotExist):
        costs_info_list = []

    return costs_info_list


def get_cost_info(cost_id):
    try:
        cost_info = CostInfo.objects.filter(id=cost_id)
    except (KeyError, CostInfo.DoesNotExist):
        return None

    print(cost_info)
    return cost_info[0]


def get_trans_info_list(customer_id):
    try:
        trans_list = TransInfo.objects.filter(customer_key=customer_id).order_by('-trans_date')
    except (KeyError, TransInfo.DoesNotExist):
        trans_list = []

    return trans_list


def customer_info_list_compare(c1, c2):
    return c1['last_trans']['trans_date'] - c2['last_trans']['trans_date']


# get GoodsInfo with goods_info_id
def get_goodsinfo_in_list_or_db(goods_info_list, goods_info_id):
    if len(goods_info_list) > 0:
        for goods_info in goods_info_list:
            if goods_info.id == goods_info_id:
                return goods_info

    try:
        goods_info = GoodsInfo.objects.filter(id=goods_info_id)
        goods_info_list.append(goods_info)
    except (KeyError, GoodsInfo.DoesNotExist):
        goods_info = None

    return goods_info


def get_picture_info_list(goods_id, picture_info_cache):
    if len(picture_info_cache) is not 0:
        for item in picture_info_cache:
            if item['goods_id'] == goods_id:
                return item['picture_info_list']

    picture_cache_item = {}
    try:
        picture_info_list = PictureInfo.objects.filter(goods_info_key=goods_id)
        picture_cache_item['picture_info_list'] = picture_info_list
        picture_cache_item['goods_id'] = goods_id
        picture_info_cache.append(picture_cache_item)
    except (KeyError, PictureInfo.DoesNotExist):
        return []

    return picture_info_list


# TODO: limit returned trans info count
def get_trans_details_list_for_customer(customer_id):
    try:
        trans_list = TransInfo.objects.filter(customer_key=customer_id).order_by('-trans_date')
    except (KeyError, TransInfo.DoesNotExist):
        trans_list = []

    if len(trans_list) is 0:
        return []

    trans_info_list = []

    # caches
    picture_info_cache = []
    cost_info_cache = []

    for trans in trans_list:
        trans_details_info = get_trans_details_info(trans, picture_info_cache, cost_info_cache)
        trans_info_list.append(trans_details_info)

    return trans_info_list


def get_trans_details_info(trans, picture_info_cache, cost_info_cache):
    transgoods_info_list = []

    try:
        transgoods_list = TransGoodsInfo.objects.filter(trans_key=trans.id)
        for transgoods in transgoods_list:
            picture_info_list = get_picture_info_list(transgoods.goods_key.id, picture_info_cache)
            transgoods_cost_info_list = get_transgoods_cost_list(transgoods.id, cost_info_cache)
            transgoods_info = {
                'transgoods': transgoods,
                'picture_info_list': picture_info_list,
                'transgoods_cost_info_list': transgoods_cost_info_list
            }

            transgoods_info_list.append(transgoods_info)
    except (KeyError, TransGoodsInfo.DoesNotExist):
        transgoods_info_list = []

    trans_cost_list = get_trans_cost_list(trans.id, cost_info_cache)
    trans_details = {
            'trans': trans,
            'transgoods_info_list': transgoods_info_list,
            'trans_cost_list': trans_cost_list
    }

    return trans_details


# get cost list for trans goods with trans_id
def get_transgoods_cost_list(transgoods_id, cost_info_cache):
    try:
        trans_goods_cost_list = TransGoodsCostInfo.objects.filter(trans_goods_info_key=transgoods_id)
    except (KeyError, TransGoodsCostInfo.DoesNotExist):
        return []

    trans_goods_cost_info_list = []
    for trans_goods_cost in trans_goods_cost_list:
        cost_info = None
        if len(cost_info_cache) > 0:
            for cost in cost_info_cache:
                if cost.id == trans_goods_cost.cost_key:
                    cost_info = cost

        if cost_info is None:
            try:
                cost_info = CostInfo.objects.filter(id=trans_goods_cost.cost_key)
                cost_info_cache.append(cost_info)
            except (KeyError, CostInfo.DoesNotExist):
                cost_info = None
                print("cost info not found for TransGoodsCostInfo:" + trans_goods_cost)

        if cost_info is not None:
            trans_goods_cost_info_list.append(cost_info)

    return trans_goods_cost_info_list


# get cost list for trans with trans_id
def get_trans_cost_list(trans_id, cost_info_cache):
    try:
        trans_cost_list = TransCostInfo.objects.filter(trans_info_key_id=trans_id)
    except (KeyError, TransCostInfo.DoesNotExist):
        return []

    print(trans_cost_list)

    trans_cost_info_list = []
    for trans_cost in trans_cost_list:
        cost_info = None
        if len(cost_info_cache) > 0:
            for cost_item in cost_info_cache:
                if cost_item.id == trans_cost.cost_key:
                    cost_info = cost_item

        if cost_info is None:
            try:
                cost_info = CostInfo.objects.filter(id=trans_cost.cost_key)
                cost_info_cache.append(cost_info)
            except (KeyError, CostInfo.DoesNotExist):
                cost_info = None
                print("cost info not found for TransCostInfo:" + trans_cost)

        if cost_info is not None:
            trans_cost_info_list.append(cost_info)

    return trans_cost_info_list


# get trans details info with trans goods info with cost list and trans cost list
def get_trans_detail_info(trans, goods_info_cache, cost_info_cache):
    try:
        trans_goods_list = TransGoodsInfo.objects.filter(id=trans.id)
    except (KeyError, GoodsInfo.DoesNotExist):
        return []

    trans_goods_info_list = []

    for trans_goods_info in trans_goods_list:
        goods_info = get_goodsinfo_in_list_or_db(goods_info_cache, trans_goods_info.goods_key)
        goods_cost_list = get_transgoods_cost_list(cost_info_cache, trans_goods_info.id)

        trans_goods_detail_info = {
            'trans_goods_info': trans_goods_info,
            'goods_info': goods_info,
            'goods_cost_list': goods_cost_list
        }

        trans_goods_info_list.append(trans_goods_detail_info)

    trans_detail_info = {
        'trans': trans,
        'trans_goods_info_list': trans_goods_info_list,
        'trans_cost_list': get_trans_cost_list(trans.id, cost_info_cache),
    }

    return trans_detail_info


def getContactList(customer_id):
    try:
        contacts = ContactInfo.objects.filter(customer_id=customer_id)
    except (KeyError, Customer.DoesNotExist):
        contacts = []

    return contacts

