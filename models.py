from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, relationship, declarative_base, sessionmaker

engine = create_engine("sqlite:///banco_mecanica.sqlite")
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Cliente(Base):
    __tablename__ = 'TAB_CLIENTE'
    id_cliente = Column(Integer, primary_key=True)
    nome_cliente = Column(String(40), nullable=False,index=True)
    cpf = Column(String(11), nullable=False, index=True,unique=True)
    telefone = Column(String(11), nullable=False,index=True,unique=True)
    endereco = Column(String(50), nullable=False,index=True)

    def __repr__(self):
        return '<Cliente: {} {} {} {} {} >'.format(self.id_cliente,self.nome_cliente, self.cpf, self.telefone, self.endereco)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_user(self):
        dados_cliente={
            "id_cliente":self.id_cliente,
            "nome_cliente":self.nome_cliente,
            "cpf":self.cpf,
            "telefone":self.telefone,
            "endereco":self.endereco,
        }
        return dados_cliente

class Veiculo(Base):
    __tablename__ = 'TAB_VEICULO'
    id_veiculo = Column(Integer, primary_key=True)
    cliente_associado = Column(Integer, ForeignKey('TAB_CLIENTE.id_cliente'))
    cliente = relationship("Cliente")
    marca_veiculo = Column(String(20), nullable=False,index=True)
    modelo_veiculo = Column(String(30), nullable=False,index=True)
    placa_veiculo = Column(String(7), nullable=False,index=True,unique=True)
    ano_fabricacao = Column(String(8), nullable=False,index=True)

    def __repr__(self):
        return '<Veiculo: {} {} {} {} {} {} '.format(self.id_veiculo,self.cliente,self.marca_veiculo,self.modelo_veiculo,self.placa_veiculo,self.ano_fabricacao)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_veiculo(self):
        dados_veiculo = {
            "id_veiculo":self.id_veiculo,
            "cliente_associado":self.cliente_associado,
            "marca_veiculo":self.marca_veiculo,
            "modelo_veiculo":self.modelo_veiculo,
            "placa_veiculo":self.placa_veiculo,
            "ano_fabricacao":self.ano_fabricacao,
        }
        return dados_veiculo

class Ordem_servico(Base):
    __tablename__ = 'TAB_OREDEM_SERVICO'
    id_ordem_servico = Column(Integer, primary_key=True)
    cliente_associado = Column(Integer, ForeignKey('TAB_CLIENTE.id_cliente'))
    veiculo_associado = Column(Integer, ForeignKey('TAB_VEICULO.id_veiculo'))
    veiculo = relationship('Veiculo')
    data_abertura = Column(String, nullable=False,index=True)
    descricao_servico = Column(String(50), nullable=False,index=True)
    status = Column(String(9), nullable=False,index=True)
    valor_estimado = Column(Float, nullable=False,index=True)

    def __repr__(self):
        return 'Ordem_servico {}'.format(self.id_ordem_servico,self.veiculo,self.data_abertura,self.descricao_servico,self.status,self.valor_estimado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_ordem_servico(self):
        dados_ordem_servico = {
            "id_ordem_servico":self.id_ordem_servico,
            "cliente_associado":self.cliente_associado,
            "veiculo_associado":self.veiculo_associado,
            "data_abertura":self.data_abertura,
            "descricao_servico":self.descricao_servico,
            "status":self.status,
            "valor_estimado":self.valor_estimado,
        }
        return dados_ordem_servico

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
