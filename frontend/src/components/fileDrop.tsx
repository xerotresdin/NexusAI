import React, { useState } from "react";
import "../styles/fileDrop.css";

const FileDrop: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>(
    "Drag and drop a .csv file here"
  );
  const [isCsvFileHovered, setIsCsvFileHovered] = useState<boolean>(false);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const files = e.dataTransfer.items;
    if (
      files.length > 0 &&
      files[0].kind === "file" &&
      files[0].type === "text/csv"
    ) {
      setIsCsvFileHovered(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsCsvFileHovered(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsCsvFileHovered(false);
    let files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === "text/csv") {
      setFile(files[0]);
      setMessage(`File "${files[0].name}" successfully uploaded.`);
    } else {
      setMessage("Please drop a .csv file.");
    }
  };

  return (
    <div
      id="app"
      className="container"
      style={{
        textAlign: "center",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        height: "100vh",
      }}
    >
      <header style={{ marginBottom: "20px" }}>
        <div
          style={{ fontSize: "32px", fontWeight: "bold", marginBottom: "24px" }}
        >
          Try NexusAI!
        </div>
        <p
          style={{ marginBottom: "40px", fontSize: "medium", color: "#4a4a4a" }}
        >
          NexusAI is an application designed to assess the probability of
          closing sales deals in the healthcare sector, particularly for health
          system enterprises consisting of multiple hospitals.
        </p>
      </header>

      <div
        className="drag-drop-box"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          margin: "20px auto",
          padding: "50px",
          border: "2px dashed #ccc",
          borderRadius: "20px",
          color: "gray",
          backgroundColor: isCsvFileHovered ? "#D3D3D3" : "#F4F4F4",
          boxShadow: isCsvFileHovered ? "0 0 10px #333" : "none",
          maxWidth: "600px",
        }}
      >
        {message}
      </div>

      <footer style={{ marginTop: "auto", fontSize: "x-small" }}>
        &copy; 2023 NexusAI Inc. All rights reserved
      </footer>
    </div>
  );
};

export default FileDrop;
