from tkinter import Tk, ttk,Label, Button, Entry, StringVar, Frame, Listbox, OptionMenu, Toplevel, Scrollbar, Canvas, VERTICAL, RIGHT, Y, LEFT, BOTH, BOTTOM
from app.api.controllers import (
    get_all_products,
    get_products_by_supplier,
    get_suppliers_by_product,
    get_products_by_category,
    get_monthly_revenue_by_store,
    get_yearly_revenue_by_store,
    get_revenue_by_date_range,
    get_most_used_carriers,
    get_categories_item_count,
    get_products_below_min_quantity,
    get_product_movement_history,
    get_products_more_than_days_in_stock,
    get_most_active_suppliers,
    get_most_sold_product_in_period,
    get_supplier_delivery_details,
    get_total_products_by_carrier,
    get_recently_added_products,
    get_product_with_longest_stock_duration,
    get_sales_performance_by_category,
    add_product,
    delete_product,
    get_category_id,
    add_fornecedor,
    delete_fornecedor,
    add_categoria,
    delete_categoria,
    get_all_fornecedores,
    get_all_categorias,
    registrar_entrada,
    registrar_saida,
    get_all_stores,
    get_current_inventory
)
from tkinter import Tk, ttk, Label, Button, Entry, StringVar, Frame, Listbox, OptionMenu, Toplevel, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH

def create_main_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(expand=True, fill="both")

    blocks = [
        "Produtos", "Fornecedor", "Categorias",
        "Transportadoras", "Estoque", "Vendas"
    ]

    for i, block in enumerate(blocks):
        button = ttk.Button(main_frame, text=block, command=lambda b=block: create_block_page(root, b))
        button.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

    for i in range(3):
        main_frame.columnconfigure(i, weight=1)
    for i in range(3):
        main_frame.rowconfigure(i, weight=1)


