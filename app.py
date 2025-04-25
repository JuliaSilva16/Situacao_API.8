from flask import Flask, request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import *
app = Flask(__name__)

app.config['SECRET_KEY'] = '<KEY>'


@app.route('/novo_cliente', methods=['POST'])
def cadastro_cliente():

    """

    :return: está retornando os dados do cadastro do cliente
    """
    if not request.form['form_nome_cliente'] or not request.form['form_cpf'] or not request.form[
        'form_telefone'] or not request.form['endereco']:
            print('Obritório preencher todos os campos')

    try:
        dados_cliente = request.get_json()

        nome_cliente = dados_cliente['nome_cliente']
        cpf = dados_cliente['cpf']
        telefone = dados_cliente['telefone']
        endereco = dados_cliente['endereco']

        form_cadastro_cliente = Cliente(
            nome_cliente=nome_cliente,
            cpf=cpf,
            telefone=telefone,
            endereco=endereco,

        )
        form_cadastro_cliente.save()

        return jsonify({
            'mensagem': 'Cliente cadastrado com sucesso!'
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })
    except IntegrityError:
        return jsonify({"Error": "Erro cpf já existente"})

@app.route('/clientes', methods=["GET"])
def clientes():
    """

    :return: está retornando os dados do cliente
    """

    try:
        sql_clientes = db_session.execute(select(Cliente)).scalars().all()
        lista_clientes = []
        for cliente in sql_clientes:
            lista_clientes.append(cliente.serialize_user())
        return jsonify(lista_clientes)

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/novo_veiculo', methods=['POST'])
def cadastro_veiculos():
    """

    :return: está retornando os dados do cadastro do veiculo
    """
    if not request.form['form_cliente_associado'] or not request.form['form_marca_veiculo'] or not request.form[
        'form_modelo_veiculo'] or not request.form['form_placa_veiculo'] or not request.form['form_ano_fabricacao']:
        print('Obritório preencher todos os campos')

    try:
        dados_veiculo = request.get_json()

        cliente_associado = dados_veiculo['cliente_associado']
        marca_veiculo  = dados_veiculo['marca_veiculo']
        modelo_veiculo = dados_veiculo['modelo_veiculo']
        placa_veiculo = dados_veiculo['placa_veiculo']
        ano_fabricacao = dados_veiculo['ano_fabricacao']

        form_cadastro_veculos = Veiculo(
            cliente_associado=cliente_associado,
            marca_veiculo =marca_veiculo,
            modelo_veiculo=modelo_veiculo,
            placa_veiculo=placa_veiculo,
            ano_fabricacao=ano_fabricacao,

        )
        form_cadastro_veculos.save()

        return jsonify({
            'mensagem': 'Veiculo cadastrado com sucesso!'
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
        sql_veiculo = db_session.execute(select(Veiculo)).scalars().all()
        lista_veiculo = []
        for veiculo in sql_veiculo:
            lista_veiculo.append(veiculo.serialize_user())
        return jsonify({
            "veiculo": {lista_veiculo}
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/nova_ordem_servico', methods=['POST'])
def cadastro_ordem_servico():
    """está retornando os dados do cadastro do ordem servico"""
    if not request.form['form_veiculo_associado'] or not request.form['form_data_abertura'] or not request.form[
        'form_descricao_servico'] or not request.form['form_status'] or not request.form['form_valor_estimado']:
        print('Obritório preencher todos os campos')
    try:
        dados_servico = request.get_json()

        veiculo_associado = dados_servico['veiculo_associado']
        data_abertura = dados_servico['data_abertura']
        descricao_servico = dados_servico['descricao_servico']
        status = dados_servico['status']
        valor_estimado = dados_servico['valor_estimado']

        form_ordem_servico = Ordem_servico(
            veiculo_associado = veiculo_associado,
            data_abertura = data_abertura,
            descricao_servico = descricao_servico,
            status = status,
            valor_estimado = valor_estimado,

        )
        form_ordem_servico.save()

        return jsonify({
            'mensagem': 'Cliente cadastrado com sucesso!'
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





@app.route('/editar_cliente/<int:cliente_id>', methods=["POST"])
def editar_cliente(cliente_id):
    dados_editar_cliente = request.get_json()
    try:
        atualizacao_cliente = db_session.execute(select(Cliente).where(Cliente.id_cliente == cliente_id)).scalars().first()

        if not atualizacao_cliente:
            return jsonify({"Error":'Não se encontra o cliente'})

        if(not "nome_cliente" in  dados_editar_cliente or not "cpf" in dados_editar_cliente  or not "telefone" in dados_editar_cliente or not "endereco" in dados_editar_cliente):
            return jsonify({"Error":"Obrigatório preencher todos os campos"}),400

        cpf = dados_editar_cliente['cpf'].strip()
        if atualizacao_cliente.cpf != cpf:
            cpf_existe = db_session.query(Cliente).filter(Cliente.cpf == cpf).scalar()
            if cpf_existe:
                return jsonify({
                    "error": "Este CPF já existe na lista de clientes"
                }), 400

        atualizacao_cliente.nome_cliente = dados_editar_cliente['nome_cliente']
        atualizacao_cliente.cpf = dados_editar_cliente['cpf'].strip()
        atualizacao_cliente.telefone = dados_editar_cliente['telefone'].strip()
        atualizacao_cliente.endereco = dados_editar_cliente['endereco']

        atualizacao_cliente.save()

        return jsonify({
            "nome": atualizacao_cliente.nome_cliente,
            "cpf": atualizacao_cliente.cpf,
            "telefone": atualizacao_cliente.telefone,
            "endereco": atualizacao_cliente.endereco,
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()


@app.route('/status', methods=['GET'])
def status():
    try:
        veiculo_ocupado = db_session.execute(
            select(Veiculo).where(Veiculo.id_veiculo == Ordem_servico.veiculo).distinc(Veiculo.id_veiculo)).scalars()

        veiculos = db_session.execute(select(Veiculo)).scalars()
        lista_veiculo_ocupado = []
        lista_veiculo_livre = []

        for veiculo in veiculos:
            lista_veiculo_ocupado.append(veiculo.serialize_user())

        for vehicle in veiculos:
            if vehicle.id_veiculo not in lista_veiculo_ocupado:
                lista_veiculo_livre.append(vehicle.serialize_user())

        return jsonify({
            "veiculos ocupados":lista_veiculo_ocupado,
            "veiculos livres":lista_veiculo_livre
        }),200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)

