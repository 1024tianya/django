from ...models import Customer, Contact, Trans


def get_customers_list():
    try:
        # TODO: limit count of db search
        customers_list = Customer.objects.all()
    except (KeyError, Customer.DoesNotExist):
        customers_list = []

    customer_info_list = []
    for customer in customers_list:
        try:
            contacts = customer.contacts.all()
        except (KeyError, Contact.DoesNotExist):
            contacts = []

        try:
            trans = customer.trans.all()
        except (KeyError, Trans.DoesNotExist):
            trans = []

        trans_count = len(trans)
        if trans_count > 0:
            latest_trans = trans.latest('add_date')
        else:
            latest_trans = None

        customer_info = {
            'customer': customer,
            'contacts': contacts,
            'trans_count': trans_count,
            'latest_trans': latest_trans,
        }

        customer_info_list.append(customer_info)

    return customer_info_list


def get_customer_with_contacts(customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except (KeyError, Customer.DoesNotExist):
        return None

    try:
        contacts = customer.contacts.all()
    except (KeyError, Contact.DoesNotExist):
        contacts = []

    customer_info = {
        'customer': customer,
        'contacts': contacts,
    }

    return customer_info
