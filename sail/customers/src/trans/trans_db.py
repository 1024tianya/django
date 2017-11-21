from ...models import Trans, TransGoodsInfo, Cost, Picture


# TODO: limit returned trans info count
def get_trans_details_list_for_customer(customer_id):
    try:
        trans_list = Trans.objects.filter(customer_key=customer_id, enabled_key=1).order_by('-trans_date')
    except (KeyError, Trans.DoesNotExist):
        trans_list = []

    if len(trans_list) is 0:
        return []

    trans_info_list = []

    for trans in trans_list:
        trans_details_info = get_trans_details_info(trans)
        trans_info_list.append(trans_details_info)

    return trans_info_list


def get_trans_details_info(trans):
    if trans is None:
        return None

    try:
        trans_goods_list = trans.trans_good.all()
    except (KeyError, TransGoodsInfo.DoesNotExist):
        trans_goods_list = []

    if len(trans_goods_list) > 0:
        trans_goods_details_list = []
        for trans_goods in trans_goods_list:
            try:
                picture_list = trans_goods.pictures.all()
            except (KeyError, Picture.DoesNotExist):
                picture_list = []

            try:
                costs = trans_goods.costs.all()
            except (KeyError, Cost.DoesNotExist):
                costs = []

            trans_goods_details = {
                'trans_goods': trans_goods,
                'picture_info_list': picture_list,
                'costs_list': costs
            }

            trans_goods_details_list.append(trans_goods_details)

    trans_cost_list = trans.costs.all()
    trans_details = {
        'trans': trans,
        'trans_goods_details_list': trans_goods_details_list,
        'trans_cost_list': trans_cost_list,
    }

    return trans_details
