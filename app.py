from flask import Flask, request, jsonify
from sqlalchemy import select
from models import *
app = Flask(__name__)

app.config['SECRET_KEY'] = '<KEY>'


@app.route('/clientes', methods=['POST'])
def cadastro_cliente():

    """

    :return: está retornando os dados do cadastro do cliente
    """

    try:
        if request.method == 'POST':
            if (not request.form["form_id_cliente"] or not request.form["form_nome_cliente"] or not request.form["form_cpf"]
                    or not request.form["form_telefone"] or not request.form["form_endereco"]):
                return jsonify({"error" : "Preencher todos os campos"})
            else:
                form_cadastro_cliente = Cliente(
                    id_cliente=int(request.form.get("form_id_cliente")),
                    nome_cliente=request.form.get("form_nome_cliente"),
                    cpf=(request.form.get("form_cpf")),
                    telefone=request.form.get("form_telefone"),
                    endereco=request.form.get("form_endereco"),

                )
                form_cadastro_cliente.save()

            return jsonify({
                'mensagem': 'Cliente cadastrado com sucesso!',
                'id_cliente': form_cadastro_cliente.id_cliente,
                'nome': form_cadastro_cliente.nome_cliente,
                'cpf': form_cadastro_cliente.cpf,
                'telefone': form_cadastro_cliente.telefone,
                'endereco': form_cadastro_cliente.endereco,
            })
    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/clientes', methods=["GET"])
def clientes():
    """

    :return: está retornando os dados do cliente
    """

    try:
        sql_clientes = select(Cliente)
        resultado_clientes = db_session.execute(sql_clientes).scalars()
        lista_clientes = []
        for cliente in resultado_clientes:
            lista_clientes.append(cliente.serialize_user())
        return jsonify({
            "cliente":{lista_clientes}
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/novo_veiculo', methods=['POST'])
def cadastro_veiculos():
    """

    :return: está retornando os dados do cadastro do veiculo
    """
    try:
        if request.method == 'POST':
            if (not request.form["form_id_veiculo"] or not request.form["form_cliente_associado"] or not request.form["form_marca_veiculo"]
                    or not request.form["form_modelo_veiculo"] or not request.form["form_placa_veiculo"] or not request.form["form_ano_fabricacao"]):
                return jsonify({"error" : "Preencher todos os campos"})
            else:
                form_cadastro_veiculo = Veiculo(
                    id_veiculo = int(request.form.get("form_id_veiculo")),
                    cliente_associado = int(request.form.get("form_cliente_associado")),
                    marca_veiculo = request.form.get("form_marca_veiculo"),
                    modelo_veiculo = request.form.get("form_placa_veiculo"),
                    placa_veiculo = request.form.get("form_ano_fabricacao"),
                    ano_fabricacao = request.form.get("form_ano_fabricao"),

                )
                form_cadastro_veiculo.save()

            return jsonify({
                'mensagem': 'Cliente cadastrado com sucesso!',
                'id_veiculo': form_cadastro_veiculo.id_veiculo,
                'cliente_associado': form_cadastro_veiculo.cliente_associado,
                'marca_veiculo': form_cadastro_veiculo.marca_veiculo,
                'modelo_veiculo': form_cadastro_veiculo.modelo_veiculo,
                'placa_veiculo': form_cadastro_veiculo.placa_veiculo,
                'ano_fabricacao': form_cadastro_veiculo.ano_fabricacao,
            })
    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/veiculos', methods=["GET"])
def veiculos():
    """

    :return: está retornando os dados do veiculo
    """
    try:
        sql_veiculos = select(Veiculo)
        resultado_veiculos = db_session.execute(sql_veiculos).scalars()
        lista_veiculos = []
        for veiculo in resultado_veiculos:
            lista_veiculos.append(veiculo.serialize_user())
        return jsonify({
            "veiculo":{lista_veiculos}
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/nova_ordem_servico', methods=['POST'])
def cadastro_ordem_servico():
    """está retornando os dados do cadastro do ordem servico"""
    try:
        if request.method == 'POST':
            if (not request.form["form_id_ordem_servico"] or not request.form["form_veiculo_associado"] or not request.form["form_data_abertura"]
                    or not request.form["form_descricao_servico"] or not request.form["form.status"] or not request.form["form_valor_estimado"]):
                return jsonify({"error" : "Preencher todos os campos"})
            else:
                form_cadastro_ordem_servico = Ordem_servico(
                    id_ordem_servico = int(request.form.get("form_id_ordem_servico")),
                    veiculo_associado = int(request.form.get("form_veiculo_associado")),
                    data_abertura = request.form.get("form_data_abertura"),
                    descricao_servico = request.form.get("form_descricao_servico"),
                    status = request.form.get("form_status"),
                    valor_estimado = float(request.form.get("form_valor_estimado")),
                )
                form_cadastro_ordem_servico.save()

            return jsonify({
                'mensagem':'Ordem cadastrado com sucesso!',
                'id_ordem_servico': form_cadastro_ordem_servico.id_ordem_servico,
                'veiculo_associado': form_cadastro_ordem_servico.veiculo_associado,
                'data_abertura': form_cadastro_ordem_servico.data_abertura,
                'descricao_servico': form_cadastro_ordem_servico.descricao_servico,
                'status': form_cadastro_ordem_servico.status,
                'valor_estimado': form_cadastro_ordem_servico.valor_estimado,
            })


    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/ordem_servico', methods=["GET"])
def ordem_servico():
    """

    :return: está retornando os dados do ordem servico
    """
    try:
        sql_ordem_servico = select(Ordem_servico)
        resultado_ordem_servico = db_session.execute(sql_ordem_servico).scalars()
        lista_ordem_servico = []
        for ordem in resultado_ordem_servico:
            lista_ordem_servico.append(ordem.serialize_user())
        return jsonify({
            "Ordem":{lista_ordem_servico}
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })


if __name__ == '__main__':
    app.run(debug=True)

