from flask import request, jsonify
from flask_restful import Resource
from models import UniqueDetails, PriceHistories, AllSizesView, SizeHistories, Sizes
from add_functions import get_filtered_sorted, get_paginated_list


class UniquesView(Resource):
    def get(self):
        unique_db = UniqueDetails.query
        filtered_sorted = get_filtered_sorted(unique_db, request.args)
        paginate = get_paginated_list(
            filtered_sorted,
            '/uniques')
        return jsonify(paginate)


class UniqueView(Resource):
    def get(self, unique):
        unique = UniqueDetails.query.filter_by(unique_id=unique).one()
        prices_history = PriceHistories.query.filter_by(unique_unique_id=unique.unique_id)
        size_history = SizeHistories.query.filter_by(unique_unique_id=unique.unique_id, avail_avail_id=1).all()
        prices_list = list(x.json() for x in prices_history)
        sizes_list = list(Sizes.query.filter_by(size_id=x.size_size_id).first().json() for x in size_history)
        if unique:
            result = unique.json()
            if len(prices_list) > 0:
                result['old_prices'] = prices_list
            if len(sizes_list) > 0:
                result['sizes'] = sizes_list
            return result
        return {'message': 'unique not found'}, 404


class SizeHistoryView(Resource):
    def get(self, unique):
        unique = SizeHistories.query.filter_by(unique_unique_id=unique).all()
        all_sizes = list(x.json() for x in unique)
        return jsonify(all_sizes)


class SizeHistoryToSize(Resource):
    def get(self, unique):
        size_history = SizeHistories.query.filter_by(unique_unique_id=unique).all()
        all_sizes = []

        for x in size_history:
            all_sizes.append(Sizes.query.filter_by(size_id=x.size_size_id).one().json())
        # all_sizes = list(x.json() for x in unique)
        return jsonify(all_sizes)


class SizesViews(Resource):
    def get(self):
        all_sizes = AllSizesView.query.all()
        all_sizes = list(x.json() for x in all_sizes)
        return jsonify(all_sizes)
