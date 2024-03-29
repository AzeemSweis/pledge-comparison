import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
    const [files, setFiles] = useState({
        previousMonth: null,
        currentMonth: null,
    });
    const [results, setResults] = useState('');

    const handleFileChange = (event) => {
        setFiles({ ...files, [event.target.name]: event.target.files[0] });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('previous_month', files.previousMonth);
        formData.append('current_month', files.currentMonth);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResults(response.data.results);  // Assuming the Flask response is { results: '...' }
        } catch (error) {
            console.error('Error uploading files:', error);
        }
    };

    return (
        <div>
            <h1>Upload CSV Files</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Previous Month:
                    <input type="file" name="previousMonth" onChange={handleFileChange} />
                </label>
                <br />
                <label>
                    Current Month:
                    <input type="file" name="currentMonth" onChange={handleFileChange} />
                </label>
                <br />
                <button type="submit">Compare</button>
            </form>
            {results && (
                <div>
                    <h2>Results:</h2>
                    <pre>{results}</pre>
                </div>
            )}
        </div>
    );
}

export default FileUpload;
