from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from models import Base, Material, Etapa, Falha, Status

class Database:
    def __init__(self, db_url='sqlite:///materiais.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.create_default_etapas()

    def create_default_etapas(self):
        default_etapas = ["Recebimento", "Lavagem", "Preparo", "Distribuição"]
        session = self.Session()
        for nome in default_etapas:
            if not session.query(Etapa).filter_by(nome=nome).first():
                new_etapa = Etapa(nome=nome)
                session.add(new_etapa)
        session.commit()
        session.close()

    def criar_material(self, nome, tipo):
        session = self.Session()
        new_material = Material(nome=nome, tipo=tipo)
        session.add(new_material)
        session.commit()
        # Carrega o objeto novamente para garantir que está na sessão
        session.refresh(new_material)
        material_dict = new_material.to_dict()
        session.close()
        return material_dict

    def recuperar_materiais(self):
        session = self.Session()
        materiais = session.query(Material).all()
        
        json_materiais = []
        for material in materiais:
            material_dict = material.to_dict()

            # Recupera o último estado do material
            ultimo_estado = self.recuperar_ultimo_estado_material(material.id)
            if ultimo_estado:
                material_dict["ultimo_estado"] = ultimo_estado

            json_materiais.append(material_dict)

        session.close()
        return json_materiais
    
    def recuperar_material_por_id(self, material_id):
        session = self.Session()
        material = session.query(Material).get(material_id)
        if not material:
            session.close()
            return None
        material_dict = material.to_dict()
        session.close()
        return material_dict
    
    def deletar_material(self, material_id):
        session = self.Session()
        material = session.query(Material).get(material_id)
        if not material:
            session.close()
            return None
        
        # Deletar os status relacionados
        session.query(Status).filter_by(material_id=material_id).delete()
        
        # Deletar as falhas relacionadas
        session.query(Falha).filter_by(material_id=material_id).delete()

        # Deletar o material
        session.delete(material)
        session.commit()
        session.close()
        return {"message": "Material e seus registros relacionados foram deletados com sucesso."}

    def criar_status(self, material_id, etapa_id, data_hora):
        session = self.Session()
        new_status = Status(material_id=material_id, etapa_id=etapa_id, data_hora=data_hora)
        session.add(new_status)
        session.commit()
        # Carrega o objeto novamente para garantir que está na sessão
        session.refresh(new_status)
        session.close()
        return new_status.to_dict()
    
    def recuperar_status_por_material_id(self, material_id):
        session = self.Session()
        statuses = (
            session.query(Status, Etapa.nome)
            .join(Etapa, Status.etapa_id == Etapa.id)
            .filter(Status.material_id == material_id)
            .all()
        )
        
        json_statuses = [
            {
                "id": status.Status.id,
                "material_id": status.Status.material_id,
                "etapa_id": status.Status.etapa_id,
                "etapa_nome": status.nome,  # Nome da etapa
                "data_hora": status.Status.data_hora.isoformat()
            } 
            for status in statuses
        ]
        session.close()
        return json_statuses

    def criar_etapa(self, nome):
        session = self.Session()
        new_etapa = Etapa(nome=nome)
        session.add(new_etapa)
        session.commit()
        # Carrega o objeto novamente para garantir que está na sessão
        session.refresh(new_etapa)
        session.close()
        return new_etapa.to_dict()
    
    def recuperar_etapas(self):
        session = self.Session()
        etapas = session.query(Etapa).all()
        json_etapas = [etapa.to_dict() for etapa in etapas]
        session.close()
        return json_etapas

    def atualizar_material(self, material_id, nome=None, tipo=None):
        session = self.Session()
        material = session.query(Material).get(material_id)
        if not material:
            session.close()
            return None
        if nome:
            material.nome = nome
        if tipo:
            material.tipo = tipo
        session.commit()
        updated_material = material.to_dict()
        session.close()
        return updated_material

    def relatar_falha(self, descricao, material_id, etapa_id, data_hora):
        session = self.Session()
        new_falha = Falha(descricao=descricao, material_id=material_id, etapa_id=etapa_id, data_hora=data_hora)
        session.add(new_falha)
        session.commit()
        # Carrega o objeto novamente para garantir que está na sessão
        session.refresh(new_falha)
        session.close()
        return new_falha.to_dict()
    
    def recuperar_falhas_por_material_id(self, material_id):
        session = self.Session()
        falhas = session.query(Falha).filter_by(material_id=material_id).all()
        json_falhas = [falha.to_dict() for falha in falhas]
        session.close()
        return json_falhas
    
    def recuperar_ultimo_estado_material(self, material_id):
        session = self.Session()

        # Recuperar o último status
        ultimo_status = session.query(Status).filter_by(material_id=material_id).order_by(desc(Status.data_hora)).first()

        # Recuperar a última falha
        ultima_falha = session.query(Falha).filter_by(material_id=material_id).order_by(desc(Falha.data_hora)).first()

        session.close()

        # Verifica qual foi o último estado registrado
        if ultimo_status and (not ultima_falha or ultimo_status.data_hora >= ultima_falha.data_hora):
            etapa = session.query(Etapa).get(ultimo_status.etapa_id)
            return {
                "tipo": "etapa",
                "valor": etapa.nome if etapa else None
            }
        elif ultima_falha and (not ultimo_status or ultima_falha.data_hora > ultimo_status.data_hora):
            return {
                "tipo": "falha",
                "valor": "Falha"
            }
        else:
            return None
    
    def relatorio_materiais_distribuidos(self):
        session = self.Session()

        results = (
            session.query(Material, Status, Etapa)
            .join(Status, Material.id == Status.material_id)
            .join(Etapa, Status.etapa_id == Etapa.id)
            .filter(Etapa.nome == "Distribuição")
            .all()
        )
        
        response = []
        for material, status, etapa in results:
            response.append({
                "material_id": material.id,
                "nome": material.nome,
                "tipo": material.tipo,
                "data_distribuicao": status.data_hora.isoformat()
            })

        session.close()
        return response
    
    def recuperar_todas_as_falhas(self):
        session = self.Session()
        falhas = (
            session.query(Falha, Material, Etapa)
            .join(Material, Falha.material_id == Material.id)
            .join(Etapa, Falha.etapa_id == Etapa.id)
            .all()
        )
        json_falhas = [
            {
                "id": falha.id,
                "descricao": falha.descricao,
                "data_hora": falha.data_hora.isoformat(),
                "material": {
                    "id": material.id,
                    "nome": material.nome,
                    "tipo": material.tipo
                },
                "etapa": {
                    "id": etapa.id,
                    "nome": etapa.nome
                }
            }
            for falha, material, etapa in falhas
        ]
        session.close()
        return json_falhas