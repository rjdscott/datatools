from flask import Flask, send_file
from flask_restful import Resource, Api
from api.resources import asset_prices as ap
# from api.resources import asset_prices as ap

import io

app = Flask(__name__)
api = Api(app)


class AssetPrices(Resource):
    def get(self, ticker):
        prices_message = ap.get_asset_prices(ticker, '../data/etl.parquet', 'bytes')
        return send_file(
            io.BytesIO(prices_message),
            as_attachment=True,
            attachment_filename='abc.abc',
            mimetype='attachment/x-protobuf')


api.add_resource(AssetPrices, '/<string:ticker>')

if __name__ == '__main__':
    app.run(debug=True)
