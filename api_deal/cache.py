from django.core.cache import cache


def clear_top_cache():
    """
    Отчистка кеша
    """
    all_key = cache.get('all_key')
    if all_key:
        for key in all_key:
            cache.delete(key)

        cache.delete('all_key')


def add_data_top_to_cache(key_cache, list_users):
    """
    Кэшируем данные по ключу
    """
    cache.set(key_cache, list_users)
    all_key = cache.get('all_key')

    # Запоминаем новый ключ
    if not all_key:
        all_key = set()

    all_key.add(key_cache)
    cache.set('all_key', all_key)
