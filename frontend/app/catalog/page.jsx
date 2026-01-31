"use client";
export const dynamic = "force-dynamic";

import { Suspense } from "react";
import { useState, useEffect, useRef } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import SneakerGrid from "../components/SneakerGrid";
import SortDropdown from "../components/SortDropdown";
import FilterSidebar from "../components/FilterSidebar";
import NoResults from "../components/NoResults";

// Выносим основное содержимое страницы в отдельный компонент
function CatalogContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const currentPage = Number(searchParams.get("page")) || 1;
  const sortBy = searchParams.get("sort_by") || "";
  const order = searchParams.get("order") || "";

  const [sneakersData, setSneakersData] = useState(null);
  const [loading, setLoading] = useState(true);
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

      // ДЕБАГ: добавим логирование запроса
      console.log("Запрос к API с параметрами:", params.toString());

      const res = await fetch(`http://127.0.0.1:8005/api/v1/catalog/?${params.toString()}`);
      const data = await res.json();

      // ДЕБАГ: посмотрим что пришло от сервера
      console.log("Ответ от сервера:", {
        total_count: data.total_count,
        items_count: data.items?.length,
        first_item: data.items?.[0],
        sort_applied: `sort_by=${sortBy}, order=${order}`
      });

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
  }, [searchParams]); // Убрали currentPage из зависимостей, он уже в searchParams

  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  // Функция для обновления сортировки
  const updateSorting = (newSortBy, newOrder = "desc") => {
    const params = new URLSearchParams(searchParams.toString());

    if (newSortBy) {
      params.set("sort_by", newSortBy);
      params.set("order", newOrder);
    } else {
      params.delete("sort_by");
      params.delete("order");
    }

    params.set("page", "1"); // Сбрасываем на первую страницу при изменении сортировки

    // Сохраняем позицию скролла перед переходом
    sessionStorage.setItem("scrollPosition", window.scrollY);
    router.push(`/catalog?${params.toString()}`);
  };

  const applyFilters = (filters) => {
    const params = new URLSearchParams();

    if (filters.sneakerName) params.set("name", filters.sneakerName);
    if (filters.minPrice) params.set("min_price", filters.minPrice);
    if (filters.maxPrice) params.set("max_price", filters.maxPrice);
    if (filters.selectedSizes?.length) params.set("size", filters.selectedSizes.join(","));
    if (filters.selectedBrands?.length) params.set("brand_name", filters.selectedBrands.join(","));
    if (filters.selectedGenders?.length) params.set("gender", filters.selectedGenders.join(","));

    // Сохраняем текущую сортировку
    if (sortBy) {
      params.set("sort_by", sortBy);
      params.set("order", order);
    }

    params.set("page", "1");

    sessionStorage.setItem("scrollPosition", window.scrollY);
    router.push(`/catalog${params.toString() ? "?" + params.toString() : ""}`);
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

        {/* Передаем текущие значения и функцию обновления */}
        <SortDropdown
          currentSortBy={sortBy}
          currentOrder={order}
          onSortChange={updateSorting}
        />
      </div>

      <FilterSidebar
        isSidebarOpen={isSidebarOpen}
        handleCloseSidebar={handleCloseSidebar}
        applyFilters={applyFilters}
      />

      {loading ? (
        <p className="text-lg text-gray-500 mt-6">Загрузка...</p>
      ) : (
        <>
          {/* ДЕБАГ: добавим информацию о сортировке */}
          {sortBy && (
            <div className="mt-4 text-sm text-gray-500">
              Сортировка по: <strong>{sortBy}</strong> ({order})
            </div>
          )}

          {sneakersData?.items?.length > 0 ? (
            <SneakerGrid data={sneakersData} cols="grid-cols-5" />
          ) : (
            <NoResults />
          )}
        </>
      )}

      {totalPages > 1 && (
        <div className="flex gap-3 mt-8">
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <button
              key={page}
              onClick={() => {
                sessionStorage.setItem("scrollPosition", window.scrollY);
                const params = new URLSearchParams(searchParams.toString());
                params.set("page", page.toString());
                router.push(`/catalog?${params.toString()}`);
              }}
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
      )}

      {sneakersData?.total_count && (
        <p className="mt-4 text-lg font-semibold text-neutral-600">
          Найдено: {sneakersData.total_count} товаров • Страница: {currentPage} из {totalPages}
        </p>
      )}
    </main>
  );
}

// Оборачиваем в Suspense на уровне страницы
export default function CatalogPage() {
  return (
    <Suspense fallback={<p>Loading catalog...</p>}>
      <CatalogContent />
    </Suspense>
  );
}