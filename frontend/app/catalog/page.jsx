"use client";
import { useState, useEffect } from "react";
import SneakerGrid from "../components/SneakerGrid";
import SortDropdown from "../components/SortDropdown";
import FilterSidebar from "../components/FilterSidebar";

export default function CatalogPage() {
  const [sneakers, setSneakers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortType, setSortType] = useState("default");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(10);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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

  const handleOpenSidebar = () => {
    setIsSidebarOpen(true);
  };

  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
  };

  const applyFilters = (filters) => {
    console.log("Фильтры:", filters);
    setIsSidebarOpen(false);
  };

  return (
    <main className="relative flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-5xl font-bold text-neutral-600 mt-16 mb-6">Каталог</h1>

<div className="w-full flex fle x-row gap-6 mt-[100px] justify-start">
  <button
    className="px-8 h-[45px] mt-4 border border-yellow-500 text-yellow-500 bg-white rounded-md hover:bg-yellow-500 hover:text-white transition-all"
    onClick={handleOpenSidebar}
  >
    Фильтры
  </button>
  <SortDropdown setSneakers={setSneakers} />
</div>


      <FilterSidebar
        isSidebarOpen={isSidebarOpen}
        handleCloseSidebar={handleCloseSidebar}
        applyFilters={applyFilters}
      />

      {loading ? (
        <p className="text-lg text-gray-500 mt-6">Загрузка...</p>
      ) : (
        <SneakerGrid sneakers={sneakers} cols="grid-cols-5" />
      )}

      <div className="flex gap-3 mt-8">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => setCurrentPage(page)}
            className={`px-4 py-2 rounded-md transition-all ${
              currentPage === page ? "bg-yellow-500 text-black font-bold" : "bg-gray-200 text-gray-600 hover:bg-gray-300"
            }`}
          >
            {page}
          </button>
        ))}
      </div>

      <p className="mt-4 text-lg font-semibold text-neutral-600">Страница: {currentPage}</p>
    </main>
  );
}
