"use client";
import { useState, useEffect, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import SneakerGrid from "../components/SneakerGrid";
import SortDropdown from "../components/SortDropdown";
import FilterSidebar from "../components/FilterSidebar";
import NoResults from "../components/NoResults";

export default function CatalogPage() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const currentPage = Number(searchParams.get("page")) || 1;
  const [sneakersData, setSneakersData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState(searchParams.get("sort_by") || "");
  const [order, setOrder] = useState(searchParams.get("order") || "");
  const [totalPages, setTotalPages] = useState(1);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const controlsRef = useRef(null);
  const [isSticky, setIsSticky] = useState(false);

  useEffect(() => {
    const savedPosition = sessionStorage.getItem("scrollPosition");
    if (savedPosition) {
      window.scrollTo(0, Number(savedPosition));
    }
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (controlsRef.current) {
        const { top } = controlsRef.current.getBoundingClientRect();
        setIsSticky(top <= 20);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const fetchSneakers = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams(searchParams.toString());
      params.set("limit", "30");

      const res = await fetch(`http://localhost:8000/api/v1/sneakers/?${params.toString()}`);
      const data = await res.json();

      setSneakersData(data || { total_count: 0, items: [] });
      setTotalPages(Math.ceil((data.total_count || 1) / 30));
      setLoading(false);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSneakers();
  }, [searchParams, currentPage]);

  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  const applyFilters = (filters) => {
    const newParams = new URLSearchParams();
    if (filters.sneakerName) newParams.set("name", filters.sneakerName);
    if (filters.minPrice) newParams.set("min_price", filters.minPrice);
    if (filters.maxPrice) newParams.set("max_price", filters.maxPrice);
    if (filters.selectedSizes?.length) newParams.set("size", filters.selectedSizes.join(","));
    if (filters.selectedBrands?.length) newParams.set("brand_name", filters.selectedBrands.join(","));
    if (filters.selectedGenders?.length) newParams.set("gender", filters.selectedGenders.join(","));

    newParams.set("page", "1");
    router.push(`/catalog${newParams.toString() ? "?" + newParams.toString() : ""}`);
    setIsSidebarOpen(false);
  };

  return (
    <main className="relative flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-5xl font-bold text-neutral-600 mt-16 mb-6">Каталог</h1>

      <div className="w-full flex flex-row gap-6 mt-[100px] justify-start items-center sticky top-30 z-50 p-4">
        <button
          className="px-8 h-[45px] border border-yellow-500 text-yellow-500 rounded-md hover:bg-yellow-500 hover:text-white transition-all"
          onClick={handleOpenSidebar}
        >
          Фильтры
        </button>
        <SortDropdown setSortBy={setSortBy} />
      </div>

      <FilterSidebar isSidebarOpen={isSidebarOpen} handleCloseSidebar={handleCloseSidebar} applyFilters={applyFilters} />

      {loading ? (
        <p className="text-lg text-gray-500 mt-6">Загрузка...</p>
      ) : (
        <>
          {sneakersData?.items?.length > 0 ? (
            <SneakerGrid data={sneakersData} cols="grid-cols-5" />
          ) : (
            <NoResults />
          )}
        </>
      )}

      <div className="flex gap-3 mt-8">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => {
              sessionStorage.setItem("scrollPosition", window.scrollY);
              const currentParams = new URLSearchParams(searchParams.toString());
              currentParams.set("page", page);
              router.push(`/catalog?${currentParams.toString()}`);
            }}
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
