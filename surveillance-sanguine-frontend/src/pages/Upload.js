import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploadedFileUrl, setUploadedFileUrl] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('No token found. Please log in.');
        return;
      }

      console.log('Token:', token);  // Debugging: Log the token

      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`,
        },
      });

      const filename = response.data.filename;
      const fileUrlResponse = await axios.get(`http://127.0.0.1:5000/file-url/${filename}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      setUploadedFileUrl(fileUrlResponse.data.file_url);
    } catch (error) {
      if (error.response && error.response.data) {
        console.error(error.response.data);
        alert(`File upload failed: ${error.response.data.message}`);
      } else {
        console.error(error);
        alert('File upload failed. Please try again.');
      }
    }
  };

  return (
    <div>
      <h2>Upload Blood Test Results</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {uploadedFileUrl && (
        <div>
          <h3>Uploaded File:</h3>
          <a href={uploadedFileUrl} target="_blank" rel="noopener noreferrer">
            {uploadedFileUrl}
          </a>
        </div>
      )}
      <div>
        <Link to="/uploaded-tests">View Uploaded Tests</Link>
      </div>
    </div>
  );
};

export default Upload;
