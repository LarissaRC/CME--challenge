import { useState, useEffect } from 'react'
import React from 'react'

function MaterialForm({ existingMaterial = {}, updateCallback }) {
  const [nome, setNome] = useState(existingMaterial.nome || "");
  const [tipo, setTipo] = useState(existingMaterial.tipo || "");
  const [descricao, setDescricao] = useState("")
  const [etapas, setEtapas] = useState([])
  const [selectedEtapa, setSelectedEtapa] = useState(null)
  const [showFailForm, setShowFailForm] = useState(false)
  const [showEtapaForm, setShowEtapaForm] = useState(false)

  const updating = Object.entries(existingMaterial).length !== 0

  useEffect(() => {
    if (updating) {
      fetchEtapas()
    }
  }, [updating])

  const fetchEtapas = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/etapas");
    const data = await response.json();
    setEtapas(data);
  };

  const onSubmit = async (e) => {
    e.preventDefault()

    const data = {
      nome,
      tipo
    }
    const url = "http://127.0.0.1:5000/api/material" + (updating ? `/${existingMaterial.id}` : "")
    const options = {
        method: updating ? "PUT" : "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    const response = await fetch(url, options)
    if (response.status !== 201 && response.status !== 200) {
        const data = await response.json()
        alert(data.message)
    } else {
        updateCallback()
    }
  }

  const onFailSubmit = async (e) => {
    e.preventDefault()
    const data = { descricao, etapa_id: existingMaterial.id }
    const url = `http://127.0.0.1:5000/api/material/${existingMaterial.id}/falha`
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }
    const response = await fetch(url, options)
    if (response.status === 201) {
        updateCallback()
    } else {
        const data = await response.json()
        alert(data.message)
    }
  }

  const onEtapaSubmit = async (e) => {
    e.preventDefault()
    const data = { etapa_id: selectedEtapa }
    const url = `http://127.0.0.1:5000/api/material/${existingMaterial.id}/status`
    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }
    const response = await fetch(url, options)
    if (response.status === 201) {
        updateCallback()
    } else {
        const data = await response.json()
        alert(data.message)
    }
  }

  return (
    <div>
      {!showFailForm && !showEtapaForm && (
        <form onSubmit={onSubmit}>
          <div>
            <label htmlFor="nome">Nome:</label>
            <input
              type="text"
              id="nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="tipo">Tipo:</label>
            <input
              type="text"
              id="tipo"
              value={tipo}
              onChange={(e) => setTipo(e.target.value)}
            />
          </div>
          <button type="submit">{updating ? "Atualizar" : "Cadastrar"}</button>
          {updating && (
            <div>
              <button type="button" onClick={() => setShowFailForm(true)}>Relatar Falha</button>
              <button type="button" onClick={() => setShowEtapaForm(true)}>Atualizar Etapa</button>
            </div>
          )}
        </form>
      )}

      {showFailForm && (
        <form onSubmit={onFailSubmit}>
          <div>
            <label htmlFor="descricao">Descrição da Falha:</label>
            <input
              type="text"
              id="descricao"
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
            />
          </div>
          <button type="submit">Relatar Falha</button>
          <button type="button" onClick={() => setShowFailForm(false)}>Voltar</button>
        </form>
      )}

      {showEtapaForm && (
        <form onSubmit={onEtapaSubmit}>
          <div>
            <label>Selecione a Etapa:</label>
            {etapas.map((etapa) => (
              <div key={etapa.id}>
                <input
                  type="radio"
                  id={`etapa-${etapa.id}`}
                  name="etapa"
                  value={etapa.id}
                  onChange={(e) => setSelectedEtapa(e.target.value)}
                />
                <label htmlFor={`etapa-${etapa.id}`}>{etapa.nome}</label>
              </div>
            ))}
          </div>
          <button type="submit">Atualizar Etapa</button>
          <button type="button" onClick={() => setShowEtapaForm(false)}>Voltar</button>
        </form>
      )}
    </div>
  )
}

export default MaterialForm