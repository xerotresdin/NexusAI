import React, { useState } from 'react';
import '../styles/fileDrop.css';

const FileDrop: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>('Drag and drop a .csv file here');
  const [isCsvFileHovered, setIsCsvFileHovered] = useState<boolean>(false);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    // Check if the file being dragged is a .csv file
    const files = e.dataTransfer.items;
    if (files.length > 0 && files[0].kind === 'file' && files[0].type === 'text/csv') {
      setIsCsvFileHovered(true);
    }
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsCsvFileHovered(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsCsvFileHovered(false); // Reset on drop
    let files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'text/csv') {
      setFile(files[0]);
      setMessage(`File "${files[0].name}" successfully uploaded.`);
    } else {
      setMessage('Please drop a .csv file.');
    }
  };

  return (
    <div id="app" className="container">
      <div className="fixed left-[50%] top-[50%] max-h-full w-full translate-x-[-50%] translate-y-[-50%] overflow-y-auto p-5 text-center sm:max-w-2xl">
        <div className="mb-6 text-4xl font-bold font-unbounded md:text-5xl">
          Use the NexusAI!
        </div>
        <p className="mb-10 text-sm text-black-300 ">
        This project targets the productivity challenges faced by professionals overwhelmed with meetings, emails, 
        and messages. Our application, currently in beta, automates recording of voice notes and text notes, enabling users to
        effortlessly retrieve relevant information from these notes, regardless of their creation time. This tool provides a 
        swift and simple solution for users to effectively handle their information overload.
        </p>
        

        
      </div>
      <div className="drag-drop-box" 
           onDragOver={handleDragOver} 
           onDragLeave={handleDragLeave}
           onDrop={handleDrop} 
           style={{ 
             margin: 'auto', 
             padding: '50px', 
             textAlign: 'center', 
             border: '2px dashed #ccc', 
             borderRadius: '20px', 
             color: 'gray', 
             backgroundColor: isCsvFileHovered ? '#D3D3D3' : '#F4F4F4', // Change color when .csv is hovered
             boxShadow: isCsvFileHovered ? '0 0 10px #333' : 'none', // Optional shadow effect
           }}>
        {message}
        
      </div>
      <footer className="mt-5 text-xs">
          &copy; 2023 NexusAI inc. All rights reserved
        </footer>
      
    </div>
  );
};

export default FileDrop;
