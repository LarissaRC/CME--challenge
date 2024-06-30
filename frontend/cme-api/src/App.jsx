import { useState, useEffect } from 'react'
import './App.css'
import Materials from './components/Materials'
import MaterialForm from './components/MaterialForm';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import * as XLSX from 'xlsx';

function App() {
  const [materials, setMaterials] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentMaterial, setCurrentMaterial] = useState({})
  const [failures, setFailures] = useState([]);

  useEffect(() => {
    fetchMaterials(),
    fetchFailures()
  }, []);

  const fetchMaterials = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/materials");
    const data = await response.json();
    setMaterials(data);
  };

  const fetchFailures = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/failure_reports');
      if (response.ok) {
        const data = await response.json();
        setFailures(data);
      } else {
        console.error('Failed to fetch failures');
      }
    } catch (error) {
      console.error('Error fetching failures:', error);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentMaterial({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (material) => {
    if (isModalOpen) return
    setCurrentMaterial(material)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchMaterials()
    fetchFailures()
  }

  const generateDistributionReport = async () => {
    const response = await fetch("http://127.0.0.1:5000/api/distribution_reports");
    const data = await response.json();

    const doc = new jsPDF();

    const headers = ["ID do Material", "Nome", "Tipo", "Data de Distribuição"];
    const tableData = data.map(item => [
      item.material_id,
      item.nome,
      item.tipo,
      new Date(item.data_distribuicao).toLocaleString()
    ]);

    doc.text("Relatório de Conclusões (Distribuições)", 20, 20);
    doc.autoTable({
      head: [headers],
      body: tableData,
      startY: 30,
    });

    doc.save("Relatorio_Conclusoes_Distribuicoes.pdf");
  };

  const generateExcelReport = () => {
    const wsData = failures.map((failure) => ({
      id: failure.id,
      nome: failure.material.nome,
      tipo: failure.material.tipo,
      'descrição da falha': failure.descricao,
      'etapa em que ocorreu': failure.etapa.nome,
      'data da ocorrência': failure.data_hora,
    }));

    const ws = XLSX.utils.json_to_sheet(wsData);

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Falhas');

    const today = new Date().toISOString().slice(0, 10);
    const fileName = `relatorio_falhas_${today}.xlsx`;

    XLSX.writeFile(wb, fileName);
  };

  return (
    <div>
      {/* Botões de cadastrar e gerar relatórios */}
      <button onClick={openCreateModal}>Cadastrar Material</button>
      <button onClick={generateDistributionReport}>Relatório de Conclusões</button>
      <button onClick={generateExcelReport}>Relatório de Falhas</button>

      <Materials materials={materials} updateMaterial={openEditModal} updateCallback={onUpdate} />

      {isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <MaterialForm existingMaterial={currentMaterial} updateCallback={onUpdate} />
        </div>
      </div>
      }

    </div>
  )
}

export default App
