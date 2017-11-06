#coding=utf-8

from django import forms
import datetime


class QuickAddTransInfoForm(forms.Form):
    trans_order_number_text = forms.CharField(label="订单号", required=False)
    contact_key = forms.ChoiceField(label="经办人", required=True)
    trans_fax_int = forms.IntegerField(label="税点", required=False, min_value=0, max_value=99, initial=0)
    trans_date = forms.DateField(label="交易日期",
                                 required=True,
                                 initial=datetime.date.today(),
                                 widget=forms.SelectDateWidget())
    goods_delivery_date = forms.DateField(label="交货日期",
                                          required=False,
                                          widget=forms.SelectDateWidget())


class TransInfoForm(forms.Form):
    trans_name_text = forms.CharField(label="交易名称", required=False)
    trans_order_number_text = forms.CharField(label="订单号", required=False)
    contact_key = forms.ChoiceField(label="经办人", required=True)
    trans_fax_int = forms.IntegerField(label="税点", required=False, min_value=0, max_value=99, initial=0)
    trans_date = forms.DateField(label="交易日期",
                                 required=True,
                                 initial=datetime.date.today(),
                                 widget=forms.SelectDateWidget())
    goods_delivery_date = forms.DateField(label="交货日期",
                                          required=False,
                                          widget=forms.SelectDateWidget())
    comment_text = forms.CharField(label="备注", required=False, widget=forms.Textarea())

    def __init__(self, contacts, *args, **kwargs):
        super(TransInfoForm, self).__init__(*args, **kwargs)
        self.fields['contact_key'].choices = contacts


class AddCustomer(forms.Form):
    company_name = forms.CharField(label="公司名称", required=True)
    company_address = forms.CharField(label="公司地址", required=False)
    company_invoice_text = forms.CharField(label="发票抬头", required=False)
    company_comment = forms.CharField(label="备注", required=False, widget=forms.Textarea())


class ContactInfoForm(forms.Form):
    name_text = forms.CharField(max_length=20, required=True, label="姓名")
    address_text = forms.CharField(max_length=100, required=False, label="地址")
    mobile1_text = forms.CharField(max_length=30, required=False, label="工作手机号码")
    mobile2_text = forms.CharField(max_length=30, required=False, label="家庭手机号码")
    phone1_text = forms.CharField(max_length=30, required=False, label="固定电话")
    phone2_text = forms.CharField(max_length=30, required=False, label="固定电话2")
    email = forms.CharField(max_length=30, required=False, label="Email")
    comment_text = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())


class TransInfoForm(forms.Form):
    trans_name_text = forms.CharField(label="交易名称", required=False, initial='')
    trans_order_number_text = forms.CharField(label="订单号", required=False, initial='')
    contract_name_text = forms.CharField(label="合同编号", required=False, initial='')
    #goods_info = forms.ChoiceField(label="货物", required=True)
    trans_handler_name_text = forms.ChoiceField(label="经办人", required=True)
    #trans_total_num_int = forms.IntegerField(label="数量", required=True, min_value=0, initial=0)
    trans_fax_int = forms.IntegerField(label="税点", required=False, min_value=0, max_value=99, initial=0)
    trans_payment_float = forms.FloatField(label="总货款", required=True, min_value=0, initial=0)
    trans_reduction_float = forms.FloatField(label="优惠", required=True, min_value=0, initial=0)
    trans_date = forms.DateField(label="交易日期", required=True, initial=datetime.datetime.now(),
                                 widget=forms.SelectDateWidget())
    trans_delivery_date = forms.DateField(label="交货日期", required=False,
                                          widget=forms.SelectDateWidget())
    comment_text = forms.CharField(label="备注", required=False, widget=forms.Textarea(), initial='')

    def __init__(self, contacts, goods, *args, **kwargs):
        super(TransInfoForm, self).__init__(*args, **kwargs)
        #self.fields['goods_info'].choices = goods
        self.fields['trans_handler_name_text'].choices = contacts


class TransGoodsInfoForm(forms.Form):
    goods_key = forms.ChoiceField(label="货物", required=True)
    num_int = forms.IntegerField(required=False, label="数量", initial=1)
    price_float = forms.IntegerField(required=False, label="成交单价", initial=0)
    price_quoted_float = forms.IntegerField(required=False, label="报价", initial=0)
    goods_color_text = forms.CharField(label="颜色", required=False, initial='')
    comment_text = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())

    def __init__(self, goods, *args, **kwargs):
        super(TransGoodsInfoForm, self).__init__(*args, **kwargs)
        self.fields['goods_key'].choices = goods


class PictureInfo(forms.Form):
    trans_goods_picture_name_text = forms.CharField(max_length=100, required=False, label="名称")
    trans_goods_picture_path_text = forms.CharField(max_length=100, required=True, label="图片路径名")


# goods forms
class GoodsInfoForm(forms.Form):
    goods_provider = forms.ChoiceField(label="供应商", required=True)
    goods_name_text = forms.CharField(max_length=100, required=True, label="货物名称")
    goods_cost_float = forms.FloatField(required=True, initial=0, label="进货价")
    goods_price_float = forms.FloatField(required=True, initial=0, label="价格")
    comment_text = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())

    def __init__(self, providers, *args, **kwargs):
        super(GoodsInfoForm, self).__init__(*args, **kwargs)
        self.fields['goods_provider'].choices = providers


# ProviderInfo forms
class ProviderInfoForm(forms.Form):
    company_name_text = forms.CharField(max_length=100, required=True, label="公司名称")
    company_address_text = forms.CharField(max_length=100, required=True, label="地址")
    comment_text = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())


# CostInfo forms
class CostInfoForm(forms.Form):
    cost_name_text = forms.CharField(max_length=100, required=True, label="费用名称")
    cost_price_float = forms.FloatField(required=True, initial=0.0, label="价格")

