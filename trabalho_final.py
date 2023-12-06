import pickle
import PySimpleGUI as sg
from datetime import datetime

# Model
class Produto:
    def __init__(self, codigo, descricao, preco):
        self.codigo = codigo
        self.descricao = descricao
        self.preco = preco

class Cliente:
    def __init__(self, cpf, nome, endereco, email):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.email = email

class Venda:
    def __init__(self, numero, data, cliente, itens):
        self.numero = numero
        self.data = data
        self.cliente = cliente
        self.itens = itens  

# View
class View:
    def __init__(self, controller):
        self.controller = controller

    def run(self):
        layout = [[sg.Text('Sistema de Gerenciamento de Vendas de Açougue')],
                  [sg.Button('Cadastrar Produto'), sg.Button('Cadastrar Cliente'), sg.Button('Realizar Venda'), sg.Button('Consultar Faturamento')],
                  [sg.Button('Consultar Produto'), sg.Button('Consultar Cliente'), sg.Button('Consultar Venda')],
                  [sg.Button('Sair')]]
        window = sg.Window('Casa de Carnes Baldoçougue', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break
            elif event == 'Cadastrar Produto':
                self.cadastrar_produto()
            elif event == 'Cadastrar Cliente':
                self.cadastrar_cliente()
            elif event == 'Realizar Venda':
                self.realizar_venda()
            elif event == 'Consultar Produto':
                self.consultar_produto()
            elif event == 'Consultar Cliente':
                self.consultar_cliente()
            elif event == 'Consultar Venda':
                self.consultar_venda()
            elif event == 'Consultar Faturamento':
                self.consultar_faturamento()

        window.close()

    def atualizar_tabela_produtos(self, window):
        self.data = []
        for codigo, produto in list(self.controller.produtos.items()):
            self.data.append([produto.codigo, produto.descricao, produto.preco])

        window['-TABLE-PRODUTOS-'].update(values=self.data)

    def cadastrar_produto(self):
        layout = [
            [sg.Text('Código', size=(10, 1)), sg.Input(key='codigo')],
            [sg.Text('Descrição', size=(10, 1)), sg.Input(key='descricao')],
            [sg.Text('Preço', size=(10, 1)), sg.Input(key='preco')],
            [sg.Button('Cadastrar')],
            [sg.Table(
                values=[], 
                headings=['Código', 'Descrição', 'Preço'], 
                key='-TABLE-PRODUTOS-', 
                auto_size_columns=False, 
                justification='right', 
                enable_events=True, 
                display_row_numbers=False, 
                num_rows=10,  
                col_widths=[10, 24, 10],  
                vertical_scroll_only=True, 
                select_mode='extended'  
            )],
            [sg.Button('Remover Selecionado(s)'), sg.Button('Voltar')],  
        ]

        window = sg.Window('Cadastrar Produto', layout, finalize=True) 

        self.atualizar_tabela_produtos(window)  

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break
            elif event == 'Cadastrar':
                try:
                    codigo = int(values['codigo'])
                    descricao = values['descricao']
                    preco = float(values['preco'])
                
                    if self.controller.verificar_codigo_produto_existente(codigo):
                        sg.popup(f'Erro: Já existe um produto com o código {codigo}.', title='Erro de Cadastro')
                    else:
                        self.controller.cadastrar_produto(codigo, descricao, preco)
                        sg.popup('Produto cadastrado com sucesso!')
                        self.atualizar_tabela_produtos(window)
                except ValueError:
                    sg.popup('Erro: Código e preço devem ser números!')
            elif event == 'Remover Selecionado(s)':
                rows_to_remove = values['-TABLE-PRODUTOS-']   
                if not rows_to_remove:
                    sg.popup('Selecione pelo menos um produto da tabela para remover!')
                else:
                    for row in reversed(sorted(rows_to_remove)):  
                        codigo_produto = self.data[row][0]  
                        self.controller.remover_produto(codigo_produto)  
                    self.atualizar_tabela_produtos(window)  

        window.close()

    def atualizar_tabela_clientes(self, window):
        self.data = []
        for cpf, cliente in list(self.controller.clientes.items()):
            self.data.append([cliente.cpf, cliente.nome, cliente.endereco, cliente.email])

        window['-TABLE-CLIENTES-'].update(values=self.data)

    def cadastrar_cliente(self):
        layout = [
            [sg.Text('CPF', size=(10, 1)), sg.Input(key='cpf')],
            [sg.Text('Nome', size=(10, 1)), sg.Input(key='nome')],
            [sg.Text('Endereço', size=(10, 1)), sg.Input(key='endereco')],
            [sg.Text('Email', size=(10, 1)), sg.Input(key='email')],
            [sg.Button('Salvar')],
            [sg.Table(
                values=[], 
                headings=['CPF', 'Nome', 'Endereço', 'Email'], 
                key='-TABLE-CLIENTES-', 
                auto_size_columns=False, 
                justification='right', 
                enable_events=True, 
                display_row_numbers=False, 
                num_rows=10,  
                col_widths=[15, 30, 35, 35],  
                vertical_scroll_only=True, 
                select_mode='extended'  
            )],
            [sg.Button('Remover Selecionado(s)'), sg.Button('Voltar')],  
        ]

        window = sg.Window('Cadastrar Cliente', layout, finalize=True) 

        self.atualizar_tabela_clientes(window)  

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break
            elif event == 'Salvar':
                cpf = values['cpf']
                nome = values['nome']
                endereco = values['endereco']
                email = values['email']

                if not cpf or not nome or not endereco:
                    sg.popup('Erro: Preencha CPF, Nome e Endereço!', title='Erro de Cadastro')
                elif self.controller.verificar_cpf_existente(cpf):
                    sg.popup('Erro: Já existe um cliente com o mesmo CPF.', title='Erro de Cadastro')
                elif email and self.controller.verificar_email_existente(email):
                    sg.popup('Erro: Já existe um cliente com o mesmo e-mail.', title='Erro de Cadastro')
                else:
                    self.controller.cadastrar_cliente(cpf, nome, endereco, email)
                    sg.popup('Cliente cadastrado com sucesso!')
                    self.atualizar_tabela_clientes(window)
            elif event == 'Remover Selecionado(s)':
                rows_to_remove = values['-TABLE-CLIENTES-']   
                if not rows_to_remove:
                    sg.popup('Selecione pelo menos um cliente da tabela para remover!')
                else:
                    for row in reversed(sorted(rows_to_remove)):  
                        cpf_cliente = self.data[row][0]  
                        self.controller.remover_cliente(cpf_cliente)  
                    self.atualizar_tabela_clientes(window)  

        window.close()

    def realizar_venda(self):
        layout = [[sg.Text('CPF do Cliente'), sg.Input(key='cpf'), sg.Button('Verificar CPF'), sg.Text(size=(40, 1), key='cpf_info')],
                  [sg.Text('Itens da Venda')],
                  [sg.Table(values=[], headings=['Código', 'Descrição', 'Quantidade', 'Valor Total'], key='-TABLE-', enable_events=True, col_widths=[10, 21, 10, 15], auto_size_columns=False, justification='right')],
                  [sg.Text('Código do Produto', size=(13, 1)), sg.Input(key='codigo_produto')],
                  [sg.Text('Quantidade (kg)', size=(13, 1)), sg.Input(key='quantidade')],
                  [sg.Button('Adicionar Produto'), sg.Button('Emitir Nota'), sg.Button('Cancelar')]]
        window = sg.Window('Realizar Venda', layout)

        itens_venda = []

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Verificar CPF':
                cpf_cliente = values['cpf']
                if not cpf_cliente or not self.controller.verificar_cpf_existente(cpf_cliente):
                    sg.popup('Erro: CPF não informado ou inválido. Por favor, insira um CPF válido ou cadastre o cliente.')
                else:
                    cliente = self.controller.clientes[cpf_cliente]
                    window['cpf_info'].update(f'Cliente: {cliente.nome}')
            elif event == 'Adicionar Produto':
                try:
                    codigo_produto = int(values['codigo_produto'])
                    quantidade = float(values['quantidade'])

                    if codigo_produto in self.controller.produtos:
                        produto = self.controller.produtos[codigo_produto]
                        valor_total = quantidade * produto.preco
                        itens_venda.append((produto, quantidade, valor_total))

                        window['-TABLE-'].update(values=self.formatar_tabela(itens_venda))
                    else:
                        sg.popup('Produto não encontrado. Digite um código válido.')
                except ValueError:
                    sg.popup('Erro: Código do produto e quantidade devem ser números!')
            elif event == 'Emitir Nota':
                cpf_cliente = values['cpf']
                if not cpf_cliente or not self.controller.verificar_cpf_existente(cpf_cliente):
                    sg.popup('Erro: CPF não informado ou inválido. Por favor, insira um CPF válido ou cadastre o cliente.')
                elif not itens_venda:
                    sg.popup('Erro: Adicione pelo menos um produto à venda antes de emitir a nota fiscal.')
                else:
                    cliente = self.controller.clientes[cpf_cliente]
                    valor_total = sum(item[2] for item in itens_venda)
                    data_emissao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    layout_resumo = [[sg.Text(f'Cliente: {cliente.nome} ({cpf_cliente})')],
                                    [sg.Text(f'Data: {data_emissao}')],
                                    [sg.Text(f'Valor Total: R$ {valor_total:.2f}')],
                                    [sg.Button('Confirmar'), sg.Button('Cancelar')]]
                    window_resumo = sg.Window('Resumo da Nota', layout_resumo)

                    while True:
                        event_resumo, values_resumo = window_resumo.read()
                        if event_resumo == sg.WINDOW_CLOSED or event_resumo == 'Cancelar':
                            window_resumo.close()
                            break
                        elif event_resumo == 'Confirmar':
                            numero_nota = self.controller.obter_proximo_numero_nota()
                            self.controller.realizar_venda(numero_nota, data_emissao, cliente, itens_venda)
                            sg.popup(f'Nota fiscal emitida com sucesso!\nNúmero da Nota: {numero_nota}')
                            window['-TABLE-'].update(values=[])
                            window_resumo.close()
                            window.close()
                            break

        window.close()

    def formatar_tabela(self, itens):
        return [(str(produto.codigo).ljust(10), produto.descricao.ljust(40), str(quantidade).ljust(10), f'R${valor:.2f}'.rjust(15)) for produto, quantidade, valor in itens]

    def consultar_produto(self):
        layout = [[sg.Text('Código do Produto'), sg.Input(key='codigo')],
                [sg.Button('Consultar'), sg.Button('Remover Produto'), sg.Text('', size=(23, 1)), sg.Button('Voltar')]]
        window = sg.Window('Consultar Produto', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break
            elif event == 'Consultar':
                try:
                    codigo_produto = int(values['codigo'])
                    if codigo_produto in self.controller.produtos:
                        produto = self.controller.produtos[codigo_produto]
                        sg.popup(f'Descrição: {produto.descricao}\nPreço por Kg: R${produto.preco:.2f}')
                    else:
                        sg.popup('Produto não encontrado. Digite um código válido.')
                except ValueError:
                    sg.popup('Erro: Código do produto deve ser um número inteiro!')
            elif event == 'Remover Produto':
                try:
                    codigo_remover = int(values['codigo'])
                    if codigo_remover in self.controller.produtos:
                        self.controller.remover_produto(codigo_remover)  
                        sg.popup(f'Produto com código {codigo_remover} removido com sucesso!')
                    else:
                        sg.popup('Produto não encontrado. Digite um código válido.')
                except ValueError:
                    sg.popup('Erro: Código do produto deve ser um número inteiro!')

        window.close()

    def consultar_cliente(self):
        layout = [[sg.Text('CPF do Cliente'), sg.Input(key='cpf')],
                  [sg.Button('Consultar'), sg.Button('Remover Cliente'), sg.Text('', size=(22, 1)), sg.Button('Voltar')]]
        window = sg.Window('Consultar Cliente', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break
            elif event == 'Consultar':
                cpf_cliente = values['cpf']
                if cpf_cliente in self.controller.clientes:
                    cliente = self.controller.clientes[cpf_cliente]
                    sg.popup(f'Nome: {cliente.nome}\nEndereço: {cliente.endereco}\nEmail: {cliente.email}')
                else:
                    sg.popup('Cliente não encontrado. Digite um CPF válido.')
            elif event == 'Remover Cliente':
                cpf_cliente = values['cpf']
                try:
                    if cpf_cliente in self.controller.clientes:
                        self.controller.remover_cliente(cpf_cliente)
                        sg.popup(f'Cliente com CPF {cpf_cliente} removido com sucesso!')
                    else:
                        sg.popup('Cliente não encontrado. Digite um CPF válido.')
                except ValueError as e:
                    sg.popup(f'Erro: {e}')

        window.close()

    def consultar_venda(self):
        layout = [[sg.Text('Número da Nota Fiscal'), sg.Input(key='numero')],
                  [sg.Button('Consultar'), sg.Button('Cancelar')]]
        window = sg.Window('Consultar Venda', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Consultar':
                try:
                    numero_nota = int(values['numero'])
                    if numero_nota in self.controller.vendas:
                        venda = self.controller.vendas[numero_nota]
                        self.mostrar_nota(venda)
                    else:
                        sg.popup('Nota fiscal não encontrada. Digite um número válido.')
                except ValueError:
                    sg.popup('Erro: Número da nota fiscal deve ser um número inteiro!')

        window.close()

    def mostrar_nota(self, venda):
        layout = [[sg.Text(f'Nota Fiscal - Número {venda.numero}')],
                  [sg.Text(f'Data de Emissão: {venda.data}')],
                  [sg.Text(f'CPF do Cliente: {venda.cliente.cpf}')],
                  [sg.Table(values=self.formatar_tabela_venda(venda.itens),
                            headings=['Código', 'Descrição', 'Quantidade', 'Valor Total'],
                            auto_size_columns=True,
                            justification='right',
                            key='-TABLE-')],
                  [sg.Text(f'Valor Total da Nota: R${self.calcular_valor_total(venda.itens):.2f}')],
                  [sg.Button('Fechar')]]
        window = sg.Window('Nota Fiscal', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break

        window.close()

    def formatar_tabela_venda(self, itens):
        return [(str(produto.codigo), produto.descricao, str(quantidade), f'R${valor:.2f}') for produto, quantidade, valor in itens]

    def calcular_valor_total(self, itens):
        return sum(valor for _, _, valor in itens)
    
    def consultar_faturamento_cliente(self):
        layout = [[sg.Text('CPF do Cliente'), sg.Input(key='cpf')],
                [sg.Button('Consultar'), sg.Button('Cancelar')]]
        window = sg.Window('Consultar Faturamento por Cliente', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Consultar':
                cpf_cliente = values['cpf']
                try:
                    if cpf_cliente in self.controller.clientes:
                        faturamento = self.controller.calcular_faturamento_cliente(cpf_cliente)
                        sg.popup(f'Faturamento para o cliente {self.controller.clientes[cpf_cliente].nome}: R${faturamento:.2f}')
                    else:
                        sg.popup('Cliente não encontrado. Digite um CPF válido.')
                except ValueError:
                    sg.popup('Erro: CPF do cliente deve ser um número inteiro.')

        window.close()

    def consultar_faturamento_periodo(self):
        layout = [[sg.Text('Data Inicial',size=(8, 1)), sg.Input(key='data_inicial'), sg.CalendarButton('Escolha a Data', target='data_inicial', format='%Y-%m-%d')],
                [sg.Text('Data Final',size=(8, 1)), sg.Input(key='data_final'), sg.CalendarButton('Escolha a Data', target='data_final', format='%Y-%m-%d')],
                [sg.Button('Consultar'), sg.Button('Cancelar')]]
        window = sg.Window('Consultar Faturamento por Período', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Consultar':
                try:
                    data_inicial = datetime.strptime(values['data_inicial'], '%Y-%m-%d')
                    data_final = datetime.strptime(values['data_final'], '%Y-%m-%d')

                    faturamento = self.controller.calcular_faturamento_periodo(data_inicial, data_final)
                    sg.popup(f'Faturamento no período de {data_inicial.strftime("%Y-%m-%d")} a {data_final.strftime("%Y-%m-%d")}:\nR${faturamento:.2f}')
                except ValueError:
                    sg.popup('Erro: Formato de data inválido. Utilize o formato YYYY-MM-DD.')

        window.close()

    def consultar_faturamento_produto(self):
        layout = [[sg.Text('Código do Produto'), sg.Input(key='codigo')],
                [sg.Button('Consultar'), sg.Button('Cancelar')]]
        window = sg.Window('Consultar Faturamento por Produto', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Consultar':
                try:
                    codigo_produto = int(values['codigo'])
                    if codigo_produto in self.controller.produtos:
                        faturamento = self.controller.calcular_faturamento_produto(codigo_produto)
                        sg.popup(f'Faturamento para o produto {self.controller.produtos[codigo_produto].descricao}: R${faturamento:.2f}')
                    else:
                        sg.popup('Produto não encontrado. Digite um código válido.')
                except ValueError:
                    sg.popup('Erro: Código do produto deve ser um número inteiro.')

        window.close()

    def consultar_vendas_cliente_periodo(self):
        layout = [[sg.Text('CPF do Cliente',size=(11, 1)), sg.Input(key='cpf')],
                [sg.Text('Data Inicial',size=(8, 1)), sg.Input(key='data_inicial'), sg.CalendarButton('Escolha a Data', target='data_inicial', format='%Y-%m-%d')],
                [sg.Text('Data Final',size=(8, 1)), sg.Input(key='data_final'), sg.CalendarButton('Escolha a Data', target='data_final', format='%Y-%m-%d')],
                [sg.Button('Consultar'), sg.Button('Cancelar')]]
        window = sg.Window('Consultar Vendas por Cliente e Período', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            elif event == 'Consultar':
                try:
                    cpf_cliente = values['cpf']
                    data_inicial = datetime.strptime(values['data_inicial'], '%Y-%m-%d')
                    data_final = datetime.strptime(values['data_final'], '%Y-%m-%d')

                    notas_fiscais = self.controller.calcular_faturamento_vendas_cliente_periodo(cpf_cliente, data_inicial, data_final)
                    if notas_fiscais:
                        popup_text = f'Notas Fiscais para o Cliente {self.controller.clientes[cpf_cliente].nome} no período de {data_inicial.strftime("%Y-%m-%d")} a {data_final.strftime("%Y-%m-%d")}:\n'
                        for nota, valor_total in notas_fiscais:
                            popup_text += f'Nota Fiscal {nota}: R${valor_total:.2f}\n'
                        sg.popup(popup_text)
                    else:
                        sg.popup(f'Nenhuma nota fiscal encontrada para o Cliente {self.controller.clientes[cpf_cliente].nome} no período especificado.')
                except ValueError:
                    sg.popup('Erro: Formato de data inválido. Utilize o formato YYYY-MM-DD.')

        window.close()

    def consultar_produtos_mais_vendidos(self):
        produtos_mais_vendidos = self.controller.calcular_produtos_mais_vendidos()

        layout = [[sg.Table(values=produtos_mais_vendidos,
                            headings=['Código', 'Descrição', 'Preço por Kg', 'Quantidade Vendida', 'Valor Total'],
                            auto_size_columns=True,
                            justification='right',
                            key='-TABLE-')],
                [sg.Button('Fechar')]]
        window = sg.Window('Produtos Mais Vendidos', layout)

        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Fechar':
                break

        window.close()

    def consultar_faturamento(self):
        layout = [[sg.Text('Opções de Consulta de Faturamento')],
                [sg.Button('Por Produto'), sg.Button('Por Cliente'), sg.Button('Por Período')],
                [sg.Button('Vendas por Cliente e Período'), sg.Button('Produtos Mais Vendidos'), sg.Text('')],
                [sg.Button('Voltar')]]
        window = sg.Window('Consultar Faturamento', layout)

        while True:
            event, _ = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break
            elif event == 'Por Produto':
                self.consultar_faturamento_produto()
            elif event == 'Por Cliente':
                self.consultar_faturamento_cliente()
            elif event == 'Por Período':
                self.consultar_faturamento_periodo()
            elif event == 'Vendas por Cliente e Período':
                self.consultar_vendas_cliente_periodo()
            elif event == 'Produtos Mais Vendidos':
                self.consultar_produtos_mais_vendidos()

        window.close()

# Controller
class Controller:
    def __init__(self):
        self.produtos = self.carregar_dados('produtos.pkl')
        self.clientes = self.carregar_dados('clientes.pkl')
        self.vendas = self.carregar_dados('vendas.pkl')
        self.cadastrar_cinco_produtos()

    def carregar_dados(self, arquivo):
        try:
            with open(arquivo, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def salvar_dados(self, arquivo, dados):
        with open(arquivo, 'wb') as f:
            pickle.dump(dados, f)

    def cadastrar_produto(self, codigo, descricao, preco):
        self.produtos[codigo] = Produto(codigo, descricao, preco)
        self.salvar_dados('produtos.pkl', self.produtos)

    def cadastrar_cliente(self, cpf, nome, endereco, email):
        self.clientes[cpf] = Cliente(cpf, nome, endereco, email)
        self.salvar_dados('clientes.pkl', self.clientes)

    def realizar_venda(self, numero, data, cliente, itens):
        self.vendas[numero] = Venda(numero, data, cliente, itens)
        self.salvar_dados('vendas.pkl', self.vendas)

    def obter_proximo_numero_nota(self):
        return len(self.vendas) + 1
    
    def calcular_faturamento_cliente(self, cpf_cliente):
        if cpf_cliente not in self.clientes:
            return 0.0

        faturamento = 0.0
        for venda in self.vendas.values():
            if venda.cliente.cpf == cpf_cliente:
                for item in venda.itens:
                    faturamento += item[1] * item[0].preco  

        return faturamento

    def calcular_faturamento_periodo(self, data_inicial, data_final):
        faturamento = 0.0

        for venda in self.vendas.values():
            venda_data = datetime.strptime(venda.data, '%Y-%m-%d %H:%M:%S')
            if data_inicial <= venda_data <= data_final:
                for item in venda.itens:
                    faturamento += item[1] * item[0].preco

        return faturamento
    
    def calcular_faturamento_produto(self, codigo_produto):
        if codigo_produto not in self.produtos:
            return 0.0

        faturamento = 0.0
        for venda in self.vendas.values():
            for item in venda.itens:
                produto, quantidade, _ = item
                if produto.codigo == codigo_produto:
                    faturamento += quantidade * produto.preco
        return faturamento

    def calcular_faturamento_vendas_cliente_periodo(self, cpf_cliente, data_inicial, data_final):
        notas_fiscais = []
        for venda in self.vendas.values():
            if venda.cliente.cpf == cpf_cliente:
                data_venda = datetime.strptime(venda.data, '%Y-%m-%d %H:%M:%S')
                if data_inicial <= data_venda <= data_final:
                    notas_fiscais.append((venda.numero, sum(item[2] for item in venda.itens)))
        return notas_fiscais

    def calcular_produtos_mais_vendidos(self):
        produtos_mais_vendidos = []
        produtos_quantidade = {}
        for venda in self.vendas.values():
            for item in venda.itens:
                produto, quantidade, _ = item
                if produto.codigo not in produtos_quantidade:
                    produtos_quantidade[produto.codigo] = {'produto': produto, 'quantidade': 0.0}
                produtos_quantidade[produto.codigo]['quantidade'] += quantidade

        produtos_ordenados = sorted(produtos_quantidade.values(), key=lambda x: x['quantidade'], reverse=True)[:5]

        for item in produtos_ordenados:
            produto = item['produto']
            quantidade = item['quantidade']
            valor_total = quantidade * produto.preco
            produtos_mais_vendidos.append((produto.codigo, produto.descricao, produto.preco, quantidade, f'{valor_total:.2f}'))
        return produtos_mais_vendidos
    
    def save_data(self):
        with open('produtos.pkl', 'wb') as f:
            pickle.dump(self.produtos, f)

    def save_data_cliente(self):
        with open('clientes.pkl', 'wb') as f:
            pickle.dump(self.clientes, f)
    
    def verificar_codigo_produto_existente(self, codigo):
        return codigo in self.produtos
    
    def remover_produto(self, codigo):
        if self.verificar_codigo_produto_existente(codigo):
            del self.produtos[codigo]
            self.save_data()
        else:
            raise ValueError(f'Produto com código {codigo} não existe.')
        
    def remover_cliente(self, cpf):
        if cpf in self.clientes:
            del self.clientes[cpf]
            self.save_data_cliente() 
        else:
            raise ValueError(f'Cliente com CPF {cpf} não existe.')
        
    def verificar_cpf_existente(self, cpf):
        return any(cliente.cpf == cpf for cliente in self.clientes.values())

    def verificar_email_existente(self, email):
        return any(cliente.email == email for cliente in self.clientes.values())
    
    def cadastrar_cinco_produtos(self):
        produtos_teste = [
            (1, 'Patinho Moído', 27),
            (2, 'Coxão Mole em Bife', 27.62),
            (3, 'Costela Suína', 19.98),
            (4, 'Miolo de Acém', 20.99),
            (5, 'Pernil Suíno com Osso', 21.95)
        ]

        for codigo, descricao, preco in produtos_teste:
            if not self.verificar_codigo_produto_existente(codigo):
                self.cadastrar_produto(codigo, descricao, preco)

# Main
def main():
    controller = Controller()
    view = View(controller)
    view.run()

if __name__ == "__main__":
    main()