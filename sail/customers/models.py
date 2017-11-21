from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import datetime
import time

from django.utils import timezone


@python_2_unicode_compatible  # only if you need to support Python 2
class Contact(models.Model):
    # ...
    def __str__(self):
        return self.name_text

    name_text = models.CharField(max_length=20, verbose_name="姓名")
    address_text = models.CharField(max_length=100, blank=True, verbose_name="地址")
    mobile1_text = models.CharField(max_length=30, blank=True, verbose_name="工作手机号码")
    mobile2_text = models.CharField(max_length=30, blank=True, verbose_name="家庭手机号码")
    phone1_text = models.CharField(max_length=30, blank=True, verbose_name="固定电话")
    phone2_text = models.CharField(max_length=30, blank=True, verbose_name="固定电话2")
    email = models.CharField(max_length=30, blank=True, verbose_name="Email")
    comment = models.CharField(max_length=1000, blank=True, verbose_name="备注")
    # auto add
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")

    class Meta:
        verbose_name = "联系人信息"
        verbose_name_plural = "联系人信息"


@python_2_unicode_compatible  # only if you need to support Python 2
class Customer(models.Model):
    def __str__(self):
        return self.name + ', address:' + self.address + ', added at:' + self.add_date.strftime("%Y-%m-%d")

    def was_published_recently(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)

    contacts = models.ManyToManyField(Contact, blank=True, related_name='customer_company', verbose_name="联系人")

    name = models.CharField(max_length=50, verbose_name="公司名称")
    address = models.CharField(max_length=100, blank=True, verbose_name="地址")
    # auto add
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    invoice = models.CharField(max_length=50, blank=True, verbose_name="发票抬头")
    comment = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "客户信息"
        verbose_name_plural = "客户信息"


class Provider(models.Model):
    # ...
    def __str__(self):
        return self.name

    contacts = models.ManyToManyField(Contact, blank=True, related_name='provider_company', verbose_name="联系人")

    name = models.CharField(max_length=50, verbose_name="公司名称")
    address = models.CharField(max_length=100, blank=True, verbose_name="地址")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    comment = models.CharField(max_length=1000, blank=True, verbose_name="备注")


###
class Picture(models.Model):
    # ...
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, blank=True, verbose_name="名称")
    picture = models.ImageField(verbose_name="图片", upload_to='images', blank=True)
    comment = models.CharField(max_length=1000, blank=True, verbose_name="备注")


# goods library
class Goods(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE,
                                 related_name='goods', verbose_name="图片")
    pictures = models.ManyToManyField(Picture, blank=True,
                                      related_name='goods', verbose_name="图片")

    name = models.CharField(max_length=100, verbose_name="名称")
    price = models.FloatField(default=0, verbose_name="单价")
    buying_price = models.FloatField(default=0, verbose_name="进货价")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    comment = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    def __str__(self):
        goods_info = self.name + ", "\
                     + str(self.price) + ", " \
                     + str(self.buying_price)
        return goods_info

    class Meta:
        verbose_name = "货物信息"
        verbose_name_plural = "货物信息"


class Cost(models.Model):
    def __str__(self):
        return self.name + '-' + str(self.price) + '-' + str(self.add_date)

    name = models.CharField(max_length=100, verbose_name="费用名称")
    price = models.FloatField(default=0, verbose_name="价格")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")


class Trans(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='trans', verbose_name="公司")
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,
                                related_name='trans', verbose_name="联系人")
    costs = models.ManyToManyField(Cost, blank=True,
                                   related_name='trans', verbose_name="费用")

    enabled_key = models.IntegerField(default=0, blank=False)
    trans_name_text = models.CharField(max_length=100, verbose_name="交易名称")
    trans_order_number_text = models.CharField(max_length=100, blank=True, verbose_name="订单号")
    contract_name_text = models.CharField(max_length=100, verbose_name="合同编号")
    trans_fax_int = models.IntegerField(default=0, blank=True, verbose_name="税点")
    trans_payment_float = models.FloatField(default=0, blank=True, verbose_name="总货款")
    trans_reduction_float = models.FloatField(default=0, blank=True, verbose_name="优惠")
    trans_date = models.DateField(verbose_name="交易日期", blank=True, null=True)
    goods_delivery_date = models.DateField(verbose_name="交货日期", blank=True, null=True)
    # auto add
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    def __str__(self):
        trans_info = self.customer_key.customer_company_name_text + ", "\
                     + self.trans_name_text + ", "\
                     + self.trans_order_number_text + ", " \
                     + self.contact_key.name_text
        return trans_info

    class Meta:
        verbose_name = "交易信息"
        verbose_name_plural = "交易信息"


class TransGoodsInfo(models.Model):
    trans = models.ForeignKey(Trans, on_delete=models.CASCADE,
                              related_name='trans_goods', verbose_name="交易")
    goods = models.ForeignKey(Goods,
                              related_name='trans_goods', verbose_name="货物")

    pictures = models.ManyToManyField(Picture, blank=True,
                                      related_name='trans_goods', verbose_name="图片")
    costs = models.ManyToManyField(Cost, blank=True,
                                   related_name='trans_goods', verbose_name="费用")

    enabled_key = models.IntegerField(default=0, blank=False)
    num_int = models.IntegerField(default=0, verbose_name="数量")
    price_float = models.FloatField(default=0, verbose_name="成交单价")
    price_quoted_float = models.FloatField(default=0, verbose_name="报价")
    goods_color_text = models.CharField(max_length=100, verbose_name="颜色")
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    def __str__(self):
        goods_info = self.trans_key.__str__() + ", "\
                     + self.goods_key.__str__() + ", "\
                     + str(self.num_int) + ", "\
                     + str(self.price_float)
        return goods_info

    class Meta:
        verbose_name = "交易货物信息"
        verbose_name_plural = "交易货物信息"

