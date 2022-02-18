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

from week1.opensearch import get_opensearch

bp = Blueprint('search', __name__, url_prefix='/search')

sortable_fields = {
    "_score": "Relevance",
    "name.keyword": "Name",
    "salesRankShortTerm": "Popularity",
    "regularPrice": "Price"
}

# Process the filters requested by the user and return a tuple that is appropriate for use in: the query, URLs displaying the filter and the display of the applied filters
# filters -- convert the URL GET structure into an OpenSearch filter query
# display_filters -- return an array of filters that are applied that is appropriate for display
# applied_filters -- return a String that is appropriate for inclusion in a URL as part of a query string.  This is basically the same as the input query string


def process_filters(filters_input):
    # Filters look like: &filter.name=regularPrice&regularPrice.key={{ agg.key }}&regularPrice.from={{ agg.from }}&regularPrice.to={{ agg.to }}
    filters = []
    # Also create the text we will use to display the filters that are applied
    display_filters = []
    applied_filters = ""
    for filter in filters_input:
        type = request.args.get(filter + ".type")
        display_name = request.args.get(filter + ".displayName", filter)
        #
        # We need to capture and return what filters are already applied so they can be automatically added to any existing links we display in aggregations.jinja2
        applied_filters += "&filter.name={}&{}.type={}&{}.displayName={}".format(filter, filter, type, filter,
                                                                                 display_name)
        # TODO: IMPLEMENT AND SET filters, display_filters and applied_filters.
        # filters get used in create_query below.  display_filters gets used by display_filters.jinja2 and applied_filters gets used by aggregations.jinja2 (and any other links that would execute a search.)
        if type == "range":
            pass
        elif type == "terms":
            pass  # TODO: IMPLEMENT
    print("Filters: {}".format(filters))

    return filters, display_filters, applied_filters


# Our main query route.  Accepts POST (via the Search box) and GETs via the clicks on aggregations/facets
@bp.route('/query', methods=['GET', 'POST'])
def query():
    # Load up our OpenSearch client from the opensearch.py file.
    opensearch = get_opensearch()
    # Put in your code to query opensearch.  Set error as appropriate.
    error = None
    user_query = None
    query_obj = None
    display_filters = None
    applied_filters = ""
    filters = None
    sort = "_score"
    sortDir = "desc"
    
    # elif request.method == 'GET':  # Handle the case where there is no query or just loading the page
    user_query = request.args.get("query", "")
    filters_input = request.args.getlist("filter.name", [])
    sort = request.args.get("sort", sort)
    sortDir = request.args.get("sortDir", sortDir)

    (filters, display_filters, applied_filters) = process_filters(filters_input)
    query_obj = create_query(user_query, filters, sort, sortDir)

    print("query obj: {}".format(query_obj))
    # TODO: Replace me with an appropriate call to OpenSearch
    response = opensearch.search(query_obj, index=config.PRODUCT_INDEX)
    # Postprocess results here if you so desire

    # print(response)
    if error is None:
        return render_template(
            "search_results.jinja2", query=user_query, search_response=response,
            display_filters=display_filters, applied_filters=applied_filters,
            sort=sort, sortDir=sortDir, sortable_fields=sortable_fields)
    else:
        redirect(url_for("index"))


def create_query(user_query, filters, sort="_score", sort_dir="desc"):
    print("Query: {} Filters: {} Sort: {}".format(user_query, filters, sort))

    if sort == 'name':
        sort_query = {"name.keyword": {"order": sort_dir}}
    elif sort == 'popularity':
        sort_query = {"salesRankShortTerm": {"order": sort_dir}}
    elif sort == 'price':
        sort_query = {"regularPrice": {"order": sort_dir}}
    else:
        sort_query = {"_score": {"order": sort_dir}}

    aggs = {
        "Departments": {
            "terms": {
                "field": "department.department"
            }
        },
        "Price": {
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

    if len(user_query) == 0:
        query_obj = {
            'size': 10,
            "query": {
                "match_all": {

                }
            },
            "aggs": aggs

        }
    else:
        query_obj = {
            'size': 10,
            "query": {
                "match": {
                    "name": user_query
                }
            },
            "aggs": aggs
        }
    query_obj["sort"] = sort_query
    print(json.dumps(query_obj))
    return query_obj

def update_query_param(key, value):
    # Bad example, not clean code
    qs = request.args.copy()
    qs[key] = value
    return urlencode(qs)