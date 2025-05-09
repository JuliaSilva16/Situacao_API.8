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

    try:
        dados_cliente = request.get_json()

        if not dados_cliente['nome_cliente'] or not dados_cliente['cpf'] or not dados_cliente['telefone'] or not dados_cliente['endereco']:
            return jsonify({'Obritório preencher todos os campos'})

        nome_cliente = dados_cliente['nome_cliente']
        cpf = dados_cliente['cpf']
        telefone = dados_cliente['telefone']
        endereco = dados_cliente['endereco']

        cpf_existe = db_session.query(Cliente).filter(Cliente.cpf == cpf).scalar()
        if cpf_existe:
            return jsonify({
                "error": "Este CPF já existe na lista de clientes"
            }), 400

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

    try:
        dados_veiculo = request.get_json()
        if not dados_veiculo['cliente_associado'] or not dados_veiculo['marca_veiculo'] or not dados_veiculo['modelo_veiculo'] or not dados_veiculo['placa_veiculo'] or not dados_veiculo['ano_fabricacao']:
            return jsonify({'Obritório preencher todos os campos'})

        cliente_associado = dados_veiculo['cliente_associado']
        marca_veiculo  = dados_veiculo['marca_veiculo']
        modelo_veiculo = dados_veiculo['modelo_veiculo']
        placa_veiculo = dados_veiculo['placa_veiculo']
        ano_fabricacao = dados_veiculo['ano_fabricacao']

        placa_existe = db_session.query(Veiculo).filter(Veiculo.placa_veiculo == placa_veiculo).scalar()
        if placa_existe:
            return jsonify({
                "error": "Esta placa já existe na lista de veiculos"
            }), 400

        form_cadastro_veiculos = Veiculo(
            cliente_associado=cliente_associado,
            marca_veiculo =marca_veiculo,
            modelo_veiculo=modelo_veiculo,
            placa_veiculo=placa_veiculo,
            ano_fabricacao=ano_fabricacao,

        )
        form_cadastro_veiculos.save()

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
            lista_veiculo.append(veiculo.serialize_veiculo())
        return jsonify({
            "veiculo": lista_veiculo
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })

