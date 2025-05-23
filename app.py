from flask import Flask, request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models import *
app = Flask(__name__)

app.config['SECRET_KEY'] = '<KEY>'


@app.route('/novo_cliente', methods=['POST'])
def cadastro_cliente():
    try:
        """
            Cadastro dos clientes da mecânica
               
            Endopoint:  
                - POST,novo_cliente
                
            Parâmetros:
                -Não tem
            
            Resposta:
                {
                    "nome_cliente":"Laura Ferreira",
                    "cpf":"1542551238451",
                    "telefone":"123",
                    "endereco":"Rua Naomi Sanomiya n211"
                }
                
            Erros possíveis:
                -Se tiver um cpf ou um telefone igual irá dar erro
                -se não tiver no formato dará erro 
        
        """

        dados_cliente = request.get_json()

        if not dados_cliente['nome_cliente'] or not dados_cliente['cpf'] or not dados_cliente['telefone'] or not dados_cliente['endereco']:
            return jsonify({'Obritório preencher todos os campos'})

        else:
            form_cadastro_cliente = Cliente(
                nome_cliente=dados_cliente['nome_cliente'],
                cpf=dados_cliente['cpf'],
                telefone=dados_cliente['telefone'],
                endereco=dados_cliente['endereco']
            )
            form_cadastro_cliente.save()

        return jsonify({
            "MENSAGEM": "Cliente cadastrado com sucesso!",
            "Nome": form_cadastro_cliente.nome_cliente,
            "CPF": form_cadastro_cliente.cpf.strip(),
            "Telefone": form_cadastro_cliente.telefone.strip(),
            "Endereço": form_cadastro_cliente.endereco
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })
    except IntegrityError:
        return jsonify({
            "error": "Este cpf e telefone já existe na lista de clientes"
        }), 400

#proteger
@app.route('/clientes', methods=["GET"])
def clientes():

    try:
        """
            Lista dos cliente da mecânica

            Endopoint:  
                - GET,clientes
                
            Parâmetros:
                -
            Resposta:
            exemplo de uma resposta da lista
                {
                    "nome_cliente":"Laura Ferreira",
                    "cpf":"1542551238451",
                    "telefone":"123",
                    "endereco":"Rua Naomi Sanomiya n211"
                }

            Erros possíveis:
                -se não tiver no formato dará erro 

        """

        sql_clientes = db_session.execute(select(Cliente)).scalars().all()
        lista_clientes = []
        for cliente in sql_clientes:
            lista_clientes.append(cliente.serialize_user())
        return jsonify(lista_clientes)

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })
#proteger
@app.route('/novo_veiculo', methods=['POST'])
def cadastro_veiculos():
    try:
        """
                Cadastro dos veículos da mecânica

                Endopoint:  
                    - POST,novo_veiculo
                    
                Parâmetros:
                    -Não tem

                Resposta:
                {
                    "cliente_associado": "1",
                    "marca_veiculo": "Civic",
                    "modelo_veiculo": "g10",
                    "placa_veiculo": "PT123",
                    "ano_fabricacao": "2021",
                    "status":"pendente"
                }

                Erros possíveis:
                    -Se a placa do veiculo tiver outro igual irá dar erro
                    -se não tiver no formato dará erro 

        """

        dados_veiculo = request.get_json()
        if not dados_veiculo['cliente_associado'] or not dados_veiculo['marca_veiculo'] or not dados_veiculo['modelo_veiculo'] or not dados_veiculo['placa_veiculo'] or not dados_veiculo['ano_fabricacao']:
            return jsonify({'Obritório preencher todos os campos'})
        else:
            form_cadastro_veiculo = Veiculo(
                cliente_associado=dados_veiculo['cliente_associado'],
                marca_veiculo=dados_veiculo['marca_veiculo'],
                modelo_veiculo=dados_veiculo['modelo_veiculo'],
                placa_veiculo=dados_veiculo['placa_veiculo'],
                ano_fabricacao=dados_veiculo['ano_fabricacao'],

            )

            form_cadastro_veiculo.save()

        return jsonify({
            "MENSAGEM": "Veiculo cadastrado com sucesso!",
            " Cliente associado": form_cadastro_veiculo.cliente_associado,
            " Marca do veiculo": form_cadastro_veiculo.marca_veiculo,
            " Modelo do veículo": form_cadastro_veiculo.modelo_veiculo,
            " Placa do veículo": form_cadastro_veiculo.placa_veiculo.strip(),
            " Ano de fabricacao": form_cadastro_veiculo.ano_fabricacao
        })

    except ValueError:
        return jsonify({"mensagem": "Cliente não encontrado."}), 404

    except IntegrityError:
        return jsonify({
            "error": "Erro essa placa ja existe na lista de veiculos"
        })

