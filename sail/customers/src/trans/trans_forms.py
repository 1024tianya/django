#coding=utf-8

from django import forms


class TransForm(forms.Form):
    company_name = forms.CharField(label="公司名称", required=True)
    company_address = forms.CharField(label="公司地址", required=False)
    company_invoice_text = forms.CharField(label="发票抬头", required=False)
    company_comment = forms.CharField(label="备注", required=False, widget=forms.Textarea())


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

