#coding=utf-8

from django import forms


class CostForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="费用名称")
    price = forms.FloatField(required=True, initial=0.0, label="价格")

