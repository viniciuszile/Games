import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home_2025 from "./Components/Home/Home_2025";
import Top3Jogos from "./Components/TOP/Top";
import Home_2026 from "./Components/Home _2026/Home_2026";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home_2026 />} />
        <Route path="/top3" element={<Top3Jogos />} />
        <Route path="/Home_2025" element={<Home_2025 />} />
      </Routes>
    </Router>
  );
}

export default App;
