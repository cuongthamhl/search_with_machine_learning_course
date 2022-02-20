# WARNING: this will silently delete all of your indexes

curl -k -X DELETE -u $ES_CREDS  "https://localhost:9200/bbuy_products"
curl -k -X DELETE -u $ES_CREDS  "https://localhost:9200/bbuy_queries"
curl -k -X DELETE -u $ES_CREDS  "https://localhost:9200/bbuy_annotations"
