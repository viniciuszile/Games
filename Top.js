import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./top.css";

export default function Top3Jogos() {
  const navigate = useNavigate();
  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);

  const jogos = [
    {
      nome: "Hollow Knight: Silksong",
      imagem:
        "https://raw.githubusercontent.com/viniciuszile/new---fotos/refs/heads/main/silk.png",
    },
    {
      nome: "Clair Obscur: Expedition 33",
      imagem:
        "https://raw.githubusercontent.com/viniciuszile/new---fotos/refs/heads/main/Clair_Obscur_Expedition_33.png",
    },
    {
      nome: "Zelda Breath Of The Wild",
      imagem:
        "https://raw.githubusercontent.com/viniciuszile/new---fotos/refs/heads/main/zelda.png",
    },
  ];

  // Fecha menu clicando fora
  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuAberto(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="top3-wrapper">
      <h1 className="top3-title">🏆 Top 3 Jogos</h1>

      <div className="top3-container">
        {/* TOP 2 */}
        <div className="top3-coluna pos-2">
          <span className="rank prata">2º</span>
          <div className="top3-card">
            <img src={jogos[1].imagem} alt={jogos[1].nome} />
          </div>
        </div>

        {/* TOP 1 */}
        <div className="top3-coluna pos-1">
          <span className="rank ouro">1º</span>
          <div className="top3-card destaque">
            <img src={jogos[0].imagem} alt={jogos[0].nome} />
          </div>
        </div>

        {/* TOP 3 */}
        <div className="top3-coluna pos-3">
          <span className="rank bronze">3º</span>
          <div className="top3-card">
            <img src={jogos[2].imagem} alt={jogos[2].nome} />
          </div>
        </div>
      </div>

      {/* 🎮 BOTÃO FLUTUANTE */}
      <button
        className="filtro-toggle"
        onClick={() => setMenuAberto(!menuAberto)}
      >
        ☰ Menu
      </button>

      {/* 📋 MENU SIMPLES */}
      {menuAberto && (
        <div className="menu-flutuante" ref={menuRef}>
          <h4>Navegação</h4>
          <button
            onClick={() => {
              setMenuAberto(false);
              navigate("/");
            }}
          >
            ⬅ Voltar para Home
          </button>
        </div>
      )}
    </div>
  );
}
