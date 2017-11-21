from ...models import Provider


def get_providers_list():
    try:
        providers_list = Provider.objects.all()
    except (KeyError, Provider.DoesNotExist):
        providers_list = []

    print(providers_list)

    return providers_list


def get_providers_choices():
    providers_list = get_providers_list();
    providers_choices = []
    for provider in providers_list:
        providers_choices.append((provider.id, provider.name))

    return providers_choices
