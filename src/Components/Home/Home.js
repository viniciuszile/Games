// Home.js atualizado com suporte a Concluído / Em andamento / dropado
import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./home.css";

function Home() {
  const navigate = useNavigate();
  const [jogos, setJogos] = useState([]);
  const [flipped, setFlipped] = useState({});
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);
  const [filtro, setFiltro] = useState("todos");
  const [ordenacao, setOrdenacao] = useState(null);
  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);

  // Carregamento do JSON
  useEffect(() => {
    fetch("https://raw.githubusercontent.com/viniciuszile/Games/refs/heads/main/public/Data/jogos.json")
      .then((res) => {
        if (!res.ok) throw new Error("Erro ao buscar os dados");
        return res.json();
      })
      .then((data) => {
        setJogos(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar os jogos:", err);
        setErro("Falha ao carregar os jogos localmente.");
        setLoading(false);
      });
  }, []);

  // Girar card
  function toggleFlip(index) {
    setFlipped((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  }

  // Normalizar acentos
  function removerAcentos(str) {
    if (typeof str !== "string") return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  // Verificar concluído
  function isConcluido(situacao) {
    if (!situacao) return false;
    const n = removerAcentos(situacao).toLowerCase().trim();
    return n === "concluido";
  }

  // Verificar dropado
  function isdropado(situacao) {
    if (!situacao) return false;
    const n = removerAcentos(situacao).toLowerCase().trim();
    return n === "dropado";
  }

  // Horas jogadas (para ordenação)
  function extrairHoras(jogo) {
    const valor = jogo["Horas De Jogo"]?.trim() || "";
    const match = valor.match(/\d+/);
    return match ? parseInt(match[0], 10) : 0;
  }

  // Ordenações
  function ordenarPorNome(a, b) {
    return (a.nome || "").localeCompare(b.nome || "");
  }

  function ordenarPorTempo(a, b) {
    return extrairHoras(a) - extrairHoras(b);
  }

  // Aplicar filtros
  let jogosFiltrados = jogos.filter((jogo) => {
    if (filtro === "concluidos") return isConcluido(jogo.situacao);
    if (filtro === "Dropado") return isdropado(jogo.situacao);
    if (filtro === "em-andamento")
      return !isConcluido(jogo.situacao) && !isdropado(jogo.situacao);
    return true;
  });

  // Aplicar ordenação
  if (ordenacao) {
    jogosFiltrados = [...jogosFiltrados];

    if (ordenacao === "nome-asc") jogosFiltrados.sort(ordenarPorNome);
    else if (ordenacao === "nome-desc") jogosFiltrados.sort((a, b) => ordenarPorNome(b, a));
    else if (ordenacao === "tempo-asc") jogosFiltrados.sort(ordenarPorTempo);
    else if (ordenacao === "tempo-desc") jogosFiltrados.sort((a, b) => ordenarPorTempo(b, a));
  }

  // Fechar menu ao clicar fora
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

  return (
    <>
      {/* Header */}
      <header className="status-header">
        <div>🎯 <strong>Zerados:</strong> {jogos.filter((j) => isConcluido(j.situacao)).length}</div>
        <div>🔥 <strong>Em andamento:</strong> {jogos.filter((j) => !isConcluido(j.situacao) && !isdropado(j.situacao)).length}</div>
        <div>❌ <strong>Dropado:</strong> {jogos.filter((j) => isdropado(j.situacao)).length}</div>
      </header>

      {/* Botão filtro */}
      <button className="filtro-toggle" onClick={() => setMenuAberto(!menuAberto)}>
        🎮 Filtros
      </button>

      {/* Menu filtros */}
      {menuAberto && (
        <div className="menu-flutuante" ref={menuRef}>
          <h4>Filtrar por:</h4>

          <button className={filtro === "todos" ? "ativo" : ""} onClick={() => setFiltro("todos")}>Todos</button>
          <button className={filtro === "concluidos" ? "ativo" : ""} onClick={() => setFiltro("concluidos")}>Concluídos</button>
          <button className={filtro === "em-andamento" ? "ativo" : ""} onClick={() => setFiltro("em-andamento")}>Em andamento</button>
          <button className={filtro === "Dropado" ? "ativo" : ""} onClick={() => setFiltro("Dropado")}>Dropado</button>

          <h4>Ordenar por:</h4>
          <button onClick={() => setOrdenacao(ordenacao === "nome-asc" ? "nome-desc" : "nome-asc")}>
            Ordem alfabética
          </button>
          <button onClick={() => setOrdenacao(ordenacao === "tempo-asc" ? "tempo-desc" : "tempo-asc")}>
            Tempo de jogo
          </button>

          <button onClick={() => setOrdenacao(null)}>Limpar ordenação</button>
        </div>
      )}

      {/* Cards */}
      <div className="container_card">
        {jogosFiltrados.map((jogo, index) => {
          const classeEstado =
            isConcluido(jogo.situacao)
              ? "concluido"
              : isdropado(jogo.situacao)
              ? "dropado"
              : "em-andamento";

          return (
            <div
              key={index}
              className={`card ${classeEstado} ${flipped[index] ? "flipped" : ""}`}
              onClick={() => toggleFlip(index)}
            >
              {/* Frente */}
              <div className="card-front">
                <img src={jogo.imagem} alt={jogo.nome} />
              </div>

              {/* Verso */}
              <div className="card-back">
                {/* dropado → mostra Motivo / Plano */}
                {isdropado(jogo.situacao) ? (
                  <>
                    {jogo.plataforma && <p><strong>Plataforma:</strong> {jogo.plataforma}</p>}
                    {jogo.inicio && <p><strong>Início:</strong> {jogo.inicio}</p>}
                    {jogo.Motivo && <p><strong>Motivo:</strong> {jogo.Motivo}</p>}
                    {jogo["Plano de ação"] && <p><strong>Plano de ação:</strong> {jogo["Plano de ação"]}</p>}
                  </>
                ) : (
                  /* Normal */
                  <>
                    <p><strong>Plataforma:</strong> {jogo.plataforma || "-"}</p>
                    <p><strong>Início:</strong> {jogo.inicio || "-"}</p>
                    <p><strong>Término:</strong> {jogo.termino || "-"}</p>
                    <p><strong>Situação:</strong> {jogo.situacao || "-"}</p>
                    <p><strong>Horas:</strong> {extrairHoras(jogo)}h</p>
                    <p><strong>Dificuldade:</strong> {jogo.dificuldade || "-"}</p>
                    <p><strong>Replay:</strong> {jogo.replay || "-"}</p>
                    <p><strong>Nota:</strong> {jogo.nota || "-"}</p>
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

export default Home;

