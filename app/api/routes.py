from flask import Blueprint, request, jsonify
from .controllers import (
    get_all_products,
    get_products_by_supplier,
    get_suppliers_by_product,
    get_products_by_category,
    get_monthly_revenue_by_store,
    get_yearly_revenue_by_store,
    get_revenue_by_date_range,
    get_carriers_usage_count,
    get_category_with_most_items,
    get_products_below_min_quantity,
    get_product_movement_history,
    get_products_more_than_days_in_stock,
    get_most_active_suppliers,
    get_most_sold_product_in_period,
    get_supplier_delivery_details,
    get_total_products_by_carrier,
    get_recently_added_products,
    get_product_with_longest_stock_duration,
    get_sales_performance_by_category
)

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/products', methods=['GET'])
def products():
    return jsonify(get_all_products())

@api_bp.route('/products/supplier/<int:supplier_id>', methods=['GET'])
def products_by_supplier(supplier_id):
    return jsonify(get_products_by_supplier(supplier_id))

@api_bp.route('/suppliers/product/<int:product_id>', methods=['GET'])
def suppliers_by_product(product_id):
    return jsonify(get_suppliers_by_product(product_id))

@api_bp.route('/products/category/<int:category_id>', methods=['GET'])
def products_by_category(category_id):
    return jsonify(get_products_by_category(category_id))

@api_bp.route('/revenue/monthly', methods=['GET'])
def monthly_revenue_by_store():
    return jsonify(get_monthly_revenue_by_store())

@api_bp.route('/revenue/yearly', methods=['GET'])
def yearly_revenue_by_store():
    return jsonify(get_yearly_revenue_by_store())

@api_bp.route('/revenue/date-range', methods=['GET'])
def revenue_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return jsonify(get_revenue_by_date_range(start_date, end_date))

@api_bp.route('/carriers/usage', methods=['GET'])
def carriers_usage_count():
    return jsonify(get_carriers_usage_count())

@api_bp.route('/categories/top', methods=['GET'])
def category_with_most_items():
    return jsonify(get_category_with_most_items())

@api_bp.route('/products/above-minimum', methods=['GET'])
def products_above_min_quantity():
    return jsonify(get_products_below_min_quantity())

@api_bp.route('/product/<int:product_id>/history', methods=['GET'])
def product_movement_history(product_id):
    return jsonify(get_product_movement_history(product_id))

@api_bp.route('/products/stock-duration', methods=['GET'])
def products_more_than_days_in_stock():
    days = request.args.get('days', default=30, type=int)
    return jsonify(get_products_more_than_days_in_stock(days))

@api_bp.route('/suppliers/active', methods=['GET'])
def most_active_suppliers():
    return jsonify(get_most_active_suppliers())

@api_bp.route('/product/most-sold', methods=['GET'])
def most_sold_product_in_period():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return jsonify(get_most_sold_product_in_period(start_date, end_date))

@api_bp.route('/suppliers/average-delivery-time', methods=['GET'])
def average_delivery_time_per_supplier():
    return jsonify(get_supplier_delivery_details())

@api_bp.route('/carriers/total-products', methods=['GET'])
def total_products_by_carrier():
    return jsonify(get_total_products_by_carrier())

@api_bp.route('/products/recently-added', methods=['GET'])
def recently_added_products():
    return jsonify(get_recently_added_products())

@api_bp.route('/product/longest-stock-duration', methods=['GET'])
def product_with_longest_stock_duration():
    return jsonify(get_product_with_longest_stock_duration())

@api_bp.route('/sales/performance/category', methods=['GET'])
def sales_performance_by_category():
    return jsonify(get_sales_performance_by_category())