def create_block_page(root, block_name):
    for widget in root.winfo_children():
        widget.destroy()

    frame = ttk.Frame(root, padding="10")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text=f"{block_name}", font=("Arial", 18)).pack(pady=20)

    left_frame = ttk.Frame(frame)
    left_frame.pack(side=LEFT, fill=Y, padx=(0, 10))

    right_frame = ttk.Frame(frame)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    result_listbox = Listbox(right_frame, width=80, height=20)
    result_listbox.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(right_frame, orient=VERTICAL)
    scrollbar.config(command=result_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    result_listbox.config(yscrollcommand=scrollbar.set)

    if block_name == "Produtos":
        create_products_page(left_frame, result_listbox)
    elif block_name == "Fornecedor":
        create_supplier_page(left_frame, result_listbox)
    elif block_name == "Categorias":
        create_categories_page(left_frame, result_listbox)
    elif block_name == "Transportadoras":
        create_carriers_page(left_frame, result_listbox)
    elif block_name == "Estoque":
        create_inventory_page(left_frame, result_listbox)
    elif block_name == "Vendas":
        create_sales_page(left_frame, result_listbox)


    back_button = ttk.Button(frame, text="Voltar", command=lambda: create_main_window(root))
    back_button.pack(side=BOTTOM, pady=20)



def show_results(listbox, results):
    listbox.delete(0, 'end')
    for result in results:
        listbox.insert('end', result)


def create_products_page(frame, result_listbox):
    buttons = [
        ("Listar produtos", lambda: show_results(result_listbox, get_all_products())),
        ("Produtos por fornecedor", lambda: handle_get_products_by_supplier(result_listbox)),
        ("Produtos por categoria", lambda: handle_get_products_by_category(result_listbox)),
        ("Histórico de movimentação de produto", lambda: handle_get_product_movement_history(result_listbox)),
        ("Adicionar produto", lambda: handle_add_product(result_listbox)),
        ("Deletar produto", lambda: handle_delete_product(result_listbox)),
        ("Registrar saída", lambda: handle_registrar_saida(result_listbox)),
        ("Registrar entrada", lambda: handle_registrar_entrada(result_listbox)),
        ("Produtos recentemente adicionados", lambda: show_results(result_listbox, get_recently_added_products()))
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)

def create_supplier_page(frame, result_listbox):
    buttons = [
        ("Adicionar fornecedor", lambda: handle_add_fornecedor(result_listbox)),
        ("Deletar fornecedor", lambda: handle_delete_fornecedor(result_listbox)),
        ("Listar fornecedores", lambda: handle_list_fornecedores(result_listbox)),
        ("Listar fornecedores por produto", lambda: handle_get_suppliers_by_product(result_listbox)),
        ("Listar fornecedores mais ativos", lambda: handle_get_most_active_suppliers(result_listbox)),
        ("Tempo médio de entrega por fornecedor", lambda: handle_get_average_delivery_time(result_listbox))
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)

def create_categories_page(frame, result_listbox):
    buttons = [
        ("Adicionar categoria", lambda: handle_add_categoria(result_listbox)),
        ("Deletar categoria", lambda: handle_delete_categoria(result_listbox)),
        ("Listar categorias", lambda: handle_list_categorias(result_listbox)),
        ("Análise de categorias", lambda: handle_categories_item_count(result_listbox))
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)

def create_carriers_page(frame, result_listbox):
    buttons = [
        ("Análise detalhada de transportadoras", lambda: handle_detailed_carriers_analysis(result_listbox)),
        ("Total de produtos por transportadora", lambda: handle_get_total_products_by_carrier(result_listbox))
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)


def create_inventory_page(frame, result_listbox):
    buttons = [
        ("Listar estoque", lambda: handle_list_inventory(result_listbox)),
        ("Produtos com mais de x dias no estoque", lambda: handle_get_products_more_than_days_in_stock(result_listbox)),
        ("Produtos com maior tempo de estoque", lambda: handle_get_product_with_longest_stock_duration(result_listbox)),
        ("Listar produtos abaixo da quantidade mínima", lambda: show_results(result_listbox, get_products_below_min_quantity()))
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)


def create_sales_page(frame, result_listbox):
    buttons = [
        ("Faturamento mensal por loja", lambda: handle_get_monthly_revenue_by_store(result_listbox)),
        ("Faturamento por intervalo", lambda: handle_get_revenue_by_date_range(result_listbox)),
        ("Produto mais vendido em período", lambda: handle_get_most_sold_product_in_period(result_listbox)),
        ("Desempenho de vendas por categorias", lambda: handle_get_sales_performance_by_category(result_listbox)),
    ]
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command).pack(pady=5)


def show_products():
    """
    Exibe uma lista de todos os produtos usando uma interface gráfica.
    """
    root = Tk()
    root.title("Lista de Produtos")

    # Cria a lista de produtos
    listbox = Listbox(root, width=100, height=20)
    listbox.pack(padx=10, pady=10, side='left')

    # Adiciona a barra de rolagem
    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox.config(yscrollcommand=scrollbar.set)

    # Obtém todos os produtos e adiciona à lista
    products = get_all_products()
    for product in products:
        listbox.insert('end', product)

    root.mainloop()


def show_results(listbox, results):
    listbox.delete(0, 'end')
    for result in results:
        listbox.insert('end', result)


def handle_get_all_products(result_listbox):
    products = get_all_products()
    show_results(result_listbox, products)

def handle_list_fornecedores(result_listbox):
    fornecedores = get_all_fornecedores()
    formatted_fornecedores = [f"ID: {f[0]}, Nome: {f[1]}, CNPJ: {f[2]}, Contato: {f[3]}" for f in fornecedores]
    show_results(result_listbox, formatted_fornecedores)

def handle_list_categorias(result_listbox):
    categorias = get_all_categorias()
    formatted_categorias = [f"ID: {c[0]}, Nome: {c[1]}" for c in categorias]
    show_results(result_listbox, formatted_categorias)


def handle_add_categoria(result_listbox):
    def add():
        nome_categoria = nome_categoria_var.get()
        if nome_categoria:
            add_categoria(nome_categoria)
            top.destroy()
            show_results(["Categoria adicionada com sucesso"])
        else:
            show_results(["Nome da categoria não fornecido"])

    top = Toplevel()
    top.title("Adicionar Categoria")
    
    Label(top, text="Nome da Categoria:").grid(row=0, column=0, sticky='e')
    nome_categoria_var = StringVar()
    Entry(top, textvariable=nome_categoria_var).grid(row=0, column=1)
    
    Button(top, text="Adicionar", command=add).grid(row=1, column=0, columnspan=2, pady=5)

