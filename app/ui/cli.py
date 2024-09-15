# app/ui/cli.py
import click
from app.api.controllers import (
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

@click.command()
@click.option('--supplier-id', default=None, help='ID do fornecedor para listar produtos.')
@click.option('--product-id', default=None, help='ID do produto para listar fornecedores.')
@click.option('--category-id', default=None, help='ID da categoria para listar produtos.')
@click.option('--start-date', default=None, help='Data de início para o intervalo de faturamento.')
@click.option('--end-date', default=None, help='Data de término para o intervalo de faturamento.')
@click.option('--days', default=None, help='Número de dias para listar produtos com mais de X dias no estoque.')
@click.option('--store', default=None, help='Nome da loja para calcular faturamento mensal.')
@click.option('--supplier-id-revenue', default=None, help='ID do fornecedor para calcular o tempo médio de entrega.')
@click.option('--product-id-movement', default=None, help='ID do produto para listar histórico de movimentação.')
@click.option('--min-quantity', default=None, help='Quantidade mínima para listar produtos acima da quantidade mínima.')
@click.option('--period-start', default=None, help='Data de início do período para o produto mais vendido.')
@click.option('--period-end', default=None, help='Data de término do período para o produto mais vendido.')
def cli(supplier_id, product_id, category_id, start_date, end_date, days, store, supplier_id_revenue, product_id_movement, min_quantity, period_start, period_end):
    if supplier_id:
        products = get_products_by_supplier(supplier_id)
        for product in products:
            print(product)
    elif product_id:
        suppliers = get_suppliers_by_product(product_id)
        for supplier in suppliers:
            print(supplier)
    elif category_id:
        products = get_products_by_category(category_id)
        for product in products:
            print(product)
    elif start_date and end_date:
        revenue = get_revenue_by_date_range(start_date, end_date)
        for record in revenue:
            print(record)
    elif days:
        products = get_products_more_than_days_in_stock(days)
        for product in products:
            print(product)
    elif store:
        monthly_revenue = get_monthly_revenue_by_store(store)
        print(monthly_revenue)
    elif supplier_id_revenue:
        avg_delivery_time = get_supplier_delivery_details(supplier_id_revenue)
        print(avg_delivery_time)
    elif product_id_movement:
        movement_history = get_product_movement_history(product_id_movement)
        for history in movement_history:
            print(history)
    elif min_quantity:
        products = get_products_below_min_quantity(min_quantity)
        for product in products:
            print(product)
    elif period_start and period_end:
        most_sold_product = get_most_sold_product_in_period(period_start, period_end)
        print(most_sold_product)
    else:
        products = get_all_products()
        for product in products:
            print(product)

if __name__ == '__main__':
    cli()
