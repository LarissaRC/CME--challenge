from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
from database import Database
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

db = Database()

@app.route('/api/materials', methods=['GET'])
def get_materials():
    materiais = db.recuperar_materiais()
    return jsonify(materiais), 200

@app.route('/api/material/<int:material_id>', methods=['GET'])
def get_material(material_id):
    material = db.recuperar_material_por_id(material_id)
    if material:
        return jsonify(material), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/api/material', methods=['POST'])
def create_material():
    nome = request.json.get('nome')
    tipo = request.json.get('tipo')
    if not nome or not tipo:
        return jsonify({"message": "Missing required fields"}), 400
    material = db.criar_material(nome, tipo)
    return jsonify(material), 201

@app.route('/api/material/<int:material_id>', methods=['PUT'])
def update_material(material_id):
    nome = request.json.get('nome')
    tipo = request.json.get('tipo')
    material = db.atualizar_material(material_id, nome, tipo)
    if material:
        return jsonify(material), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/api/material/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    result = db.deletar_material(material_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Material not found"}), 404

@app.route('/api/material/<int:material_id>/statuses', methods=['GET'])
def get_statuses(material_id):
    statuses = db.recuperar_status_por_material_id(material_id)
    return jsonify(statuses), 200

@app.route('/api/material/<int:material_id>/status', methods=['POST'])
def create_status(material_id):
    etapa_id = request.json.get('etapa_id')
    data_hora = datetime.now()
    status = db.criar_status(material_id, etapa_id, data_hora)
    return jsonify(status), 201

@app.route('/api/material/<int:material_id>/falhas', methods=['GET'])
def get_falhas(material_id):
    falhas = db.recuperar_falhas_por_material_id(material_id)
    return jsonify(falhas), 200

@app.route('/api/material/<int:material_id>/falha', methods=['POST'])
def create_falha(material_id):
    descricao = request.json.get('descricao')
    etapa_id = request.json.get('etapa_id')
    data_hora = datetime.now()
    falha = db.relatar_falha(descricao, material_id, etapa_id, data_hora)
    return jsonify(falha), 201

@app.route('/api/etapa', methods=['POST'])
def create_etapa():
    nome = request.json.get('nome')
    if not nome:
        return jsonify({"message": "Missing required field 'nome'"}), 400
    etapa = db.criar_etapa(nome)
    return jsonify(etapa), 201

@app.route('/api/etapas', methods=['GET'])
def get_etapas():
    etapas = db.recuperar_etapas()
    return jsonify(etapas), 200

@app.route('/api/material/<int:material_id>/ultimo_estado', methods=['GET'])
def get_ultimo_estado_material(material_id):
    ultimo_estado = db.recuperar_ultimo_estado_material(material_id)
    if ultimo_estado:
        return jsonify(ultimo_estado), 200
    return jsonify({"message": "Nenhum estado encontrado para o material"}), 404

@app.route('/api/distribution_reports', methods=['GET'])
def get_distribution_reports():
    try:
        response = db.relatorio_materiais_distribuidos()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/api/failure_reports', methods=['GET'])
def generate_failure_report():
    try:
        response = db.recuperar_todas_as_falhas()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
