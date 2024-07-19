import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UploadedTests = () => {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    const fetchTests = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/tests', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setTests(response.data);
      } catch (error) {
        console.error('Error fetching tests:', error);
      }
    };

    fetchTests();
  }, []);

  return (
    <div>
      <h2>Uploaded Tests</h2>
      <ul>
        {tests.map((test) => (
          <li key={test.id}>
            <a href={`http://127.0.0.1:5000/uploads/${test.id}`} target="_blank" rel="noopener noreferrer">
              Test on {new Date(test.test_date).toLocaleString()}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UploadedTests;
