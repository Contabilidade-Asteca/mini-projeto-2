"""Aplicação web para o sistema bancário educativo."""

from flask import Flask, flash, redirect, render_template, request, url_for

from dsaoperacoes.banco import Banco
from dsautilitarios.exceptions import ContaInexistenteError, SaldoInsuficienteError

app = Flask(__name__)
app.config["SECRET_KEY"] = "dsa-mini-projeto-2"

banco = Banco("Banco Digital DSA")


def _resumo_dashboard():
    contas = banco.listar_contas()
    clientes = banco.listar_clientes()
    total_saldo = sum(conta.saldo for conta in contas)
    return {
        "clientes": sorted(clientes, key=lambda cliente: cliente.nome.lower()),
        "contas": sorted(contas, key=lambda conta: conta.numero),
        "total_clientes": len(clientes),
        "total_contas": len(contas),
        "total_saldo": total_saldo,
    }


@app.route("/")
def dashboard():
    contexto = _resumo_dashboard()
    return render_template("index.html", **contexto, extrato=None)


@app.route("/clientes", methods=["POST"])
def adicionar_cliente():
    nome = request.form.get("nome", "").strip()
    cpf = request.form.get("cpf", "").strip()

    if not nome or not cpf:
        flash("Informe nome e CPF para cadastrar um cliente.", "danger")
        return redirect(url_for("dashboard"))

    if banco.cliente_existe(cpf):
        flash("Já existe um cliente cadastrado com este CPF.", "warning")
        return redirect(url_for("dashboard"))

    banco.adicionar_cliente(nome, cpf)
    flash(f"Cliente {nome} cadastrado com sucesso!", "success")
    return redirect(url_for("dashboard"))


@app.route("/contas", methods=["POST"])
def criar_conta():
    cpf = request.form.get("cpf_cliente", "").strip()
    tipo = request.form.get("tipo", "").strip()

    cliente = banco.buscar_cliente(cpf)
    if not cliente:
        flash("Cliente não encontrado. Cadastre o cliente antes de criar uma conta.", "danger")
        return redirect(url_for("dashboard"))

    conta = banco.criar_conta(cliente, tipo)
    if conta is None:
        flash("Tipo de conta inválido. Escolha entre conta corrente ou poupança.", "danger")
        return redirect(url_for("dashboard"))

    flash(
        f"Conta {conta.numero} ({'Corrente' if conta.tipo.endswith('Corrente') else 'Poupança'}) criada para {cliente.nome}.",
        "success",
    )
    return redirect(url_for("dashboard"))


@app.route("/contas/depositar", methods=["POST"])
def depositar():
    numero = request.form.get("numero_conta_deposito", "").strip()
    valor = request.form.get("valor_deposito", "").strip()

    try:
        numero = int(numero)
        valor = float(valor)
    except ValueError:
        flash("Informe número da conta e valor válidos para depósito.", "danger")
        return redirect(url_for("dashboard"))

    if valor <= 0:
        flash("O valor do depósito deve ser maior que zero.", "warning")
        return redirect(url_for("dashboard"))

    try:
        conta = banco.buscar_conta(numero)
    except ContaInexistenteError as erro:
        flash(str(erro), "danger")
        return redirect(url_for("dashboard"))

    conta.depositar(valor)
    flash(f"Depósito de R${valor:.2f} realizado na conta {numero}.", "success")
    return redirect(url_for("dashboard"))


@app.route("/contas/sacar", methods=["POST"])
def sacar():
    numero = request.form.get("numero_conta_saque", "").strip()
    valor = request.form.get("valor_saque", "").strip()

    try:
        numero = int(numero)
        valor = float(valor)
    except ValueError:
        flash("Informe número da conta e valor válidos para saque.", "danger")
        return redirect(url_for("dashboard"))

    if valor <= 0:
        flash("O valor do saque deve ser maior que zero.", "warning")
        return redirect(url_for("dashboard"))

    try:
        conta = banco.buscar_conta(numero)
    except ContaInexistenteError as erro:
        flash(str(erro), "danger")
        return redirect(url_for("dashboard"))

    try:
        conta.sacar(valor)
        flash(f"Saque de R${valor:.2f} realizado na conta {numero}.", "success")
    except SaldoInsuficienteError as erro:
        flash(str(erro), "danger")

    return redirect(url_for("dashboard"))


@app.route("/contas/extrato", methods=["POST"])
def extrato():
    numero = request.form.get("numero_conta_extrato", "").strip()

    try:
        numero = int(numero)
    except ValueError:
        flash("Informe um número de conta válido para consultar o extrato.", "danger")
        return redirect(url_for("dashboard"))

    try:
        conta = banco.buscar_conta(numero)
    except ContaInexistenteError as erro:
        flash(str(erro), "danger")
        return redirect(url_for("dashboard"))

    historico = [
        {
            "data": data.strftime("%d/%m/%Y %H:%M"),
            "descricao": descricao,
        }
        for data, descricao in conta.obter_historico()
    ]

    contexto = _resumo_dashboard()
    contexto.update(
        {
            "extrato": {
                "numero": conta.numero,
                "cliente": conta.cliente.nome,
                "saldo": conta.saldo,
                "historico": historico,
            }
        }
    )
    return render_template("index.html", **contexto)


if __name__ == "__main__":
    app.run(debug=True)
