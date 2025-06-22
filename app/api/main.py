from flask import Flask
from flask import request
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel
import pandas as pd
import numpy as np
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

client = MilvusClient("../../dados/milvus_demo.db")
model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)
df = pd.read_parquet('../../dados/articles2.parquet')


@app.route("/api/articles")
def get_articles():
    query_text = request.args.get('query')
    query_vectors = model.encode([query_text], batch_size=12, max_length=1024, return_dense=True, return_sparse=False, return_colbert_vecs=False)['dense_vecs']

    res = client.search(
        collection_name="demo_collection",  # target collection
        data=query_vectors,  # query vectors
        limit=10,  # number of returned entities
        output_fields=["id"],  # specifies fields to be returned
    )

    ids = [x['id'] for x in res[0]]
    data = df.loc[ids].to_dict('records')
    result = []
    for row in data:
        row['keywords'] = row['keywords'].tolist()
        row['authors'] = row['authors'].tolist()
        result.append(row)
    return result

def proccess_value(value):
    if value is np.ndarray:
        return value.tolist()
    return value