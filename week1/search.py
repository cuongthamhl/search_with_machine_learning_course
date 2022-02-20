import json
import config
#
# The main search hooks for the Search Flask application.
#
from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from urllib.parse import urlparse
from urllib.parse import urlencode

from week1.opensearch import open_search_client

bp = Blueprint('search', __name__, url_prefix='/search')


# Our main query route
@bp.route('/query', methods=['GET', 'POST'])
def query():

    error = None
    es_query = None
    es_query = create_query(request.args)

    print(json.dumps(es_query))

    response = open_search_client.search(es_query, index=config.PRODUCT_INDEX)

    if error is None:
        return render_template(
            "search_results.jinja2",
            query=request.args.get('query', ''),
            search_response=response,
            display_filters=None, applied_filters="",
            sort=None, sortDir=None)
    else:
        redirect(url_for("index"))


def create_query(query_params: dict):
    search_phrase = query_params.get('query', '')
    sort = query_params.get('sort', '_score')
    sort_dir = query_params.get('sortDir', 'DESC')

    if sort == 'name':
        sort_query = {"name.keyword": {"order": sort_dir}}
    elif sort == 'popularity':
        sort_query = {"salesRankShortTerm": {"order": sort_dir}}
    elif sort == 'price':
        sort_query = {"regularPrice": {"order": sort_dir}}
    else:
        sort_query = {"_score": {"order": sort_dir}}

    base_search_query = {
        "multi_match": {
            "query": search_phrase,
            "fields": ["name^1000", "shortDescription^50", "longDescription^10", "department"]
        }
    }

    if len(search_phrase) == 0:
        base_search_query = {
            "match_all": {}
        }

    shared_boolean_filter_query = {
        "bool": {
            "filter": []
        }
    }

    # shared filters that will be applied to both aggregations and post_filters
    # aggregations: left navigation
    # post_filters: search results on the right
    shared_filters = []

    price_filter_query = {}
    if 'filter.Price' in query_params:
        price_param = query_params.get('filter.Price')
        min = 0
        max = 9999999

        # not very clean, but for quick turnaround
        if price_param == '*-100.0':
            min = 0
            max = 99.99
        elif price_param == '100.0-200.0':
            min = 100
            max = 199.99
        elif price_param == '200.0-*':
            min = 200
            max = 9999

        price_filter_query['range'] = {}
        price_filter_query['range']['regularPrice'] = {
            'gte': min,
            'lt': max
        }

    if len(price_filter_query) > 0:
        shared_filters.append(price_filter_query)

    department_filter_query = {}
    if 'filter.Departments' in query_params:
        param = query_params.get('filter.Departments')
        if len(param) > 0:
            department_filter_query['term'] = {}
            department_filter_query['term']['department.department'] = param

    if len(department_filter_query) > 0:
        shared_filters.append(department_filter_query)

    shared_boolean_filter_query['bool']['filter'] = shared_filters

    aggs = {
        "Departments": {
            "filter": shared_boolean_filter_query,
            "aggs": {
                "buckets": {
                    "terms": {
                        "field": "department.department"

                    }
                }
            }
        },
        "Price": {
            "filter": shared_boolean_filter_query,
            "aggs": {
                "buckets": {
                    "range": {
                        "field": "regularPrice",
                        "ranges": [
                            {"to": 100.0},
                            {"from": 100.0, "to": 200.0},
                            {"from": 200.0}
                        ]
                    }
                }
            }
        },
        "Images": {
            "filter": {
                "match_all": {}
            },
            "aggs": {
                "buckets": {
                    "missing": {
                        "field": "image.keyword"
                    }
                }
            }
        }

    }

    filtered_aggs = {
        "filtered_aggs": {
            "filters": {
                "filters": []
            }
        }
    }

    main_es_query = {
        'size': 10,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": base_search_query,
                        # "should": [
                        #     {
                        #        # TODO: boost quality signals

                        #     }
                        # ]
                    }
                },
                "boost_mode": "replace",
                "score_mode": "avg",
                "functions": [
                    {
                        "field_value_factor": {
                            "field": "salesRankLongTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    },
                    {
                        "field_value_factor": {
                            "field": "salesRankMediumTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    },
                    {
                        "field_value_factor": {
                            "field": "salesRankShortTerm",
                            "missing": 100000000,
                            "modifier": "reciprocal"
                        }
                    },
                ]
            }
        },
        "aggs": aggs
    }

    if len(shared_filters) > 0:
        main_es_query['post_filter'] = {
            "bool": {
                "filter": shared_filters
            }
        }

    main_es_query["sort"] = sort_query

    return main_es_query


@bp.app_template_filter('first_elem_or_default')
def first_elem_or_default(input, default):
    if len(input) > 0:
        return input[0]
    else:
        return default


def update_query_param(key, value):
    # Bad example, not clean code
    qs = request.args.copy()
    if len(value) > 0:
        qs[key] = value
    else:
        qs.pop(key, None)
    return urlencode(qs)
