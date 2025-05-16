"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function FilterSidebar({ isSidebarOpen, handleCloseSidebar }) {
  const searchParams = useSearchParams();
  const router = useRouter();

  // ✅ Устанавливаем начальные значения из URL
  const [minPrice, setMinPrice] = useState(searchParams.get("min_price") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("max_price") || "");
  const [sneakerName, setSneakerName] = useState(searchParams.get("name") || "");
  const [selectedSizes, setSelectedSizes] = useState(searchParams.get("size")?.split(",") || []);
  const [selectedBrands, setSelectedBrands] = useState(searchParams.get("brand_name")?.split(",") || []);
  const [selectedGenders, setSelectedGenders] = useState(searchParams.get("gender")?.split(",") || []);

  const availableSizes = Array.from({ length: 36 }, (_, i) => i + 15);
  const availableBrands = ["Nike", "Adidas", "Puma", "Reebok", "New Balance"];
  const availableGenders = ["Мужские", "Женские", "Унисекс"];

  // ✅ Автоматически обновляем фильтры при смене URL
  useEffect(() => {
    setMinPrice(searchParams.get("min_price") || "");
    setMaxPrice(searchParams.get("max_price") || "");
    setSneakerName(searchParams.get("name") || "");
    setSelectedSizes(searchParams.get("size")?.split(",").filter(Boolean) || []);
    setSelectedBrands(searchParams.get("brand_name")?.split(",").filter(Boolean) || []);
    setSelectedGenders(searchParams.get("gender")?.split(",").filter(Boolean) || []);
  }, [searchParams]);

  // ✅ Сброс фильтров (сортировка остаётся)
  const resetFilters = () => {
    const currentParams = new URLSearchParams(searchParams.toString());
    currentParams.delete("name");
    currentParams.delete("min_price");
    currentParams.delete("max_price");
    currentParams.delete("size");
    currentParams.delete("brand_name");
    currentParams.delete("gender");

    router.push(`/catalog?${currentParams.toString()}`);
  };

  // ✅ Применение фильтров (сохранение сортировки)
  const applyFilters = () => {
    const newParams = new URLSearchParams(searchParams.toString());

    if (sneakerName) newParams.set("name", sneakerName);
    if (minPrice) newParams.set("min_price", minPrice);
    if (maxPrice) newParams.set("max_price", maxPrice);
    if (selectedSizes.length) newParams.set("size", selectedSizes.join(","));
    if (selectedBrands.length) newParams.set("brand_name", selectedBrands.join(","));
    if (selectedGenders.length) newParams.set("gender", selectedGenders.join(","));

    const sortBy = searchParams.get("sort_by");
    const order = searchParams.get("order");
    if (sortBy) newParams.set("sort_by", sortBy);
    if (order) newParams.set("order", order);

    router.push(`/catalog?${newParams.toString()}`);
    handleCloseSidebar();
  };

  return (
    <>
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-md"
          onClick={handleCloseSidebar}
        ></div>
      )}

      <div
        className={`fixed top-0 left-0 h-full w-[450px] bg-white shadow-lg transform transition-transform duration-300 ${
          isSidebarOpen ? "translate-x-0" : "translate-x-[-100%]"
        }`}
      >
        <div className="p-10 flex flex-col h-full">
          <h2 className="text-xl font-bold text-neutral-600 mb-10">
            Фильтрация товаров
          </h2>

          {/* Фильтр: Название */}
          <label className="block text-sm font-medium text-gray-600">
            Название кроссовок
          </label>
          <input
            type="text"
            className={`w-full mt-3 p-2 border rounded transition ${
              sneakerName.length > 0 ? "border-yellow-500" : "border-gray-300"
            }`}
            placeholder="Введите название..."
            value={sneakerName}
            onChange={(e) => setSneakerName(e.target.value)}
          />

          {/* Фильтр: Цена */}
          <label className="block text-sm font-medium text-gray-600 mt-5">
            Цена
          </label>
          <div className="flex gap-3 mt-3">
            <input
              type="number"
              className="w-full p-2 border rounded"
              placeholder="Мин"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
            />
            <input
              type="number"
              className="w-full p-2 border rounded"
              placeholder="Макс"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
            />
          </div>

          {/* Фильтр: Бренды */}
<label className="block text-sm font-medium text-gray-600 mt-5">
  Бренды
</label>
<div className="flex flex-col mt-3 gap-2">
  {availableBrands.map((brand) => (
    <div
      key={brand}
      className="flex justify-between items-center cursor-pointer"
      onClick={() =>
        setSelectedBrands((prev) =>
          prev.includes(brand)
            ? prev.filter((b) => b !== brand)
            : [...prev, brand]
        )
      }
    >
      <span className="text-gray-700 font-medium">{brand}</span>
      <button
        className={`w-5 h-5 border rounded-md flex items-center justify-center transition-all ${
          selectedBrands.includes(brand)
            ? "bg-yellow-500 border-yellow-600"
            : "bg-gray-200 hover:bg-gray-300"
        }`}
      >
        {selectedBrands.includes(brand) && (
          <span className="text-black font-bold">✓</span>
        )}
      </button>
    </div>
  ))}
</div>


          {/* Фильтр: Размер */}
          <label className="block text-sm font-medium text-gray-600 mt-5">
            Размер
          </label>
          <div className="grid grid-cols-6 gap-2 mt-3">
            {availableSizes.map((size) => (
              <button
                key={size}
                className={`w-[50px] px-3 py-2 border rounded-md transition-all ${
                  selectedSizes.includes(size.toString())
                    ? "bg-yellow-500 text-white font-bold border-yellow-600"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                }`}
                onClick={() =>
                  setSelectedSizes((prev) =>
                    prev.includes(size.toString())
                      ? prev.filter((s) => s !== size.toString())
                      : [...prev, size.toString()]
                  )
                }
              >
                {size}
              </button>
            ))}
          </div>

          {/* Кнопки управления */}
          <div className="flex justify-between w-full mt-auto">
            <button
              className="w-[45%] px-6 py-3 border border-gray-400 text-gray-600 bg-white rounded-md hover:bg-gray-300 transition-all"
              onClick={resetFilters}
            >
              Сброс настроек
            </button>
            <button
              className="w-[45%] px-6 py-3 border border-yellow-500 text-yellow-500 bg-white rounded-md hover:bg-yellow-500 hover:text-white transition-all"
              onClick={applyFilters}
            >
              Применить
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
