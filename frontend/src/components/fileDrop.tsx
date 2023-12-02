import React, { useState } from 'react';
import '../styles/fileDrop.css';

const FileDrop: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    let files = e.dataTransfer.files;
    if (files.length > 0) {
      setFile(files[0]);
      // Read and process the file here
    }
  };

  return (
    <div id="app" className="container">
      <div className="drag drag-drop-box" 
           onDragOver={handleDragOver} 
           onDrop={handleDrop} 
           style={{ margin: 'auto', padding: '50px', textAlign: 'center', border: '2px dashed #ccc', borderRadius: '20px', color: 'white', backgroundColor: '#F4F4F4' }}>
        Drag and drop a file here
        {file && <p>File selected: {file.name}</p>}
      </div>
    </div>
  );
};

export default FileDrop;
