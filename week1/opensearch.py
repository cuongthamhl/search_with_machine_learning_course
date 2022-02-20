from opensearchpy import OpenSearch

open_search_client = OpenSearch(
    hosts=[{'host': '127.0.0.1', 'port': 9200}],
    http_auth=('admin', 'admin'),
    use_ssl=True,
    verify_certs=False,
)