def handle_delete_categoria(result_listbox):
    def delete():
        categoria_id = categoria_id_var.get()
        if categoria_id:
            delete_categoria(categoria_id)
            top.destroy()
            show_results(["Categoria deletada com sucesso"])
        else:
            show_results(["ID da categoria não fornecido"])

    top = Toplevel()
    top.title("Deletar Categoria")
    
    Label(top, text="ID da Categoria:").grid(row=0, column=0, sticky='e')
    categoria_id_var = StringVar()
    Entry(top, textvariable=categoria_id_var).grid(row=0, column=1)
    
    Button(top, text="Deletar", command=delete).grid(row=1, column=0, columnspan=2, pady=5)


def handle_add_fornecedor(result_listbox):
    def add():
        nome = nome_var.get()
        cnpj = cnpj_var.get()
        contato = contato_var.get()
        
        if nome and cnpj and contato:
            add_fornecedor(nome, cnpj, contato)
            top.destroy()
            show_results(result_listbox, ["Fornecedor adicionado com sucesso"])
        else:
            show_results(["Todos os campos devem ser preenchidos"])

    top = Toplevel()
    top.title("Adicionar Fornecedor")
    
    Label(top, text="Nome:").grid(row=0, column=0, sticky='e')
    nome_var = StringVar()
    Entry(top, textvariable=nome_var).grid(row=0, column=1)
    
    Label(top, text="CNPJ:").grid(row=1, column=0, sticky='e')
    cnpj_var = StringVar()
    Entry(top, textvariable=cnpj_var).grid(row=1, column=1)
    
    Label(top, text="Contato:").grid(row=2, column=0, sticky='e')
    contato_var = StringVar()
    Entry(top, textvariable=contato_var).grid(row=2, column=1)
    
    Button(top, text="Adicionar", command=add).grid(row=3, column=0, columnspan=2, pady=5)

def handle_delete_fornecedor(result_listbox):
    def delete():
        fornecedor_id = fornecedor_id_var.get()
        if fornecedor_id:
            delete_fornecedor(fornecedor_id)
            top.destroy()
            show_results(["Fornecedor deletado com sucesso"])
        else:
            show_results(["ID do fornecedor não fornecido"])

    top = Toplevel()
    top.title("Deletar Fornecedor")
    
    Label(top, text="ID do Fornecedor:").grid(row=0, column=0, sticky='e')
    fornecedor_id_var = StringVar()
    Entry(top, textvariable=fornecedor_id_var).grid(row=0, column=1)
    
    Button(top, text="Deletar", command=delete).grid(row=1, column=0, columnspan=2, pady=5)
   

def handle_add_product(result_listbox):
    def add():
        product_name = name_var.get()
        product_category = category_var.get()
        product_quantity = quantity_var.get()
        product_weight = weight_var.get()
        
        if product_name and product_category and product_quantity and product_weight:
            try:
                # Converte a quantidade e o peso para o tipo apropriado
                quantity = int(product_quantity)
                weight = float(product_weight)
                category = str(product_category)
                
                # Obtém o ID da categoria a partir do nome da categoria
                category_id = get_category_id(product_category)
                
                if category_id is not None:
                    # Adiciona o produto ao banco de dados
                    add_product(product_name, category, category_id, quantity, weight)
                    top.destroy()
                    show_results(result_listbox,get_all_products())
                else:
                    show_results(["Categoria não encontrada"])
            except ValueError:
                show_results(["Quantidade deve ser um número inteiro e peso deve ser um número válido"])
        else:
            show_results(["Todos os campos devem ser preenchidos"])

    top = Toplevel()
    top.title("Adicionar Produto")
    
    Label(top, text="Nome do Produto:").grid(row=0, column=0, sticky='e')
    name_var = StringVar()
    Entry(top, textvariable=name_var).grid(row=0, column=1)
    
    Label(top, text="Categoria do Produto:").grid(row=1, column=0, sticky='e')
    category_var = StringVar()
    Entry(top, textvariable=category_var).grid(row=1, column=1)
    
    Label(top, text="Quantidade Mínima:").grid(row=2, column=0, sticky='e')
    quantity_var = StringVar()
    Entry(top, textvariable=quantity_var).grid(row=2, column=1)
    
    Label(top, text="Peso do Produto:").grid(row=3, column=0, sticky='e')
    weight_var = StringVar()
    Entry(top, textvariable=weight_var).grid(row=3, column=1)
    
    Button(top, text="Adicionar", command=add).grid(row=4, column=0, columnspan=2, pady=5)


