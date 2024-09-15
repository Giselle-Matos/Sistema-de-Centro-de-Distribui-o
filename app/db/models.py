# app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class Categoria(Base):
    __tablename__ = 'categorias'
    categoria_id = Column(Integer, primary_key=True)
    nome_categoria = Column(String, unique=True, nullable=False)
    produtos = relationship("Produto", back_populates="categoria")

class Produto(Base):
    __tablename__ = 'produtos'
    pid = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'))
    quantidade_minima = Column(Integer, nullable=False)
    peso = Column(Float)  # Adicionado para cálculo de peso total
    categoria = relationship("Categoria", back_populates="produtos")
    estoque = relationship("Estoque", back_populates="produto")
    historico = relationship("HistoricoEntradaSaida", back_populates="produto")
    fornecedores = relationship("ProdutoFornecedor", back_populates="produto")

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    fornecedor_id = Column(Integer, primary_key=True)
    nome_fornecedor = Column(String, unique=True, nullable=False)
    produtos_fornecedores = relationship("ProdutoFornecedor", back_populates="fornecedor")
    historico = relationship("HistoricoEntradaSaida", back_populates="fornecedor")

class ProdutoFornecedor(Base):
    __tablename__ = 'produtos_fornecedores'
    pid = Column(Integer, ForeignKey('produtos.pid'), primary_key=True)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.fornecedor_id'), primary_key=True)
    preco = Column(Float, nullable=False)
    produto = relationship("Produto", back_populates="fornecedores")
    fornecedor = relationship("Fornecedor", back_populates="produtos_fornecedores")

class Estoque(Base):
    __tablename__ = 'estoque'
    estoque_id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('produtos.pid'), nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    produto = relationship("Produto", back_populates="estoque")

class TipoOperacaoEnum(PyEnum):
    ENTRADA = "entrada"
    SAIDA = "saída"

class HistoricoEntradaSaida(Base):
    __tablename__ = 'historico_entrada_saida'
    historico_id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('produtos.pid'), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.fornecedor_id'))
    quantidade = Column(Integer, nullable=False)
    tipo_operacao = Column(Enum(TipoOperacaoEnum), nullable=False)
    data_operacao = Column(Date, nullable=False)
    data_pedido = Column(Date)
    data_entrega = Column(Date)
    loja_destino = Column(String)
    transportadora = Column(String)
    peso_total = Column(Float)
    produto = relationship("Produto", back_populates="historico")
    fornecedor = relationship("Fornecedor", back_populates="historico")
