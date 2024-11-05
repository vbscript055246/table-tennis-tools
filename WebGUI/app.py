from flask import Flask, render_template, request, jsonify

import pandas as pd
from seeker import GetNewData, Comparator, Modifier

app = Flask(__name__)

df = {
    'blade' : pd.read_excel('blade_full_data.xlsx', sheet_name='Sheet1'),
    'rubber' : pd.read_excel('rubber_full_data.xlsx', sheet_name='Sheet1'),
    'pips' : pd.read_excel('pips_full_data.xlsx', sheet_name='Sheet1')
}

product_data = {
    'blade': df['blade']['Name'].tolist(),
    'rubber': df['rubber']['Name'].tolist(),
    'pips': df['pips']['Name'].tolist()
}


@app.route('/')
def index():
    return render_template('index.html')


# 當用戶選擇產品類型時，返回對應的產品名稱列表
@app.route('/get_product_names', methods=['GET'])
def get_product_names():
    product_type = request.args.get('product_type')

    if product_type in product_data:
        # 返回對應產品類型的產品名稱列表
        return jsonify(product_data[product_type])
    else:
        # 如果沒有匹配的產品類型，返回空列表
        return jsonify([])


@app.route('/search', methods=['POST'])
def search():
    global df
    request_data = request.get_json()

    product_type = request_data.get('product_type')
    product_name = request_data.get('product_name')

    comparator = Comparator(df[product_type], product_type)
    comparator.apply_mask()

    cdf = comparator.customized_STD(product_name=product_name,option=request_data)
    search_results = Modifier(product_type).do(cdf)
    return jsonify(search_results.to_dict(orient='records'))

if __name__ == '__main__':
    GetNewData('blade', force=False)
    GetNewData('rubber', force=False)
    GetNewData('pips', force=False)

    app.run(port=9487, debug=True, use_reloader=False)
