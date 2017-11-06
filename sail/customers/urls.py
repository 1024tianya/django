from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.customer_index, name='customer_index'),

    url(r'^customers/$', views.customer_index, name='customer_index'),
    url(r'^goods/$', views.goods_index, name='goods_index'),
    url(r'^costs/$', views.cost_index, name='cost_index'),
    url(r'^providers/$', views.provider_index, name='provider_index'),

    url(r'^goods/(?P<goods_id>[0-9]+)/{0,1}$', views.edit_goods, name='goods_detail'),
    url(r'^goods/add/$', views.add_goods, name='add_goods'),
    url(r'^goods/edit/(?P<goods_id>[0-9]+)/{0,1}$', views.edit_goods, name='edit_goods'),
    url(r'^goods/del/(?P<goods_id>[0-9]+)/{0,1}$', views.del_goods, name='del_goods'),

    url(r'^providers/add/$', views.add_provider, name='add_provider'),
    url(r'^providers/edit/(?P<provider_id>[0-9]+)/{0,1}$', views.edit_provider, name='edit_provider'),
    url(r'^providers/del/(?P<provider_id>[0-9]+)/{0,1}$', views.del_provider, name='del_provider'),

    url(r'^costs/add/$', views.add_cost, name='add_cost'),
    url(r'^costs/adddirect$', views.add_cost_direct, name='add_costdirect'),
    url(r'^costs/edit/(?P<cost_id>[0-9]+)/{0,1}$', views.edit_cost, name='edit_cost'),
    url(r'^costs/del/(?P<cost_id>[0-9]+)/{0,1}$', views.del_cost, name='del_cost'),

    url(r'^customers/(?P<customer_id>[0-9]+)/{0,1}$', views.customer_detail, name='detail'),
    url(r'^customers/add/{0,1}$', views.add_customer, name='add_customer'),
    url(r'^customers/edit/(?P<customer_id>[0-9]+)/{0,1}$', views.edit_customer, name='edit_customer'),
    url(r'^customers/del/(?P<customer_id>[0-9]+)/{0,1}$', views.del_customer, name='del_customer'),

    url(r'^customers/contact/add/(?P<customer_id>[0-9]+)/{0,1}$', views.add_contact, name='add_contact'),
    url(r'^customers/contact/edit/(?P<contact_id>[0-9]+)/{0,1}$', views.edit_contact, name='edit_contact'),
    url(r'^customers/contact/del/(?P<contact_id>[0-9]+)/{0,1}$', views.del_contact, name='del_contact'),

    url(r'^customers/translist/(?P<customer_id>[0-9]+)/{0,1}$', views.trans_list_of_customer, name='trans_list_of_customer'),
    url(r'^customers/trans/add/(?P<customer_id>[0-9]+)/{0,1}$', views.add_trans, name='add_trans'),
    url(r'^customers/trans/edit/(?P<trans_id>[0-9]+)/{0,1}$', views.edit_trans, name='edit_trans'),
    url(r'^customers/trans/del/(?P<trans_id>[0-9]+)/{0,1}$', views.del_trans, name='del_trans'),
    url(r'^customers/trans/delcost/(?P<trans_cost_id>[0-9]+)/{0,1}$', views.del_trans_cost, name='del_trans_cost'),

    url(r'^customers/transgoods/add/(?P<trans_id>[0-9]+)/{0,1}$', views.add_transgoods, name='add_transgoods'),
    url(r'^customers/transgoods/edit/(?P<transgoods_id>[0-9]+)/{0,1}$', views.edit_transgoods, name='edit_transgoods'),
    url(r'^customers/transgoods/del/(?P<transgoods_id>[0-9]+)/{0,1}$', views.del_transgoods, name='del_transgoods'),
    url(r'^customers/transgoods/delcost/(?P<transgoods_cost_id>[0-9]+)/{0,1}$', views.del_transgoods_cost, name='del_transgoods_cost'),

    url(r'^customers/addpicture/(?P<trans_id>[0-9]+)/{0,1}$', views.add_picture, name='add_picture'),
]
