import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./Home_2025.css";

function Home_2025() {
  const navigate = useNavigate();

  const [jogos, setJogos] = useState([]);
  const [flipped, setFlipped] = useState({});
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);
  const [filtro, setFiltro] = useState("todos");
  const [ordenacao, setOrdenacao] = useState(null);
  const [menuAberto, setMenuAberto] = useState(false);

  const menuRef = useRef(null);

  /* ========================= */
  /* 📥 Carregar JSON          */
  /* ========================= */
  useEffect(() => {
    fetch(
      "https://raw.githubusercontent.com/viniciuszile/Games/refs/heads/main/public/Data/jogos_2025.json"
    )
      .then((res) => {
        if (!res.ok) throw new Error("Erro ao buscar os dados");
        return res.json();
      })
      .then((data) => {
        setJogos(data);
        setLoading(false);
      })
      .catch(() => {
        setErro("Falha ao carregar os jogos.");
        setLoading(false);
      });
  }, []);

  /* ========================= */
  /* 🔄 Flip                  */
  /* ========================= */
  function toggleFlip(index) {
    setFlipped((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  }

  /* ========================= */
  /* 🔤 Utilidades             */
  /* ========================= */
  function removerAcentos(str) {
    if (typeof str !== "string") return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  function isConcluido(situacao) {
    const n = removerAcentos(situacao || "").toLowerCase().trim();
    return n === "concluido";
  }

  function isDropado(situacao) {
    const n = removerAcentos(situacao || "").toLowerCase().trim();
    return n === "dropado";
  }

  function extrairHoras(jogo) {
    const valor = jogo["Horas De Jogo"]?.trim() || "";
    const match = valor.match(/\d+/);
    return match ? parseInt(match[0], 10) : 0;
  }

  function extrairRank(jogo) {
    const r = parseInt(jogo.Rank_25, 10);
    return isNaN(r) ? 999 : r;
  }

  /* ========================= */
  /* 🔃 Ordenações             */
  /* ========================= */
  function ordenarPorNome(a, b) {
    return (a.nome || "").localeCompare(b.nome || "");
  }

  function ordenarPorTempo(a, b) {
    return extrairHoras(a) - extrairHoras(b);
  }

  function ordenarPorRankAsc(a, b) {
    return extrairRank(a) - extrairRank(b);
  }

  function ordenarPorRankDesc(a, b) {
    return extrairRank(b) - extrairRank(a);
  }

  /* ========================= */
  /* 🎯 Filtros                */
  /* ========================= */
  let jogosFiltrados = jogos.filter((jogo) => {
    if (
      (ordenacao === "rank-asc" || ordenacao === "rank-desc") &&
      extrairRank(jogo) >= 999
    ) {
      return false;
    }

    if (filtro === "concluidos") return isConcluido(jogo.situacao);
    if (filtro === "dropado") return isDropado(jogo.situacao);
    if (filtro === "em-andamento")
      return !isConcluido(jogo.situacao) && !isDropado(jogo.situacao);

    return true;
  });

  if (ordenacao) {
    jogosFiltrados = [...jogosFiltrados];

    if (ordenacao === "nome-asc") jogosFiltrados.sort(ordenarPorNome);
    if (ordenacao === "nome-desc")
      jogosFiltrados.sort((a, b) => ordenarPorNome(b, a));

    if (ordenacao === "tempo-asc") jogosFiltrados.sort(ordenarPorTempo);
    if (ordenacao === "tempo-desc")
      jogosFiltrados.sort((a, b) => ordenarPorTempo(b, a));

    if (ordenacao === "rank-asc") jogosFiltrados.sort(ordenarPorRankAsc);
    if (ordenacao === "rank-desc") jogosFiltrados.sort(ordenarPorRankDesc);
  }

  /* ========================= */
  /* ❌ Fechar menu fora       */
  /* ========================= */
  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuAberto(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (loading) return <p style={{ color: "#fff" }}>Carregando...</p>;
  if (erro) return <p style={{ color: "red" }}>{erro}</p>;

  /* ========================= */
  /* 🧮 Contadores             */
  /* ========================= */
  const totalConcluidos = jogos.filter((j) => isConcluido(j.situacao)).length;
  const totalDropados = jogos.filter((j) => isDropado(j.situacao)).length;
  const totalEmAndamento = jogos.length - totalConcluidos - totalDropados;

  /* ========================= */
  /* 🖥️ Render                 */
  /* ========================= */
  return (
    <>
      <header className="status-header">
        <div>🎯 <strong>Zerados:</strong> {totalConcluidos}</div>
        <div>🔥 <strong>Em andamento:</strong> {totalEmAndamento}</div>
        <div>❌ <strong>Dropado:</strong> {totalDropados}</div>
        <div>📦 <strong>Total:</strong> {jogos.length}</div>
      </header>

      <button
        className="filtro-toggle"
        onClick={() => setMenuAberto(!menuAberto)}
      >
        🎮 Filtros
      </button>

      {menuAberto && (
        <div className="menu-flutuante" ref={menuRef}>
            <h4>🧭 Navegação</h4>
            <div className="menu-grid">
              <button onClick={() => navigate("/")}>🏠 2026</button>
              <button onClick={() => navigate("/top3")}>🏆 Top 3 (2025)</button>

            </div>

            <h4>🔍 Filtrar por</h4>
            <div className="menu-grid">
              <button onClick={() => setFiltro("todos")}>📋 Todos</button>
              <button onClick={() => setFiltro("concluidos")}>✅ Concluídos</button>
              <button onClick={() => setFiltro("em-andamento")}>⏳ Em andamento</button>
              <button onClick={() => setFiltro("dropado")}>🗑️ Dropado</button>
            </div>

            <h4>↕️ Ordenar por</h4>
            <div className="menu-grid">
              <button onClick={() => setOrdenacao("nome-asc")}>🔤 Nome</button>
              <button onClick={() => setOrdenacao("tempo-asc")}>⏱️ Tempo</button>
              <button onClick={() => setOrdenacao("rank-asc")}>🏆 Rank 2025</button>
              <button onClick={() => setOrdenacao(null)}>🧹 Limpar</button>
    </div>

          <button onClick={() => setOrdenacao(null)}>Limpar</button>
        </div>
      )}

      <div className="container_card">
        {jogosFiltrados.map((jogo, index) => {
          const dropado = isDropado(jogo.situacao);
          const classeEstado = isConcluido(jogo.situacao)
            ? "concluido"
            : dropado
            ? "dropado"
            : "em-andamento";

          return (
            <div
              key={index}
              className={`card ${classeEstado} ${
                flipped[index] ? "flipped" : ""
              }`}
              onClick={() => toggleFlip(index)}
            >
              <div className="card-front">
                <img src={jogo.imagem} alt={jogo.nome} />
              </div>

              <div className="card-back">
                {dropado ? (
                  <>
                    <p className="campo plataforma"><strong>Plataforma:</strong> {jogo.plataforma || "-"}</p>
                    <p className="campo inicio"><strong>Início:</strong> {jogo.inicio || "-"}</p>
                    <p className="campo motivo"><strong>Motivo:</strong> {jogo.Motivo || "-"}</p>
                    <p className="campo plano"><strong>Plano de ação:</strong> {jogo["Plano de ação"] || "-"}</p>
                  </>
                ) : (
                  <>
                    <p className="campo plataforma"><strong>Plataforma:</strong> {jogo.plataforma || "-"}</p>
                    <p className="campo inicio"><strong>Início:</strong> {jogo.inicio || "-"}</p>
                    <p className="campo termino"><strong>Término:</strong> {jogo.termino || "-"}</p>
                    <p className="campo situacao"><strong>Situação:</strong> {jogo.situacao || "-"}</p>
                    <p className="campo horas"><strong>Horas:</strong> {extrairHoras(jogo)}h</p>
                    <p className="campo dificuldade"><strong>Dificuldade:</strong> {jogo.dificuldade || "-"}</p>
                    <p className="campo replay"><strong>Replay:</strong> {jogo.replay || "-"}</p>
                    <p className="campo nota"><strong>Nota:</strong> {jogo.nota || "-"}</p>
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </>
  );
}

export default Home_2025;

