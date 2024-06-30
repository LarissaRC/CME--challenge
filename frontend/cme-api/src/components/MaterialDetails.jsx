import React from 'react'

function MaterialDetails({ material }) {
  const combinedHistory = [...material.statuses, ...material.falhas]
  
  combinedHistory.sort((a, b) => new Date(b.data_hora) - new Date(a.data_hora))

  return (
    <div>
      <div>
        <h2>Detalhes do Material</h2>
        <p><strong>ID:</strong> {material.id}</p>
        <p><strong>Nome:</strong> {material.nome}</p>
        <p><strong>Tipo:</strong> {material.tipo}</p>
        <h3>Histórico</h3>
        <ul>
            {combinedHistory.map((item, index) => (
            <li key={index}>
              {item.etapa_nome ? (
                <>
                  <p>{item.etapa_nome}</p>
                  <p>{new Date(item.data_hora).toLocaleString()}</p>
                </>
              ) : (
                <>
                  <p>Falha - {item.descricao}</p>
                  <p>{new Date(item.data_hora).toLocaleString()}</p>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default MaterialDetails