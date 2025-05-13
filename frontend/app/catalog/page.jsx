"use client";
import { useState, useEffect } from "react";
import SneakerGrid from "../components/SneakerGrid";
import SortDropdown from "../components/SortDropdown";

export default function CatalogPage() {
  const [sneakers, setSneakers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortType, setSortType] = useState("default");
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 10;

  const fetchSneakers = async () => {
    try {
      setLoading(true);
      const res = await fetch(`http://localhost:8000/api/v1/sneakers/?page=${currentPage}&limit=30&order=${sortType}`);
      const data = await res.json();
      setSneakers(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSneakers();
  }, [sortType, currentPage]);

  const handleSortChange = (newSortType) => {
    setSortType(newSortType);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const getPageNumbers = () => {
    const pages = [];
    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
      pages.push(1);
      if (currentPage > 3) pages.push("...");
      for (let i = Math.max(2, currentPage - 2); i <= Math.min(totalPages - 1, currentPage + 2); i++) {
        pages.push(i);
      }
      if (currentPage < totalPages - 2) pages.push("...");
      pages.push(totalPages);
    }
    return pages;
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen bg-white text-black p-6">
      <h1 className="text-5xl font-bold text-neutral-600 mt-16 mb-6">Каталог</h1>

<div className="w-full flex flex-row gap-6 mt-[100px] justify-start">
  <button className="px-9 py-4 bg-yellow-500 text-black font-semibold rounded-full transition-all duration-300 hover:bg-yellow-600 hover:shadow-lg hover:brightness-75">
    Фильтры
  </button>

  <SortDropdown onChange={handleSortChange} />
</div>




      {loading ? (
        <p className="text-lg text-gray-500 mt-6">Загрузка...</p>
      ) : (
        <SneakerGrid sneakers={sneakers} cols="grid-cols-5" />
      )}

      <div className="flex gap-3 mt-8">
        {getPageNumbers().map((page, index) => (
          <button
            key={index}
            onClick={() => typeof page === "number" && handlePageChange(page)}
            className={`px-4 py-2 rounded-md transition-all ${
              currentPage === page ? "bg-yellow-500 text-black font-bold" : "bg-gray-200 text-gray-600 hover:bg-gray-300"
            }`}
            disabled={page === "..."}
          >
            {page}
          </button>
        ))}
      </div>

      <p className="mt-4 text-lg font-semibold text-neutral-600">Страница: {currentPage}</p>
    </main>
  );
}
