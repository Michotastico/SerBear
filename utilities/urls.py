from utilities.exceptions import MalformedUrl


def check_url(url_path):
    if not url_path.startswith('/'):
        raise MalformedUrl(url_path)


def _join_url_paths(base, tail):
    final_url = '/{}'
    if base.startswith('/'):
        final_url = base
    else:
        final_url = final_url.format(base)

    if not final_url.endswith('/'):
        final_url += '/'

    final_tail = tail
    if final_tail.startswith('/'):
        final_tail = final_tail[1:]

    return '{}{}'.format(final_url, final_tail)


def url(path_url, handler):
    return [(path_url, handler)]


def include_url_group(basal_path_url, urls):
    processed_urls = map(
        lambda _url: (_join_url_paths(basal_path_url, _url[0]), _url[1]),
        urls
    )
    return list(processed_urls)


def url_group(*urls):
    group = list()
    for url_set in urls:
        group.extend(url_set)
    return group
