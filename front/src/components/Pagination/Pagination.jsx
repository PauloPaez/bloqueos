import React from "react";
import "./Pagination.css";
import { ChevronLeft } from "lucide-react";
import { ChevronFirst } from "lucide-react";
import { ChevronRight } from "lucide-react";
import { ChevronLast } from "lucide-react";

const Pagination = ({
    currentPage,
    totalItems,
    pageSize,
    onPageChange,
    onPageSizeChange,
    maxVisiblePages = 5,
}) => {
    const totalPages = Math.ceil(totalItems / pageSize);

    // Calcular el rango de páginas visibles
    const getVisiblePages = () => {
        const half = Math.floor(maxVisiblePages / 2);
        let start = Math.max(currentPage - half, 1);
        let end = Math.min(start + maxVisiblePages - 1, totalPages);

        // Ajustar el inicio si no hay suficientes páginas al final
        if (end - start + 1 < maxVisiblePages) {
            start = Math.max(end - maxVisiblePages + 1, 1);
        }

        return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    };

    const visiblePages = getVisiblePages();

    // Calcular información para mostrar
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = Math.min(currentPage * pageSize, totalItems);

    const pageSizeOptions = [5, 10, 15, 20, 25, 50];

    if (totalPages <= 1) {
        return (
            <div className="pagination-container">
                <div className="pagination-info">
                    <span>
                        Mostrando {totalItems} de {totalItems} registros
                    </span>
                </div>
                {totalItems > 5 && (
                    <div className="pagination-size-selector">
                        <label htmlFor="pageSize">Elementos por página:</label>
                        <select
                            id="pageSize"
                            value={pageSize}
                            onChange={(e) =>
                                onPageSizeChange(Number(e.target.value))
                            }
                            className="page-size-select"
                        >
                            {pageSizeOptions.map((size) => (
                                <option key={size} value={size}>
                                    {size}
                                </option>
                            ))}
                        </select>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="pagination-container">
            <div className="pagination-info">
                <span>
                    Mostrando {startItem} a {endItem} de {totalItems} registros
                </span>
            </div>

            <div className="pagination-controls">
                {/* Botón Primera página */}
                <button
                    className={`pagination-btn ${
                        currentPage === 1 ? "disabled" : ""
                    }`}
                    onClick={() => onPageChange(1)}
                    disabled={currentPage === 1}
                    title="Primera página"
                >
                    <ChevronFirst size={16} />
                </button>

                {/* Botón Página anterior */}
                <button
                    className={`pagination-btn ${
                        currentPage === 1 ? "disabled" : ""
                    }`}
                    onClick={() => onPageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    title="Página anterior"
                >
                    <ChevronLeft size={16} />
                </button>

                {/* Números de página */}
                {visiblePages[0] > 1 && (
                    <>
                        <button
                            className="pagination-btn"
                            onClick={() => onPageChange(1)}
                        >
                            1
                        </button>
                        {visiblePages[0] > 2 && (
                            <span className="pagination-ellipsis">...</span>
                        )}
                    </>
                )}

                {visiblePages.map((page) => (
                    <button
                        key={page}
                        className={`pagination-btn ${
                            page === currentPage ? "active" : ""
                        }`}
                        onClick={() => onPageChange(page)}
                    >
                        {page}
                    </button>
                ))}

                {visiblePages[visiblePages.length - 1] < totalPages && (
                    <>
                        {visiblePages[visiblePages.length - 1] <
                            totalPages - 1 && (
                            <span className="pagination-ellipsis">...</span>
                        )}
                        <button
                            className="pagination-btn"
                            onClick={() => onPageChange(totalPages)}
                        >
                            {totalPages}
                        </button>
                    </>
                )}

                {/* Botón Página siguiente */}
                <button
                    className={`pagination-btn ${
                        currentPage === totalPages ? "disabled" : ""
                    }`}
                    onClick={() => onPageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    title="Página siguiente"
                >
                    <ChevronRight size={16} />
                </button>

                {/* Botón Última página */}
                <button
                    className={`pagination-btn ${
                        currentPage === totalPages ? "disabled" : ""
                    }`}
                    onClick={() => onPageChange(totalPages)}
                    disabled={currentPage === totalPages}
                    title="Última página"
                >
                    <ChevronLast size={16} />
                </button>
            </div>

            <div className="pagination-size-selector">
                <label htmlFor="pageSize">Elementos por página:</label>
                <select
                    id="pageSize"
                    value={pageSize}
                    onChange={(e) => onPageSizeChange(Number(e.target.value))}
                    className="page-size-select"
                >
                    {pageSizeOptions.map((size) => (
                        <option key={size} value={size}>
                            {size}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
};

export default Pagination;