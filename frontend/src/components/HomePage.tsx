import React from "react";
import FileDrop from "./FileDrop";

const HomePage: React.FC = () => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "left", height: "100vh" }}>
      <div style={{ alignSelf: "flex-start" }}>
        <img src="/logo.png" alt="Logo"style={{
            float: "left",
            maxWidth: "300px",
            maxHeight: "300px",
            margin: "10px",
          }}
        />
      </div>
      <FileDrop />
    </div>
  );
};

export default HomePage;
