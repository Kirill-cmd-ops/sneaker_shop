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
  const [activeFilters, setActiveFilters] = useState(null);

  const fetchSneakers = async () => {
    try {
      setLoading(true);
      const res = await fetch(
        `http://localhost:8000/api/v1/sneakers/?page=${currentPage}&limit=30&order=${sortType}`
      );
      const data = await res.json();
      setSneakers(Array.isArray(data) ? data : []);
      setLoading(false);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
      setLoading(false);
    }
  };

  const fetchFilteredSneakers = async (filters) => {
    try {
      setLoading(true);

      const params = new URLSearchParams({
        page: currentPage,
        limit: 30,
        order: sortType,
      });

      if (filters.sneakerName) params.append("name", filters.sneakerName);
      if (filters.minPrice) params.append("min_price", filters.minPrice);
      if (filters.maxPrice) params.append("max_price", filters.maxPrice);
      if (filters.selectedSizes && filters.selectedSizes.length > 0)
        params.append("size", filters.selectedSizes.join(","));
      if (filters.selectedBrands && filters.selectedBrands.length > 0)
        params.append("brand_name", filters.selectedBrands.join(","));
      if (filters.selectedGenders && filters.selectedGenders.length > 0)
        params.append("gender", filters.selectedGenders.join(","));

      const res = await fetch(`http://localhost:8000/api/v1/sneakers/?${params.toString()}`);
      const data = await res.json();
      setSneakers(Array.isArray(data) ? data : []);
      setLoading(false);
      setActiveFilters(filters);
    } catch (error) {
      console.error("Ошибка загрузки данных фильтра:", error);
      setLoading(false);
    }
  };


  useEffect(() => {
    if (activeFilters) {
      fetchFilteredSneakers(activeFilters);
    } else {
      fetchSneakers();
    }
  }, [sortType, currentPage, activeFilters]);

  const handleSortChange = (newSortType) => {
    setSortType(newSortType);
    setActiveFilters(null);
  };

  const handleOpenSidebar = () => {
    setIsSidebarOpen(true);
  };

  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
  };


  const applyFilters = (filters) => {
    setIsSidebarOpen(false);
    fetchFilteredSneakers(filters);
  };

  return (
    <main className="relative flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-5xl font-bold text-neutral-600 mt-16 mb-6">Каталог</h1>

      <div className="w-full flex flex-row gap-6 mt-[100px] justify-start">
        <button
          className="px-8 h-[45px] mt-4 border border-yellow-500 text-yellow-500 bg-white rounded-md hover:bg-yellow-500 hover:text-white transition-all"
          onClick={handleOpenSidebar}
        >
          Фильтры
        </button>
        <SortDropdown setSneakers={setSneakers} onChange={handleSortChange} />
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
              currentPage === page
                ? "bg-yellow-500 text-black font-bold"
                : "bg-gray-200 text-gray-600 hover:bg-gray-300"
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