def handle_delete_product(result_listbox):
    def delete():
        product_id = product_id_var.get()
        if product_id:
            delete_product(product_id)
            top.destroy()
            show_results(result_listbox, get_all_products())
        else:
            show_results(["Produto ID não fornecido"])

    top = Toplevel()
    top.title("Deletar Produto")
    
    Label(top, text="Produto ID:").grid(row=0, column=0, sticky='e')
    product_id_var = StringVar()
    Entry(top, textvariable=product_id_var).grid(row=0, column=1)
    
    Button(top, text="Deletar", command=delete).grid(row=1, column=0, columnspan=2, pady=5)

def handle_registrar_entrada(result_listbox):
    def registrar():
        pid = pid_var.get()
        fornecedor_id = fornecedor_id_var.get()
        quantidade = quantidade_var.get()
        data_operacao = data_operacao_var.get()
        data_pedido = data_pedido_var.get()
        data_entrega = data_entrega_var.get()
        
        if all([pid, fornecedor_id, quantidade, data_operacao, data_pedido, data_entrega]):
            success = registrar_entrada(pid, fornecedor_id, quantidade, data_operacao, data_pedido, data_entrega)
            if success:
                top.destroy()
                show_results(result_listbox, ["Entrada registrada com sucesso"])
            else:
                show_results(["Erro ao registrar entrada"])
        else:
            show_results(["Todos os campos devem ser preenchidos"])

    top = Toplevel()
    top.title("Registrar Entrada")
    
    fields = [
        ("ID do Produto", StringVar()),
        ("ID do Fornecedor", StringVar()),
        ("Quantidade", StringVar()),
        ("Data da Operação", StringVar()),
        ("Data do Pedido", StringVar()),
        ("Data de Entrega", StringVar())
    ]
    
    for i, (label, var) in enumerate(fields):
        Label(top, text=label).grid(row=i, column=0, sticky='e')
        Entry(top, textvariable=var).grid(row=i, column=1)
    
    pid_var, fornecedor_id_var, quantidade_var, data_operacao_var, data_pedido_var, data_entrega_var = [var for _, var in fields]
    
    Button(top, text="Registrar", command=registrar).grid(row=len(fields), column=0, columnspan=2, pady=5)



def handle_registrar_saida(result_listbox):
    def registrar():
        pid = pid_var.get()
        quantidade = quantidade_var.get()
        data_operacao = data_operacao_var.get()
        loja_destino = loja_destino_var.get()
        transportadora = transportadora_var.get()
        
        if all([pid, quantidade, data_operacao, loja_destino, transportadora]):
            success = registrar_saida(pid, quantidade, data_operacao, loja_destino, transportadora)
            if success:
                top.destroy()
                show_results(result_listbox, ["Saída registrada com sucesso"])
            else:
                show_results(result_listbox, ["Erro ao registrar saída"])
        else:
            show_results(result_listbox, ["Todos os campos devem ser preenchidos"])

    top = Toplevel()
    top.title("Registrar Saída")
    
    fields = [
        ("ID do Produto", StringVar()),
        ("Quantidade", StringVar()),
        ("Data da Operação", StringVar()),
        ("Loja de Destino", StringVar()),
        ("Transportadora", StringVar())
    ]
    
    for i, (label, var) in enumerate(fields):
        Label(top, text=label).grid(row=i, column=0, sticky='e')
        Entry(top, textvariable=var).grid(row=i, column=1)
    
    pid_var, quantidade_var, data_operacao_var, loja_destino_var, transportadora_var = [var for _, var in fields]
    
    Button(top, text="Registrar", command=registrar).grid(row=len(fields), column=0, columnspan=2, pady=5)


