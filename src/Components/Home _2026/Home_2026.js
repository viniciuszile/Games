import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./Home_2026.css";

function Home_2026() {

  const navigate = useNavigate();

  const [jogos, setJogos] = useState([]);
  const [flipped, setFlipped] = useState({});
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  const [filtro, setFiltro] = useState("todos");

  // FILTRO PLATAFORMA
  const [filtroPlataforma, setFiltroPlataforma] =
    useState("todos");

  const [ordenacao, setOrdenacao] = useState(null);

  const [menuAberto, setMenuAberto] = useState(false);

  const menuRef = useRef(null);

  /* ========================= */
  /* 📥 Carregar JSON          */
  /* ========================= */

  useEffect(() => {

    fetch(
      "https://raw.githubusercontent.com/viniciuszile/Games/refs/heads/main/public/Data/jogos_2026.json"
    )
      .then((res) => {

        if (!res.ok) {
          throw new Error("Erro ao buscar os dados");
        }

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
  /* 🔄 Flip                   */
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

  function parseDataInicio(jogo) {

    if (!jogo.inicio || jogo.inicio === "-") {
      return 0;
    }

    const partes = jogo.inicio
      .trim()
      .split("/");

    const dia = parseInt(partes[0], 10);
    const mes = parseInt(partes[1], 10) - 1;
    const ano = parseInt(partes[2], 10);

    return new Date(
      ano,
      mes,
      dia
    ).getTime();

  }

  function removerAcentos(str) {

    if (typeof str !== "string") {
      return "";
    }

    return str
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

  }

  function isConcluido(situacao) {

    const n = removerAcentos(situacao || "")
      .toLowerCase()
      .trim();

    return n === "concluido";

  }

  function ispausado(situacao) {

    const n = removerAcentos(situacao || "")
      .toLowerCase()
      .trim();

    return n === "pausado";

  }

  function extrairHoras(jogo) {

    const valor =
      jogo["Horas De Jogo"]?.trim() || "";

    const match = valor.match(/\d+/);

    return match
      ? parseInt(match[0], 10)
      : 0;

  }

  function extrairRank(jogo) {

    const r = parseInt(jogo.Rank_25, 10);

    return isNaN(r)
      ? 999
      : r;

  }

  /* ========================= */
  /* 🔃 Ordenações             */
  /* ========================= */

  function ordenarPorNome(a, b) {

    return (a.nome || "")
      .localeCompare(b.nome || "");

  }

  function ordenarPorTempo(a, b) {

    return (
      extrairHoras(a) -
      extrairHoras(b)
    );

  }

  function ordenarPorRankAsc(a, b) {

    return (
      extrairRank(a) -
      extrairRank(b)
    );

  }

  function ordenarPorRankDesc(a, b) {

    return (
      extrairRank(b) -
      extrairRank(a)
    );

  }

  /* ========================= */
  /* 🎯 Filtros                */
  /* ========================= */

  let jogosFiltrados = jogos.filter((jogo) => {

    // esconder jogos sem horas
    if (
      (ordenacao === "tempo-asc" ||
        ordenacao === "tempo-desc") &&
      extrairHoras(jogo) <= 0
    ) {
      return false;
    }

    // esconder rank vazio
    if (
      (ordenacao === "rank-asc" ||
        ordenacao === "rank-desc") &&
      extrairRank(jogo) >= 999
    ) {
      return false;
    }

    // filtro situação
    if (filtro === "concluidos") {

      if (!isConcluido(jogo.situacao)) {
        return false;
      }

    }

    if (filtro === "pausado") {

      if (!ispausado(jogo.situacao)) {
        return false;
      }

    }

    if (filtro === "em-andamento") {

      if (
        isConcluido(jogo.situacao) ||
        ispausado(jogo.situacao)
      ) {
        return false;
      }

    }

    // FILTRO PLATAFORMA
    if (filtroPlataforma !== "todos") {

      const plataformaJogo =
        (jogo.plataforma || "")
          .toLowerCase();

      const plataformaFiltro =
        filtroPlataforma.toLowerCase();

      if (
        !plataformaJogo.includes(
          plataformaFiltro
        )
      ) {
        return false;
      }

    }

    return true;

  });

  /* ========================= */
  /* 📅 Ordem padrão           */
  /* ========================= */

  jogosFiltrados = [...jogosFiltrados].sort((a, b) => {

    const dataA = parseDataInicio(a);
    const dataB = parseDataInicio(b);

    return dataA - dataB;

  });

  /* ========================= */
  /* 🔃 Ordenações extras      */
  /* ========================= */

  if (ordenacao) {

    if (ordenacao === "nome-asc") {
      jogosFiltrados.sort(ordenarPorNome);
    }

    if (ordenacao === "nome-desc") {

      jogosFiltrados.sort((a, b) =>
        ordenarPorNome(b, a)
      );

    }

    if (ordenacao === "tempo-asc") {
      jogosFiltrados.sort(ordenarPorTempo);
    }

    if (ordenacao === "tempo-desc") {

      jogosFiltrados.sort((a, b) =>
        ordenarPorTempo(b, a)
      );

    }

    if (ordenacao === "rank-asc") {
      jogosFiltrados.sort(
        ordenarPorRankAsc
      );
    }

    if (ordenacao === "rank-desc") {
      jogosFiltrados.sort(
        ordenarPorRankDesc
      );
    }

  }

  /* ========================= */
  /* ❌ Fechar menu fora       */
  /* ========================= */

  useEffect(() => {

    function handleClickOutside(e) {

      if (
        menuRef.current &&
        !menuRef.current.contains(e.target)
      ) {
        setMenuAberto(false);
      }

    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () =>
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

  }, []);

  if (loading) {

    return (
      <p style={{ color: "#fff" }}>
        Carregando...
      </p>
    );

  }

  if (erro) {

    return (
      <p style={{ color: "red" }}>
        {erro}
      </p>
    );

  }

  /* ========================= */
  /* 🧮 Contadores             */
  /* ========================= */

  const totalConcluidos =
    jogos.filter((j) =>
      isConcluido(j.situacao)
    ).length;

  const totalpausados =
    jogos.filter((j) =>
      ispausado(j.situacao)
    ).length;

  const totalEmAndamento =
    jogos.length -
    totalConcluidos -
    totalpausados;

  /* ========================= */
  /* 🖥️ Render                 */
  /* ========================= */

  return (
    <>

      <header className="status-header">

        <div>
          🎯 <strong>Zerados:</strong>{" "}
          {totalConcluidos}
        </div>

        <div>
          🔥 <strong>Em andamento:</strong>{" "}
          {totalEmAndamento}
        </div>

        <div>
          ⏸️ <strong>pausado:</strong>{" "}
          {totalpausados}
        </div>

        <div>
          📦 <strong>Total:</strong>{" "}
          {jogos.length}
        </div>

      </header>

      <button
        className="filtro-toggle"
        onClick={() =>
          setMenuAberto(!menuAberto)
        }
      >
        🎮 Filtros
      </button>

      {menuAberto && (

        <div
          className="menu-flutuante"
          ref={menuRef}
        >

          <h4>🧭 Navegação</h4>

          <div className="menu-grid">

            <button
              onClick={() =>
                navigate("/Home_2025")
              }
            >
              🏠 2025
            </button>

          </div>

          <h4>🔍 Filtrar por</h4>

          <div className="menu-grid">

            <button
              onClick={() =>
                setFiltro("todos")
              }
            >
              📋 Todos
            </button>

            <button
              onClick={() =>
                setFiltro("concluidos")
              }
            >
              ✅ Concluídos
            </button>

            <button
              onClick={() =>
                setFiltro("em-andamento")
              }
            >
              ⏳ Em andamento
            </button>

            <button
              onClick={() =>
                setFiltro("pausado")
              }
            >
              ⏸️ pausado
            </button>

          </div>

          <h4>🖥️ Plataforma</h4>

          <div className="menu-grid">

            <button
              onClick={() =>
                setFiltroPlataforma("todos")
              }
            >
              🎮 Todas
            </button>

            <button
              onClick={() =>
                setFiltroPlataforma("steam")
              }
            >
              💨 Steam
            </button>

            <button
              onClick={() =>
                setFiltroPlataforma("gamepass")
              }
            >
              🟢 Gamepass
            </button>

          </div>

          <h4>↕️ Ordenar por</h4>

          <div className="menu-grid">

            <button
              onClick={() =>
                setOrdenacao("nome-asc")
              }
            >
              🔤 Nome
            </button>

            <button
              onClick={() =>
                setOrdenacao("tempo-asc")
              }
            >
              ⏱️ Tempo
            </button>

            <button
              className="botao-rank-desativado"
              disabled
            >
              🏆 Rank 2026
            </button>

            <button
              onClick={() => {

                setOrdenacao(null);
                setFiltro("todos");
                setFiltroPlataforma("todos");

              }}
            >
              🧹 Limpar
            </button>

          </div>

        </div>

      )}

      <div className="container_card">

        {jogosFiltrados.map(
          (jogo, index) => {

            const pausado =
              ispausado(jogo.situacao);

            const classeEstado =
              isConcluido(
                jogo.situacao
              )
                ? "concluido"
                : pausado
                ? "pausado"
                : "em-andamento";

            return (

              <div
                key={crypto.randomUUID()}
                className={`card ${classeEstado} ${
                  flipped[index]
                    ? "flipped"
                    : ""
                }`}
                onClick={() =>
                  toggleFlip(index)
                }
              >

                <div className="card-front">

                  <img
                    src={jogo.imagem}
                    alt={jogo.nome}
                  />

                </div>

                <div className="card-back">

                  {pausado ? (

                    <>
                      <p className="campo plataforma">
                        <strong>
                          Plataforma:
                        </strong>{" "}
                        {jogo.plataforma || "-"}
                      </p>

                      <p className="campo situacao">
                        <strong>
                          Situação:
                        </strong>{" "}
                        {jogo.situacao || "-"}
                      </p>

                      <p className="campo inicio">
                        <strong>
                          Início:
                        </strong>{" "}
                        {jogo.inicio || "-"}
                      </p>

                      <p className="campo motivo">
                        <strong>
                          Motivo:
                        </strong>{" "}
                        {jogo.Motivo || "-"}
                      </p>

                      <p className="campo plano">
                        <strong>
                          Plano de ação:
                        </strong>{" "}
                        {jogo[
                          "Plano de ação"
                        ] || "-"}
                      </p>
                    </>

                  ) : (

                    <>
                      <p className="campo plataforma">
                        <strong>
                          Plataforma:
                        </strong>{" "}
                        {jogo.plataforma || "-"}
                      </p>

                      <p className="campo inicio">
                        <strong>
                          Início:
                        </strong>{" "}
                        {jogo.inicio || "-"}
                      </p>

                      <p className="campo termino">
                        <strong>
                          Término:
                        </strong>{" "}
                        {jogo.termino || "-"}
                      </p>

                      <p className="campo situacao">
                        <strong>
                          Situação:
                        </strong>{" "}
                        {jogo.situacao || "-"}
                      </p>

                      <p className="campo horas">
                        <strong>
                          Horas:
                        </strong>{" "}
                        {extrairHoras(
                          jogo
                        )}h
                      </p>

                      <p className="campo dificuldade">
                        <strong>
                          Dificuldade:
                        </strong>{" "}
                        {jogo.dificuldade ||
                          "-"}
                      </p>

                      <p className="campo replay">
                        <strong>
                          Replay:
                        </strong>{" "}
                        {jogo.replay || "-"}
                      </p>

                      <p className="campo nota">
                        <strong>
                          Nota:
                        </strong>{" "}
                        {jogo.nota || "-"}
                      </p>
                    </>

                  )}

                </div>

              </div>

            );

          }
        )}

      </div>

    </>
  );
}

export default Home_2026;