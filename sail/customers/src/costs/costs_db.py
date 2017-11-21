from ...models import Cost


def get_costs_list():
    try:
        costs_list = Cost.objects.all()
    except (KeyError, Cost.DoesNotExist):
        costs_list = []

    return costs_list

