import React, { useState } from 'react';

const PdfJs = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [fileUrl, setFileUrl] = useState('');
  const [bookId, setBookId] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('Uploading...');
      const response = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data', 
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setUploadStatus('Upload successful');
      setFileUrl(data.file_url);
      setBookId(data.book_id);
    } catch (error) {
      setUploadStatus('Error during upload');
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Upload a PDF</h1>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      
      {uploadStatus && <p>{uploadStatus}</p>}

      {fileUrl && (
        <div>
          <p>File uploaded successfully! View the file below:</p>
          <a href={fileUrl} target="_blank" rel="noopener noreferrer">
            {bookId} - View PDF
          </a>
        </div>
      )}
    </div>
  );
};

export default PdfJs;
