from django.conf.urls import url

from . import views
from .src.customers import customers_views
from .src.providers import providers_views
from .src.goods import goods_views
from .src.costs import costs_views


urlpatterns = [
    url(r'^$', views.base_index, name='base_index'),

    url(r'^customers/$', customers_views.customer_index, name='customer_index'),
    url(r'^customers/customers_list$', customers_views.customer_list, name='customers_list'),
    url(r'^customers/(?P<customer_id>[0-9]+)/{0,1}$', customers_views.customer_info, name='customer_info'),
    url(r'^customers/add/$', customers_views.customer_add, name='customer_add'),
    url(r'^customers/edit/(?P<customer_id>[0-9]+)/{0,1}$', customers_views.customer_edit, name='customer_edit'),
    url(r'^customers/del/(?P<customer_id>[0-9]+)/{0,1}$', customers_views.customer_del, name='customer_del'),

    # contacts of customer
    url(r'^customers/contact/(?P<contact_id>[0-9]+)/{0,1}$', views.contact_info, name='contact_info'),
    url(r'^customers/contact/add/(?P<customer_id>[0-9]+)/{0,1}$', views.contact_add, name='contact_add'),
    url(r'^customers/contact/edit/(?P<contact_id>[0-9]+)/{0,1}$', views.contact_edit, name='contact_edit'),
    url(r'^customers/contact/del/(?P<contact_id>[0-9]+)/{0,1}$', views.contact_del, name='contact_del'),

    # query condition added in request info.
    url(r'^trans/$', views.trans_list, name='trans_list'),
    url(r'^trans/add/(?P<customer_id>[0-9]+)/{0,1}$', views.trans_add, name='add_trans'),
    url(r'^trans/edit/(?P<trans_id>[0-9]+)/{0,1}$', views.trans_edit, name='edit_trans'),
    url(r'^trans/del/(?P<trans_id>[0-9]+)/{0,1}$', views.trans_del, name='del_trans'),

    # query condition added in request info.
    url(r'^trans_goods/$', views.trans_goods_list, name='trans_goods_list'),
    url(r'^trans_goods/add/(?P<trans_id>[0-9]+)/{0,1}$', views.trans_goods_add, name='trans_goods_add'),
    url(r'^trans_goods/edit/(?P<trans_goods_id>[0-9]+)/{0,1}$', views.trans_goods_edit, name='trans_goods_edit'),
    url(r'^trans_goods/del/(?P<trans_goods_id>[0-9]+)/{0,1}$', views.trans_goods_del, name='trans_goods_del'),

    url(r'^providers/$', providers_views.provider_index, name='provider_index'),
    url(r'^providers/(?P<provider_id>[0-9]+)/{0,1}$', providers_views.provider_info, name='provider_info'),
    url(r'^providers/add/$', providers_views.provider_add, name='provider_add'),
    url(r'^providers/edit/(?P<provider_id>[0-9]+)/{0,1}$', providers_views.provider_edit, name='provider_edit'),
    url(r'^providers/del/(?P<provider_id>[0-9]+)/{0,1}$', providers_views.provider_del, name='provider_del'),

    url(r'^goods/$', goods_views.goods_index, name='goods_index'),
    url(r'^goods/(?P<goods_id>[0-9]+)/{0,1}$', goods_views.goods_info, name='goods_info'),
    url(r'^goods/add/{0,1}$', goods_views.goods_add, name='goods_add'),
    url(r'^goods/edit/(?P<goods_id>[0-9]+)/{0,1}$', goods_views.goods_edit, name='goods_edit'),
    url(r'^goods/del/(?P<goods_id>[0-9]+)/{0,1}$', goods_views.goods_del, name='goods_del'),

    url(r'^costs/$', costs_views.cost_index, name='cost_index'),
    url(r'^costs/add/{0,1}$', costs_views.cost_add, name='cost_add'),
    url(r'^costs/edit/(?P<cost_id>[0-9]+)/{0,1}$', costs_views.cost_edit, name='cost_edit'),
    url(r'^costs/del/(?P<cost_id>[0-9]+)/{0,1}$', costs_views.cost_del, name='cost_del'),

    # condition added in request url
    url(r'^goods/upload_image/$', views.image_upload, name='image_upload'),
]