@app.route('/nova_ordem_servico', methods=['POST'])
def cadastro_ordem_servico():
    """está retornando os dados do cadastro do ordem servico"""

    try:
        dados_servico = request.get_json()
        if not dados_servico['cliente_associado'] or not dados_servico['data_abertura'] or not dados_servico[
            'descricao_servico'] or not dados_servico['status'] or not dados_servico['valor_estimado']:
            return jsonify({'Obritório preencher todos os campos'})

        cliente_associado = dados_servico['cliente_associado']
        veiculo_associado = dados_servico['veiculo_associado']
        data_abertura = dados_servico['data_abertura']
        descricao_servico = dados_servico['descricao_servico']
        status = dados_servico['status']
        valor_estimado = dados_servico['valor_estimado']

        cliente_associado_existe = db_session.query(Ordem_servico).filter(Ordem_servico.cliente_associado == cliente_associado).scalar()
        veiculo_associado_existe = db_session.query(Ordem_servico).filter(Ordem_servico.veiculo_associado == veiculo_associado).scalar()
        if cliente_associado_existe and veiculo_associado_existe:
            return jsonify({
                "error": "Este cliente e veiculo já existe na lista de ordem de servico"
            }), 400

        form_ordem_servico = Ordem_servico(
            cliente_associado = cliente_associado,
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
            lista_ordem_servico.append(ordem.serialize_ordem_servico())
        return jsonify({
            "Ordem":lista_ordem_servico
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



@app.route('/editar_veiculo/<int:veiculo_id>', methods=["POST"])
def editar_veiculo(veiculo_id):
    dados_editar_veiculo = request.get_json()
    try:
        atualizacao_veiculo = db_session.execute(select(Veiculo).where(Veiculo.id_veiculo == veiculo_id)).scalars().first()

        if not atualizacao_veiculo:
            return jsonify({"Error":'Não se encontrado veiculo'})

        if not "cliente_associado" in dados_editar_veiculo or not "marca_veiculo" in dados_editar_veiculo  or not "modelo_veiculo" in dados_editar_veiculo or not "placa_veiculo" in dados_editar_veiculo or not "ano_fabricacao" in dados_editar_veiculo:
            return jsonify({"Error":"Obrigatório preencher todos os campos"}),400

        placa = dados_editar_veiculo['placa_veiculo'].strip()
        if atualizacao_veiculo.placa_veiculo != placa:
            placa_existe = db_session.query(Veiculo).filter(Veiculo.placa_veiculo == placa).scalar()
            if placa_existe:
                return jsonify({
                    "error": "Está placa já existe na lista de veiculos"
                }), 400

        atualizacao_veiculo.cliente_associado = dados_editar_veiculo['cliente_associado']
        atualizacao_veiculo.marca_veiculo = dados_editar_veiculo['marca_veiculo']
        atualizacao_veiculo.modelo_veiculo = dados_editar_veiculo['modelo_veiculo']
        atualizacao_veiculo.placa_veiculo = dados_editar_veiculo['placa_veiculo'].strip()
        atualizacao_veiculo.ano_fabricacao = dados_editar_veiculo['ano_fabricacao']

        atualizacao_veiculo.save()

        return jsonify({
            "cliente_associado": atualizacao_veiculo.cliente_associado,
            "marca_veiculo": atualizacao_veiculo.marca_veiculo,
            "modelo_veiculo": atualizacao_veiculo.modelo_veiculo,
            "placa_veiculo": atualizacao_veiculo.placa_veiculo,
            "ano_fabricacao": atualizacao_veiculo.ano_fabricacao,
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()



@app.route('/editar_ordem/<int:ordem_id>', methods=["POST"])
def editar_ordem(ordem_id, cliente_associado,veiculo_associado):
    dados_editar_ordem = request.get_json()
    try:
        atualizacao_ordem = db_session.execute(select(Ordem_servico).where(Ordem_servico.id_ordem_servico == ordem_id)).scalars().first()

        if not atualizacao_ordem:
            return jsonify({"Error":'Não se encontrado a ordem de servico'})

        if not "cliente_associado" in dados_editar_ordem or not "veiculo_associado" in dados_editar_ordem  or not "data_abertura" in dados_editar_ordem or not "descricao_servico" in dados_editar_ordem or not "valor_estimado" in dados_editar_ordem:
            return jsonify({"Error":"Obrigatório preencher todos os campos"}),400

        cliente_veiculo = dados_editar_ordem['cliente and veiculo'].strip()
        if atualizacao_ordem.cliente and atualizacao_ordem.veiculo != cliente_veiculo:
            cliente_associado_existe = db_session.query(Ordem_servico).filter(Ordem_servico.cliente_associado == cliente_associado).scalar()
            veiculo_associado_existe = db_session.query(Ordem_servico).filter(Ordem_servico.veiculo_associado == veiculo_associado).scalar()
            if cliente_associado_existe and veiculo_associado_existe:
                return jsonify({
                    "error": "Este cliente e veiculo já existe na lista de ordem de servico"
                }), 400


        dados_editar_ordem.cliente_associado = dados_editar_ordem['cliente_associado'].strip()
        dados_editar_ordem.veiculo_associado = dados_editar_ordem['veiculo_associado'].strip()
        dados_editar_ordem.modelo_veiculo = dados_editar_ordem['modelo_veiculo']
        dados_editar_ordem.data_abertura = dados_editar_ordem['data_abertura']
        dados_editar_ordem.descricao_servico = dados_editar_ordem['descricao_servico']
        dados_editar_ordem.valor_estimado = dados_editar_ordem['valor_estimado']

        atualizacao_ordem.save()

        return jsonify({
            "cliente_associado": atualizacao_ordem.cliente_associado,
            "marca_veiculo_associado": atualizacao_ordem.marca_veiculo_associado,
            "modelo_veiculo": atualizacao_ordem.modelo_veiculo,
            "data_abertura": atualizacao_ordem.data_abertura,
            "descricao_servico": atualizacao_ordem.descricao_servico,
            "valor_estimado": atualizacao_ordem.valor_estimado,
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()

@app.route('/status', methods=['GET'])
def status():
    try:
        status_veiculo = db_session.execute(
            select(Veiculo).where(Veiculo.id_veiculo == Ordem_servico.veiculo).distinc(Veiculo.id_veiculo)).scalars()

        veiculos = db_session.execute(select(Veiculo)).scalars()
        lista_veiculo_pendente = []
        lista_veiculo_andamento = []
        lista_veiculo_concluido = []

        for veiculo in veiculos:
            lista_veiculo_pendente.append(veiculo.serialize_status())

        for vehicle in veiculos:
            if vehicle.id_veiculo not in lista_veiculo_andamento:
                lista_veiculo_concluido.append(vehicle.serialize_status())

        return jsonify({
            "veiculos pendente":lista_veiculo_pendente,
            "veiculos andamento":lista_veiculo_andamento,
            "veiculos concluido":lista_veiculo_concluido
        }),200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)

