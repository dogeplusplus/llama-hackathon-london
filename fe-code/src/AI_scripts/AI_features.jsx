import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import one from "../assets/gifs/one.gif";
import two from "../assets/gifs/two.gif";
import three from "../assets/gifs/three.gif";
import four from "../assets/gifs/four.gif";
import QA from "./QA";
import Revision from "./Revision";
import Summary from "./Summary";
import Exercises from "./Exercises";

const SectionCard = ({ bgImage, icon, summary, route }) => {
  return (
    <div
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        height: "300px",
        padding: "20px",
        margin: "10px",
        borderRadius: "8px",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
        <img src={icon} alt="icon" style={{ width: "40px", height: "40px", marginRight: "10px" }} />
        <p>{summary}</p>
      </div>
      <button
        onClick={route}
        style={{
          padding: "10px 20px",
          backgroundColor: "#333",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        AI assist with ...
      </button>
    </div>
  );
};

const AI_features = () => {
  const navigate = useNavigate(); // Using useNavigate hook for routing

  const handleButtonClick = (path) => {
    navigate(path);
  };

  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "space-around" }}>
      <SectionCard
        bgImage="https://images.unsplash.com/photo-1"
        icon={one}
        summary="This is the Q&A feature"
        route={() => handleButtonClick("/component-one")}
      />
      <SectionCard
        bgImage="https://images.unsplash.com/photo-2"
        icon={two}
        summary="This is the summarization feature"
        route={() => handleButtonClick("/component-two")}
      />
      <SectionCard
        bgImage="https://images.unsplash.com/photo-3"
        icon={three}
        summary="This is the exercises feature"
        route={() => handleButtonClick("/component-three")}
      />
      <SectionCard
        bgImage="https://images.unsplash.com/photo-4"
        icon={four}
        summary="This is the revisions feature"
        route={() => handleButtonClick("/component-four")}
      />
    </div>
  );
};

// Wrap the component in a <Router> at the top level
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AI_features />} />
        <Route path="/component-one" element={<QA />} />
        <Route path="/component-two" element={<Revision />} />
        <Route path="/component-three" element={<Summary />} />
        <Route path="/component-four" element={<Exercises />} />
      </Routes>
    </Router>
  );
};

export default App;