def handle_get_products_by_supplier(result_listbox):
    def show_products():
        supplier_id = supplier_id_var.get()
        if supplier_id:
            products = get_products_by_supplier(supplier_id)
            results = [f"Produtos do Fornecedor (ID: {supplier_id}):", ""]
            for product in products:
                product_info = f"ID: {product[0]}, Nome: {product[1]}"
                if len(product) > 2:
                    product_info += f", Categoria: {product[2]}"
                results.append(product_info)
            show_results(result_listbox, results)
        else:
            show_results(result_listbox, ["Por favor, insira um ID de fornecedor válido."])

    top = Toplevel()
    top.title("Buscar Produtos por Fornecedor")
    
    Label(top, text="ID do Fornecedor:").grid(row=0, column=0, sticky='e')
    supplier_id_var = StringVar()
    Entry(top, textvariable=supplier_id_var).grid(row=0, column=1)
    
    Button(top, text="Buscar Produtos", command=show_products).grid(row=1, column=0, columnspan=2, pady=5)

    top = Toplevel(root)
    top.title("Buscar Produtos por Fornecedor")
    
    Label(top, text="ID do Fornecedor:").grid(row=0, column=0, sticky='e')
    supplier_id_var = StringVar()
    Entry(top, textvariable=supplier_id_var).grid(row=0, column=1)
    
    Button(top, text="Buscar Produtos", command=show_products).grid(row=1, column=0, columnspan=2, pady=5)



def handle_get_suppliers_by_product(result_listbox):
    suppliers_data = get_suppliers_by_product()
    results = ["Fornecedores por Produto (com preços):", ""]
    for product, suppliers in suppliers_data:
        results.append(f"Produto: {product}")
        results.append(f"Fornecedores: {suppliers}")
        results.append("")
    show_results(result_listbox, results)

def handle_get_products_by_category(result_listbox):
    def show_products():
        category_id = category_var.get()
        if category_id:
            products = get_products_by_category(category_id)
            results = [f"Produtos da Categoria (ID: {category_id}):", ""]
            for product in products:
                product_info = f"ID: {product[0]}"
                if len(product) > 1:
                    product_info += f", Nome: {product[1]}"
                results.append(product_info)
            show_results(result_listbox, results)
        else:
            show_results(["Por favor, selecione uma categoria."])


    top = Toplevel()
    top.title("Buscar Produtos por Categoria")
    
    Label(top, text="Categoria:").grid(row=0, column=0, sticky='e')
    categories = get_all_categorias()
    category_var = StringVar()
    category_dropdown = OptionMenu(top, category_var, *[cat[0] for cat in categories])
    category_dropdown.grid(row=0, column=1)
    
    Button(top, text="Buscar Produtos", command=show_products).grid(row=1, column=0, columnspan=2, pady=5)


