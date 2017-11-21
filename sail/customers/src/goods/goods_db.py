from ...models import Goods, Picture


def get_goods_list():
    try:
        goods_list = Goods.objects.all()
    except (KeyError, Goods.DoesNotExist):
        goods_list = []

    goods_info_list = []
    for goods in goods_list:
        print(goods.provider.name)
        try:
            pictures = goods.pictures.all()
        except (KeyError, Picture.DoesNotExist):
            pictures = []

        goods_info = {
            'goods': goods,
            'pictures': pictures,
        }

        goods_info_list.append(goods_info)

    return goods_info_list

