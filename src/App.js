import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Components/Home/Home";
import Top3Jogos from "./Components/TOP/Top";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/top3" element={<Top3Jogos />} />
      </Routes>
    </Router>
  );
}

export default App;
