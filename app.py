from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Modelo (dados)
class Despesa:
    def __init__(self, categoria, valor, data):
        self.categoria = categoria
        self.valor = valor
        self.data = data

    def __str__(self):
        return f"{self.data} - {self.categoria}: R${self.valor:.2f}"


class Categoria:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome


# Dados simulados em memória
despesas = []

categorias = [
    Categoria("Alimentação"),
    Categoria("Transporte"),
    Categoria("Lazer"),
    Categoria("Moradia"),
    Categoria("Educação"),
    Categoria("Saúde"),
    Categoria("Investimentos"),
    Categoria("Impostos")
]

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html', categorias=categorias, despesas=despesas)

# Rota para adicionar uma despesa
@app.route('/add_despesa', methods=['POST'])
def add_despesa():
    categoria = request.form['categoria']
    valor = float(request.form['valor'])
    data = request.form['data']
    
    # Verifica se a categoria selecionada existe
    if categoria not in [c.nome for c in categorias]:
        return "Categoria não encontrada!", 400
    
    despesas.append(Despesa(categoria, valor, data))
    return redirect(url_for('index'))

# Rota para calcular as despesas de um mês específico
@app.route('/calcular_despesas', methods=['POST'])
def calcular_despesas():
    # Obtém o mês escolhido
    mes = request.form.get('mes')
    if not mes:
        return "Erro: mês não selecionado", 400  # Retorna erro se não houver mês selecionado

    mes_nome = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }

    # Filtra as despesas do mês escolhido
    total_despesas = sum(despesa.valor for despesa in despesas if despesa.data.startswith(f"2024-{mes}"))
    
    # Passa o valor do total de despesas e o nome do mês
    return render_template('index.html', categorias=categorias, despesas=despesas, total_despesas=total_despesas, mes_nome=mes_nome[mes])


if __name__ == "__main__":
    app.run(debug=True)
