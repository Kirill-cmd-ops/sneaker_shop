"use client";
import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function SearchBar({ isOpen, toggleSearch }) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");

  // ✅ При открытии поиска берём прошлый `name` из URL (если есть)
  useEffect(() => {
  if (isOpen) {
    const brand = searchParams.get("brand_name") || "";
    const model = searchParams.get("name") || "";

    // ✅ Если есть оба параметра, объединяем их
    setSearchQuery(`${brand} ${model}`.trim());
  }
}, [isOpen]);


  const handleSearch = () => {
  const trimmedQuery = searchQuery.trim();

  if (!trimmedQuery) {
    router.push("/catalog");
    toggleSearch();
    return;
  }

  const brands = ["Nike", "Adidas", "Puma", "Reebok", "New Balance"];
  let matchedBrand = null;
  let modelName = trimmedQuery;

  // ✅ Проверяем, начинается ли ввод с бренда
  brands.forEach((brand) => {
    if (trimmedQuery.toLowerCase().startsWith(brand.toLowerCase())) {
      matchedBrand = brand;
      modelName = trimmedQuery.slice(brand.length).trim(); // Убираем бренд из строки
    }
  });

  let newParams = new URLSearchParams();

  if (matchedBrand) newParams.set("brand_name", matchedBrand);
  if (modelName) newParams.set("name", modelName);

  router.push(`/catalog?${newParams.toString()}`);
  toggleSearch();
};



  return (
    <>
      {isOpen && <div className="fixed inset-0 bg-black/50 backdrop-blur-md" onClick={toggleSearch}></div>}

      {isOpen && (
        <div className="fixed top-16 left-1/2 transform -translate-x-1/2 w-[500px] bg-white shadow-lg rounded-md p-3 flex items-center">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Введите название..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full p-2 text-black border border-gray-300 rounded-md focus:outline-none focus:border-yellow-500"
            />
            <button onClick={handleSearch} className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <img src="/search.svg" alt="Поиск" className="h-5 w-5 opacity-70 hover:opacity-100 transition-all" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
