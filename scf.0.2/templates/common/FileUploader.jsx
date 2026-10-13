import React from "react";
import { BsFillTrash3Fill, BsFileEarmarkDiff } from "react-icons/bs";

const FileUploader = ({ files, onFileChange, onRemoveFile }) => {
    const handleFileChange = (e) => {
        const selectedFiles = Array.from(e.target.files);
        onFileChange(selectedFiles);
    };

    return (
        <div className="card shadow">
            <div className="card-body">
                {/* Input oculto */}
                <div className="mb-3">
                    <input
                        type="file"
                        multiple
                        onChange={handleFileChange}
                        className="form-control"
                        id="fileInput"
                        style={{ display: "none" }}
                    />
                    {/* Ícono que activa el input */}
                    <label htmlFor="fileInput" style={{ cursor: 'pointer' }}>
                        <BsFileEarmarkDiff /><span className="ms-1">Agregar Archivos</span>
                    </label>

                </div>

                {/* Lista de archivos seleccionados */}
                <ul className="list-group">
                    {files.map((file, index) => (
                        <li
                            key={index}
                            className="list-group-item d-flex"
                        >
                            <span
                                style={{ cursor: 'pointer' }}
                                onClick={() => onRemoveFile(index)}
                                role="button"
                                tabIndex={0}
                            >
                                <BsFillTrash3Fill />
                            </span>
                            <span className="ms-1" >{file.name}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default FileUploader;