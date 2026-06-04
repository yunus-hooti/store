from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):
    """
    A generator that generates unique slugs for a model
    :param instance:
    :param new_slug:
    :return:
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name, aloow_unicode=True)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{rendstr}".format(
            slug=slug, rendstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def random_string_generator(size=10, chars='abcdefghijklmnopqrstuvwxyz0123456789'):
    import random
    return ''.join(random.choice(chars) for _ in range(size))