#proteger
@app.route('/veiculos', methods=["GET"])
def veiculos():

    try:
        """
            Lista dos veículos da mecânica

            Endopoint:  
                - GET,veiculos
                
            Parâmetros:
                -Não tem

            Resposta:
            Uma das respostas
            {
                "cliente_associado": "1",
                "marca_veiculo": "Civic",
                "modelo_veiculo": "g10",
                "placa_veiculo": "PT123",
                "ano_fabricacao": "2021",
                "status":"pendente"
            }

            Erros possíveis:
                -se não tiver no formato dará erro 

        """

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

#proteger
@app.route('/nova_ordem_servico', methods=['POST'])
def cadastro_ordem_servico():

    try:
        """
            Cadastro de ordem de serviço da mecânica

            Endopoint:  
                - POST,nova_ordem_servico
                
            Parâmetros:
                -Não tem

            Resposta:
            {
                "cliente_associado" : 3,
                "veiculo_associado" : 3,
                "data_abertura" :"10/01/2025",
                "descricao_servico" :"motor",
                "valor_estimado":"5689",
                "status": "concluido"
            }

            Erros possíveis:
                -Se tiver um cliente ou veiculo associado igual outri  irá dar erro
                -se não tiver no formato dará erro 

        """

        dados_servico = request.get_json()
        if not dados_servico['cliente_associado'] or not dados_servico['data_abertura'] or not dados_servico[
            'descricao_servico'] or not dados_servico['status'] or not dados_servico['valor_estimado']:
            return jsonify({'Obritório preencher todos os campos'})
        else:
            form_ordem_servico = Ordem_servico(
                cliente_associado=dados_servico[ 'cliente_associado'],
                veiculo_associado=dados_servico[ 'veiculo_associado'],
                data_abertura=dados_servico[ 'data_abertura'],
                descricao_servico=dados_servico[ 'descricao_servico'],
                status=dados_servico['status'],
                valor_estimado=dados_servico['valor_estimado'],

            )
            form_ordem_servico.save()

        return jsonify({
            "MENSAGEM": "Ordem de serviço cadastrado com sucesso!",
            "Cliente associado": form_ordem_servico.cliente_associado,
            "Veiculo associado": form_ordem_servico.veiculo_associado,
            "Data de abertura": form_ordem_servico.data_abertura,
            "Descrição": form_ordem_servico.descricao_servico,
            "Status": form_ordem_servico.status,
            "Valor": form_ordem_servico.valor_estimado
        })

    except ValueError:
        return jsonify({
            'Error': "Error"
        })
    except IntegrityError:
        return jsonify({
                "error": "Este cliente ou veiculo associado já existem na lista de ordem de servico"
            }), 400

#proteger
@app.route('/ordem_servico', methods=["GET"])
def ordem_servico():
    try:
        """
            Lista da ordem de serviço da mecânica

            Endopoint:  
                - GET,ordem_servico

            Parâmetros:
                -Não tem

            Resposta:
            {
                "cliente_associado" : 3,
                "veiculo_associado" : 3,
                "data_abertura" :"10/01/2025",
                "descricao_servico" :"motor",
                "valor_estimado":"5689",
                "status": "concluido"
            }

            Erros possíveis:
                -se não tiver no formato dará erro 

        """

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