def handle_get_revenue_by_date_range(result_listbox):
    def show_revenue():
        start_date = start_date_var.get()
        end_date = end_date_var.get()
        if start_date and end_date:
            revenue_data = get_revenue_by_date_range(start_date, end_date)
            results = [f"Faturamento no período de {start_date} a {end_date}:", ""]
            current_store = None
            for loja, mes, ano, faturamento in revenue_data:
                if loja != current_store:
                    if current_store is not None:
                        results.append("")
                    results.append(f"Loja: {loja}")
                    current_store = loja
                results.append(f"  {ano}/{mes:02d}: R$ {faturamento:.2f}")
            show_results(result_listbox, results)
        else:
            show_results(["Por favor, insira datas válidas."])

    top = Toplevel()
    top.title("Faturamento por Intervalo de Datas")
    
    Label(top, text="Data Inicial (YYYY-MM-DD):").grid(row=0, column=0, sticky='e')
    start_date_var = StringVar()
    Entry(top, textvariable=start_date_var).grid(row=0, column=1)
    
    Label(top, text="Data Final (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
    end_date_var = StringVar()
    Entry(top, textvariable=end_date_var).grid(row=1, column=1)
    
    Button(top, text="Mostrar Faturamento", command=show_revenue).grid(row=2, column=0, columnspan=2, pady=5)

def handle_get_products_more_than_days_in_stock(result_listbox):
    def show_products():
        days = days_var.get()
        if days:
            products = get_products_more_than_days_in_stock(days)
            results = [f"Produtos com mais de {days} dias no estoque:", ""]
            for product in products:
                results.append(f"Nome: {product[0]}, Dias no estoque: {product[1]}")
            show_results(result_listbox, results)
        else:
            show_results(["Por favor, insira um número válido de dias."])

    top = Toplevel()
    top.title("Produtos com Mais Dias no Estoque")
    
    Label(top, text="Número de dias:").grid(row=0, column=0, sticky='e')
    days_var = StringVar()
    Entry(top, textvariable=days_var).grid(row=0, column=1)
    
    Button(top, text="Buscar Produtos", command=show_products).grid(row=1, column=0, columnspan=2, pady=5)

def handle_get_monthly_revenue_by_store(result_listbox):
    def show_revenue():
        store = store_var.get()
        if store:
            monthly_revenue = get_monthly_revenue_by_store(store)
            show_results(result_listbox, monthly_revenue)
        else:
            show_results(result_listbox, ["Loja não fornecida"])

    top = Toplevel()
    top.title("Faturamento Mensal por Loja")
    top.transient(root)
    top.grab_set()
    
    Label(top, text="Selecione a Loja:").grid(row=0, column=0, sticky='e')
    store_var.set("Todas")  # default value
    stores = ["Todas"] + [store[0] for store in get_all_stores()]
    OptionMenu(top, store_var, *stores).grid(row=0, column=1)
    
    Button(top, text="Mostrar Faturamento", command=show_revenue).grid(row=1, column=0, columnspan=2, pady=5)


def handle_get_average_delivery_time(result_listbox):
    delivery_data = get_supplier_delivery_details()
    results = ["Tempo de Entrega por Fornecedor:", ""]
    
    if delivery_data:
        current_supplier = None
        supplier_avg_time = {}
        
        for supplier, avg_time, product, delivery_time in delivery_data:
            if all([supplier, avg_time, product, delivery_time]):
                if supplier != current_supplier:
                    if current_supplier:
                        results.append(f"Tempo Médio de Entrega: {supplier_avg_time[current_supplier]:.2f} dias")
                        results.append("")
                    current_supplier = supplier
                    results.append(f"Fornecedor: {supplier}")
                
                results.append(f"  Produto: {product}")
                results.append(f"  Tempo de Entrega: {delivery_time} dias")
                
                if supplier not in supplier_avg_time:
                    supplier_avg_time[supplier] = avg_time
        
        # Add average time for the last supplier
        if current_supplier:
            results.append(f"Tempo Médio de Entrega: {supplier_avg_time[current_supplier]:.2f} dias")
    else:
        results.append("Nenhum dado de entrega encontrado.")
    
    show_results(result_listbox, results)





def handle_get_product_movement_history(result_listbox):
    def show_history():
        product_id = product_id_var.get()
        if product_id:
            history_data = get_product_movement_history(product_id)
            if history_data:
                results = [f"Histórico de Movimentação do Produto (ID: {product_id}):", ""]
                for entry in history_data:
                    results.append(f"ID: {entry[0]}")
                    results.append(f"Produto: {entry[1]}")
                    results.append(f"Quantidade: {entry[2]}")
                    results.append(f"Tipo de Operação: {entry[3]}")
                    results.append(f"Data: {entry[4]}")
                    results.append(f"Loja Destino: {entry[5] or 'N/A'}")
                    results.append(f"Fornecedor: {entry[6]}")
                    results.append(f"Transportadora: {entry[7] or 'N/A'}")
                    results.append("")
            else:
                results = ["Nenhum histórico encontrado para este produto."]
            show_results(result_listbox, results)
        else:
            show_results(result_listbox, ["Por favor, insira um ID de produto válido."])

    top = Toplevel()
    top.title("Histórico de Movimentação de Produto")
    
    Label(top, text="ID do Produto:").grid(row=0, column=0, sticky='e')
    product_id_var = StringVar()
    Entry(top, textvariable=product_id_var).grid(row=0, column=1)
    
    Button(top, text="Mostrar Histórico", command=show_history).grid(row=1, column=0, columnspan=2, pady=5)



def handle_list_products_below_min_quantity(result_listbox):
    products = get_products_below_min_quantity()
    formatted_products = [f"ID: {p[0]}, Nome: {p[1]}, Quantidade Atual: {p[2]}, Quantidade Mínima: {p[3]}" for p in products]
    show_results(result_listbox, formatted_products)

def handle_get_most_sold_product_in_period(result_listbox):
    def show_most_sold():
        start_date = start_date_var.get()
        end_date = end_date_var.get()
        if start_date and end_date:
            products_data = get_most_sold_product_in_period(start_date, end_date)
            if products_data:
                max_quantity = products_data[0][1]
                most_sold = [p for p in products_data if p[1] == max_quantity]
                results = [f"Produto(s) Mais Vendido(s) no período de {start_date} a {end_date}:", ""]
                for product in most_sold:
                    results.append(f"Nome: {product[0]}")
                    results.append(f"Quantidade Vendida: {product[1]}")
                    results.append(f"Faturamento Total: R$ {product[2]:.2f}")
                    results.append("")
            else:
                results = ["Nenhum produto vendido neste período."]
            show_results(result_listbox, results)
        else:
            show_results(["Por favor, insira datas válidas."])

    top = Toplevel()
    top.title("Produto Mais Vendido em Período")
    
    Label(top, text="Data Inicial (YYYY-MM-DD):").grid(row=0, column=0, sticky='e')
    start_date_var = StringVar()
    Entry(top, textvariable=start_date_var).grid(row=0, column=1)
    
    Label(top, text="Data Final (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
    end_date_var = StringVar()
    Entry(top, textvariable=end_date_var).grid(row=1, column=1)
    
    Button(top, text="Mostrar Produtos Mais Vendidos", command=show_most_sold).grid(row=2, column=0, columnspan=2, pady=5)

def handle_detailed_carriers_analysis(result_listbox):
    most_used_entrada, most_used_saida, carriers_data = get_most_used_carriers()
    
    results = [
        f"Transportadora mais utilizada para entrada: {most_used_entrada[0]} ({most_used_entrada[1]} entradas)",
        f"Transportadora mais utilizada para saída: {most_used_saida[0]} ({most_used_saida[2]} saídas)",
        "\nRelação de transportadoras x entradas/saídas:"
    ]
    
    for carrier in carriers_data:
        results.append(f"{carrier[0]}: {carrier[1]} entradas, {carrier[2]} saídas")
    
    show_results(result_listbox, results)


def handle_categories_item_count(result_listbox):
    most_items_category, categories_data = get_categories_item_count()
    
    results = [
        f"Categoria com mais itens: {most_items_category[0]} ({most_items_category[1]} itens)",
        "\nRelação de categorias x quantidade de itens:"
    ]
    
    for category in categories_data:
        results.append(f"{category[0]}: {category[1]} itens")
    
    show_results(result_listbox, results)

def handle_get_monthly_revenue_by_store(result_listbox):
    def show_revenue():
        store = store_var.get()
        if store:
            monthly_revenue = get_monthly_revenue_by_store(store)
            show_results(result_listbox, monthly_revenue)
        else:
            show_results(result_listbox, ["Loja não fornecida"])

    top = Toplevel()
    top.title("Faturamento Mensal por Loja")
    top.transient()
    top.grab_set()
    
    Label(top, text="Selecione a Loja:").grid(row=0, column=0, sticky='e')
    store_var.set("Todas")  # default value
    stores = ["Todas"] + [store[0] for store in get_all_stores()]
    OptionMenu(top, store_var, *stores).grid(row=0, column=1)
    
    Button(top, text="Mostrar Faturamento", command=show_revenue).grid(row=1, column=0, columnspan=2, pady=5)


def handle_get_most_active_suppliers(result_listbox):
    suppliers_data = get_most_active_suppliers()
    results = ["Fornecedores Mais Ativos:", ""]
    
    if suppliers_data:
        most_active = suppliers_data[0]
        results.append(f"Fornecedor Mais Ativo:")
        results.append(f"Nome: {most_active[0]}")
        results.append(f"Quantidade de Produtos: {most_active[1]}")
        results.append("")
        results.append("Outros Fornecedores:")
        
        for supplier, product_count in suppliers_data[1:]:
            results.append(f"Fornecedor: {supplier}")
            results.append(f"Quantidade de Produtos: {product_count}")
            results.append("")
    else:
        results.append("Nenhum fornecedor encontrado.")
    
    show_results(result_listbox, results)

def handle_get_total_products_by_carrier(result_listbox):
    carrier_data = get_total_products_by_carrier()
    results = ["Total de Produtos por Transportadora:", ""]
    for carrier, total_quantity, entrada_quantity, saida_quantity in carrier_data:
        results.append(f"Transportadora: {carrier}")
        results.append(f"Total de Produtos: {total_quantity}")
        results.append(f"Quantidade de Entrada: {entrada_quantity}")
        results.append(f"Quantidade de Saída: {saida_quantity}")
        results.append("")
    show_results(result_listbox, results)

def handle_get_recently_added_products(result_listbox):
    products_data = get_recently_added_products()
    results = ["Produtos Recentemente Adicionados ao Estoque:", ""]
    for product, date, quantity in products_data:
        results.append(f"Produto: {product}")
        results.append(f"Data de Entrada: {date}")
        results.append(f"Quantidade: {quantity}")
        results.append("")
    show_results(result_listbox, results)

def handle_get_product_with_longest_stock_duration(result_listbox):
    products_data = get_product_with_longest_stock_duration()
    results = ["Produto(s) com Maior Tempo de Permanência no Estoque:", ""]
    if products_data:
        max_duration = products_data[0][1]
        for product, duration in products_data:
            if duration == max_duration:
                results.append(f"Produto: {product}")
                results.append(f"Tempo no Estoque: {duration} dias")
                results.append("")
            else:
                break
    else:
        results.append("Nenhum produto encontrado no estoque.")
    show_results(result_listbox, results)

def handle_get_sales_performance_by_category(result_listbox):
    performance_data = get_sales_performance_by_category()
    results = ["Análise de Desempenho de Vendas por Categoria:", ""]
    
    if performance_data:
        max_sales_category = max(performance_data, key=lambda x: x[1])
        results.append(f"Categoria com Maior Venda: {max_sales_category[0]} (R$ {max_sales_category[1]:.2f})")
        results.append("")
        
        for category, total_sales, sales_count in performance_data:
            results.append(f"Categoria: {category}")
            results.append(f"Total Vendido: R$ {total_sales:.2f}")
            results.append(f"Quantidade de Vendas: {sales_count}")
            results.append("")
    else:
        results.append("Nenhum dado de venda encontrado.")
    
    show_results(result_listbox, results)


    
def handle_list_inventory(result_listbox):
    inventory_data = get_current_inventory()
    results = ["Estoque Atual:", ""]
    current_category = None
    for estoque_id, pid, product, category, quantity, below_min in inventory_data:
        if category != current_category:
            results.append(f"\nCategoria: {category}")
            current_category = category
        results.append(f"ID Estoque: {estoque_id}")
        results.append(f"ID Produto: {pid}")
        results.append(f"Produto: {product}")
        results.append(f"Quantidade: {quantity}")
        results.append(f"Abaixo do mínimo: {'Sim' if below_min else 'Não'}")
        results.append("")
    show_results(result_listbox, results)






# Configuração da interface gráfica
root = Tk()
root.title("Controle de Estoque")

canvas = Canvas(root)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
frame = Frame(canvas)

# Add the frame to a window in the canvas

# Campos de entrada e botões

Label(frame, text="Loja:").grid(row=6, column=0, sticky='e')
store_var = StringVar()
Entry(frame, textvariable=store_var).grid(row=6, column=1)

root.mainloop()
