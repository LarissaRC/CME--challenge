import { useState } from 'react'
import React from 'react'
import MaterialDetails from './MaterialDetails'

function Materials({ materials, updateMaterial, updateCallback }) {
    const [selectedMaterial, setSelectedMaterial] = useState(null)
    const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false)

    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/api/material/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    const openDetailsModal = async (material) => {
        const response = await fetch(`http://127.0.0.1:5000/api/material/${material.id}/statuses`)
        const statuses = await response.json()
        const responseFalhas = await fetch(`http://127.0.0.1:5000/api/material/${material.id}/falhas`)
        const falhas = await responseFalhas.json()

        setSelectedMaterial({ ...material, statuses, falhas })
        setIsDetailsModalOpen(true)
    }

    const closeDetailsModal = () => {
        setIsDetailsModalOpen(false)
        setSelectedMaterial(null)
    }

  return (
    <div>
        <h2>Materiais</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {
                materials.map((material) => (
                    <tr key={material.id}>
                        <td>{material.id}</td>
                        <td>{material.nome}</td>
                        <td>{material.tipo}</td>
                        <td>{material.ultimo_estado ? material.ultimo_estado.valor : "---"}</td>
                        <td>
                            <button onClick={() => openDetailsModal(material)}>Detalhes</button>
                            <button onClick={() => updateMaterial(material)}>Atualizar</button>
                            <button onClick={() => onDelete(material.id)}>Deletar</button>
                        </td>
                    </tr>
                ))
                }
            </tbody>
        </table>

        {isDetailsModalOpen && <div className="modal">
            <div className="modal-content">
                <span className="close" onClick={closeDetailsModal}>&times;</span>
                {selectedMaterial && <MaterialDetails material={selectedMaterial} />}
            </div>
        </div>
        }
    </div>
  )
}

export default Materials