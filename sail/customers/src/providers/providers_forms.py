#coding=utf-8

from django import forms


class ProviderForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="公司名称")
    address = forms.CharField(max_length=100, required=True, label="地址")
    comment = forms.CharField(max_length=1000, required=False, label="备注",  widget=forms.Textarea())



