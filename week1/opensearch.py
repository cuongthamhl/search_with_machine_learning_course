from flask import current_app, g
from opensearchpy import OpenSearch

# Create an OpenSearch client instance and put it into Flask shared space for use by the application

open_search_client = OpenSearch(
            hosts=[{'host': '127.0.0.1', 'port': 9200}],        
            http_auth = ('admin', 'admin'),
            use_ssl = True,
            verify_certs = False,
          
)

def get_opensearch():
    if 'opensearch' not in g:
        # Implement a client connection to OpenSearch so that the rest of the application can communicate with OpenSearch
        
        g.opensearch = open_search_client

    return g.opensearch
