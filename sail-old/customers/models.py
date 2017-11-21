from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import datetime

from django.utils import timezone

from django.conf import settings
# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class Customer(models.Model):
    def __str__(self):
        return self.customer_company_name_text

    def was_published_recently(self):
        return self.customer_add_date >= timezone.now() - datetime.timedelta(days=1)

    customer_company_name_text = models.CharField(max_length=50, verbose_name="公司名称")
    customer_company_address_text = models.CharField(max_length=100, blank=True, verbose_name="地址")

    # contacts key
    contacts = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    trans = models.ForeignKey(TransInfo, unique=True)

    # auto add
    customer_add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    customer_company_invoice_text = models.CharField(max_length=50, blank=True, verbose_name="发票抬头")
    customer_comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "客户信息"
        verbose_name_plural = "客户信息"


@python_2_unicode_compatible  # only if you need to support Python 2
class ContactInfo(models.Model):
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
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")
    # auto add
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")

    class Meta:
        verbose_name = "联系人信息"
        verbose_name_plural = "联系人信息"


class ProviderInfo(models.Model):
    # ...
    def __str__(self):
        return self.company_name_text

    company_name_text = models.CharField(max_length=50, verbose_name="公司名称")
    company_address_text = models.CharField(max_length=100, blank=True, verbose_name="地址")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE)


###
# goods library
class GoodsInfo(models.Model):
    goods_name_text = models.CharField(max_length=100, verbose_name="名称")
    goods_price_float = models.FloatField(default=0, verbose_name="单价")
    goods_cost_float = models.FloatField(default=0, verbose_name="进货价")
    pictures = models.ForeignKey(GoodsPicture, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加日期")
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")

    def __str__(self):
        goods_info = self.goods_name_text + ", "\
                     + str(self.goods_price_float) + ", " \
                     + str(self.goods_cost_float)
        return goods_info

    class Meta:
        verbose_name = "货物信息"
        verbose_name_plural = "货物信息"


# picture library
class PictureInfo(models.Model):
    # ...
    def __str__(self):
        return self.picture_name_text

    picture_name_text = models.CharField(max_length=100, blank=True, verbose_name="名称")
    picture_path_text = models.CharField(max_length=100, verbose_name="图片路径名")
    picture = models.ImageField(verbose_name="图片", upload_to='photos', blank=True)
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")


class GoodsPicture(models.Model):
    # ...
    def __str__(self):
        return self.picture_name_text

    picture_name_text = models.CharField(max_length=100, blank=True, verbose_name="名称")
    picture = models.ImageField(verbose_name="图片", upload_to='images', blank=True)
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")


class TransInfo(models.Model):
    # ...
    enabled_key = models.IntegerField(default=0, blank=False)
    trans_name_text = models.CharField(max_length=100, verbose_name="交易名称")
    trans_order_number_text = models.CharField(max_length=100, blank=True, verbose_name="订单号")
    contract_name_text = models.CharField(max_length=100, verbose_name="合同编号")
    # 经办人
    contact_key = models.ForeignKey(ContactInfo)
    goods_info = models.ForeignKey(TransGoodsInfo, on_delete=models.CASCADE)
    costs = models.ForeignKey(TransCostInfo)
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
    enabled_key = models.IntegerField(default=0, blank=False)
    trans_key = models.ForeignKey(TransInfo, on_delete=models.CASCADE)
    goods_key = models.ForeignKey(GoodsInfo, blank=True)
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


class TransGoodsPicture(models.Model):
    # ...
    def __str__(self):
        return self.picture_name_text

    trans_goods_info_key = models.ForeignKey(TransGoodsInfo, on_delete=models.CASCADE)
    picture_name_text = models.CharField(max_length=100, blank=True, verbose_name="名称")
    picture = models.ImageField(verbose_name="图片", upload_to='images', blank=True)
    comment_text = models.CharField(max_length=1000, blank=True, verbose_name="备注")


class CostInfo(models.Model):
    # ...
    def __str__(self):
        return self.cost_name_text

    cost_name_text = models.CharField(max_length=100, verbose_name="费用名称")
    cost_price_float = models.FloatField(default=0, verbose_name="价格")


# trans goods cost library, link to trans goods info
class TransGoodsCostInfo(models.Model):
    trans_goods_info_key = models.ForeignKey(TransGoodsInfo, on_delete=models.CASCADE)
    cost_key = models.ForeignKey(CostInfo)


# created for every trans
class TransCostInfo(models.Model):
    trans_info_key = models.ForeignKey(TransInfo, on_delete=models.CASCADE)
    cost_key = models.ForeignKey(CostInfo)

