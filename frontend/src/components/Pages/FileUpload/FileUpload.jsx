import React, { useState } from 'react'

function FileUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload-excel', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert("File uploaded and database updated successfully!");
      } else {
        alert("Upload failed.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setUploading(false);
    }
  };
  return (
    <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100 mb-8">
      <h2 className="text-lg font-bold mb-4 text-gray-800">Upload Dataset (Excel)</h2>
      <div className="flex items-center gap-4">
        <input 
          type="file" 
          accept=".xlsx, .xls" 
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button 
          onClick={handleUpload}
          disabled={uploading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
        >
          {uploading ? 'Processing...' : 'Upload & Sync'}
        </button>
      </div>
    </div>
  );
}

export default FileUpload