#proteger
@app.route('/editar_cliente/<int:cliente_id>', methods=["POST"])
def editar_cliente(cliente_id):
    dados_editar_cliente = request.get_json()
    try:
        """
            Editar a lista cliente

            Endopoint:  
                - POST,nova_ordem_servico,<int:cliente_id>

            Parâmetros:
                -<int:cliente_id>: ira pegar diretamente do id para a atualização 

            Resposta:
            {
                "cliente_associado" : 3,
                "veiculo_associado" : 3,
                "data_abertura" :"10/01/2025",
                "descricao_servico" :"motor",
                "valor_estimado":"5689",
                "status": "concluido"
            }

            Erros possíveis:
                -Se tiver um cliente ou veiculo associado igual outri  irá dar erro
                -se não tiver no formato dará erro 

                """

        atualizacao_cliente = db_session.execute(select(Cliente).where(Cliente.id_cliente == cliente_id)).scalars().first()

        if not atualizacao_cliente:
            return jsonify({"Error":'Não se encontra o cliente'})

        if not "nome_cliente" in dados_editar_cliente or not "cpf" in dados_editar_cliente  or not "telefone" in dados_editar_cliente or not "endereco" in dados_editar_cliente:
            return jsonify({"Error":"Obrigatório preencher todos os campos"}),400

        cpf = dados_editar_cliente['cpf'].strip()
        if atualizacao_cliente.cpf != cpf:
            cpf_existe = db_session.query(Cliente).filter(Cliente.cpf == cpf).scalar()
            if cpf_existe:
                return jsonify({
                    "error": "Este CPF já existe na lista de clientes"
                }), 400

        telefone = dados_editar_cliente['telefone'].strip()
        if atualizacao_cliente.telefone != telefone:
            telefone_existe = db_session.query(Cliente).filter(Cliente.telefone == telefone).scalar()
            if telefone_existe:
                return jsonify({
                    "error": "Este telefone já existe na lista de clientes"
                }), 400

        atualizacao_cliente.nome_cliente = dados_editar_cliente['nome_cliente']
        atualizacao_cliente.cpf = dados_editar_cliente['cpf'].strip().strip()
        atualizacao_cliente.telefone = dados_editar_cliente['telefone'].strip()
        atualizacao_cliente.endereco = dados_editar_cliente['endereco']

        atualizacao_cliente.save()

        return jsonify({
            "MENSAGEM":"Editado a lista cliente com sucesso!",
            "Nome": atualizacao_cliente.nome_cliente,
            "CPF": atualizacao_cliente.cpf,
            "Telefone": atualizacao_cliente.telefone,
            "Endereço": atualizacao_cliente.endereco,
        }), 201

    except IntegrityError:
        return jsonify({
            "error": "Este cpf e telefone já existe na lista de clientes"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()


#proteger
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
            "MENSAGEM":"Editado a lista veiculo com sucesso!",
            "Cliente associado": atualizacao_veiculo.cliente_associado,
            "Marca do veículo": atualizacao_veiculo.marca_veiculo,
            "Modelo do veículo": atualizacao_veiculo.modelo_veiculo,
            "Placa do veículo": atualizacao_veiculo.placa_veiculo,
            "Ano de fabricação": atualizacao_veiculo.ano_fabricacao,
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        db_session.close()


#proteger
@app.route('/editar_ordem/<int:ordem_id>', methods=["POST"])
def editar_ordem(ordem_id):
    dados_editar_ordem = request.get_json()

    try:
        atualizacao_ordem = db_session.execute(select(Ordem_servico).where(Ordem_servico.id_ordem_servico == ordem_id)).scalars().first()

        if not atualizacao_ordem:
            return jsonify({"Error":'Não se encontrado a ordem de servico'})

        if not "cliente_associado" in dados_editar_ordem or not "veiculo_associado" in dados_editar_ordem  or not "data_abertura" in dados_editar_ordem or not "descricao_servico" in dados_editar_ordem or not "valor_estimado" in dados_editar_ordem or not "status":
            return jsonify({"Error":"Obrigatório preencher todos os campos"}),400

        cliente_associado = dados_editar_ordem['cliente_associado']
        if atualizacao_ordem.cliente_associado != cliente_associado:
            cliente_associado_existe = db_session.query(Ordem_servico).filter(Ordem_servico.cliente_associado == cliente_associado).scalar()
            if cliente_associado_existe:
                return jsonify({
                    "error": "Este cliente já existe na lista de orde de serviço"
                }), 400

        veiculo_associado = dados_editar_ordem['veiculo_associado']
        if atualizacao_ordem.veiculo_associado != veiculo_associado:
            veiculo_associado_existe = db_session.query(Cliente).filter(Cliente.telefone == veiculo_associado).scalar()
            if veiculo_associado_existe:
                return jsonify({
                    "error": "Este veiculo já existe na lista de ordem de serviço"
                }), 400

        atualizacao_ordem.cliente_associado = dados_editar_ordem['cliente_associado']
        atualizacao_ordem.veiculo_associado = dados_editar_ordem['veiculo_associado']
        atualizacao_ordem.modelo_veiculo = dados_editar_ordem['modelo_veiculo']
        atualizacao_ordem.data_abertura = dados_editar_ordem['data_abertura']
        atualizacao_ordem.descricao_servico = dados_editar_ordem['descricao_servico']
        atualizacao_ordem.valor_estimado = float(dados_editar_ordem['valor_estimado'])
        atualizacao_ordem.status = dados_editar_ordem['status']

        atualizacao_ordem.save()

        return jsonify({
            "MENSAGEM":"Editado a lista ordem de servico com sucesso!",
            "cliente_associado": atualizacao_ordem.cliente_associado,
            "veiculo_associado": atualizacao_ordem.veiculo_associado,
            "modelo_veiculo": atualizacao_ordem.modelo_veiculo,
            "data_abertura": atualizacao_ordem.data_abertura,
            "descricao_servico": atualizacao_ordem.descricao_servico,
            "valor_estimado": atualizacao_ordem.valor_estimado,
            "status": atualizacao_ordem.status,
        }), 201

    except IntegrityError:
        return jsonify({
                "error": "Este cliente ou veiculo associado já existem na lista de ordem de servico"
            }), 400

    finally:
        db_session.close()

@app.route('/status/<status02>', methods=["GET"])
def status(status02):
    try:
        sql_status = select(Ordem_servico).where(Ordem_servico.status == status02)
        resultado_status = db_session.execute(sql_status).scalars()
        lista_status = []
        for status in resultado_status:
            lista_status.append(status.serialize_ordem_servico())
        return jsonify({
            "LISTA":lista_status
        })

    except ValueError:
        return jsonify({
            'Error': "Erro"
        })
    finally:
        db_session.close()

if __name__ == '__main__':
    app.run(debug=True)

