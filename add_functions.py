from flask import abort, request
from models import UniqueDetails, SizeHistories
from sqlalchemy import or_


def get_paginated_list(results, url):
    result_list = list(x.json() for x in results['results'])
    offset = int(results.get('offset'))
    limit = int(results.get('limit'))
    count = len(result_list)
    if count < offset:
        abort(404)
    # make response
    results['count'] = count
    # make URLs
    # make previous url
    if offset == 1:
        results['previous'] = ''
    else:
        start_copy = max(1, offset - limit)
        results['previous'] = url + '?offset=%d' % start_copy
        for arg in results.get('args'):
            results['previous'] += '&%s=%s' % (arg, results.get(arg))
    # make next url
    if offset + limit > count:
        results['next'] = ''
    else:
        start_copy = offset + limit
        results['next'] = url + '?offset=%d' % start_copy
        for arg in results.get('args'):
            results['next'] += '&%s=%s' % (arg, results.get(arg))
    # finally extract result according to bounds
    results['results'] = result_list[(offset - 1):(offset - 1 + limit)]
    results.pop('args')
    return results


def get_filtered_sorted(results, arguments):
    limit = int(arguments.get('limit', 200))
    if limit < 0:
        abort(404)
    elif limit < 5 or 2000 < limit:
        limit = 200

    params = {'offset': arguments.get('offset', 1), 'limit': limit, 'args': ['limit']}

    # filtering
    if request.args.get('site'):
        results = results.filter(UniqueDetails.site_name.ilike(request.args.get('site')))
        params['site'] = request.args.get('site')
        params['args'].append('site')
    if request.args.get('brand'):
        brands = request.args.get('brand').split(';')
        results = results.filter(or_(*[UniqueDetails.brand_name.ilike('%' + name + '%') for name in brands]))
        params['brand'] = request.args.get('brand')
        params['args'].append('brand')
    if request.args.get('sizes'):
        sizes = tuple(request.args.get('sizes').split(';'))
        results = results.filter(UniqueDetails.sizes.any(SizeHistories.size_size_id.in_(sizes)))
        params['sizes'] = request.args.get('sizes')
        params['args'].append('sizes')

    # ordering
    if request.args.get('all') and request.args.get('all') == 'y':
        results = results.order_by(UniqueDetails.unique_id)
        params['all'] = 'y'
        params['args'].append('all')
    else:
        results = results.order_by(UniqueDetails.first_to_show.desc())
    order = request.args.get('order', 'mod_site_uniq')
    if order != 'mod_site_uniq':
        params['order'] = order
        params['args'].append('order')
    order_nav = request.args.get('nav', 'desc')
    params['nav'] = order_nav
    params['args'].append('nav')

    # final result
    order_attr = getattr(UniqueDetails, order)
    order_naved = getattr(order_attr, order_nav)
    results = results.order_by(order_naved())

    params['results'] = results
    return params
