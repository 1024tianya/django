#coding=utf-8

from django import forms


class GoodsForm(forms.Form):
    goods_provider = forms.ChoiceField(label="供应商", required=True)
    name = forms.CharField(max_length=100, required=True, label="货物名称")
    buying_price = forms.FloatField(required=True, initial=0, label="进货价")
    price = forms.FloatField(required=True, initial=0, label="价格")
    comment = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())

    def __init__(self, providers, *args, **kwargs):
        super(GoodsForm, self).__init__(*args, **kwargs)
        self.fields['goods_provider'].choices = providers


class PictureInfo(forms.Form):
    trans_goods_picture_name_text = forms.CharField(max_length=100, required=False, label="名称")
    trans_goods_picture_path_text = forms.CharField(max_length=100, required=True, label="图片路径名")