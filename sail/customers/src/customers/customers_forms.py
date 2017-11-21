#coding=utf-8

from django import forms


class CustomerForm(forms.Form):
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




