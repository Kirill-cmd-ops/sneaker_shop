import React, { useState } from "react";

export default function FilterSidebar({ isSidebarOpen, handleCloseSidebar, applyFilters }) {
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [sneakerName, setSneakerName] = useState("");
  const [selectedSizes, setSelectedSizes] = useState([]);
  const [selectedBrands, setSelectedBrands] = useState([]);

  const availableSizes = ["40", "41", "42", "43", "44", "45"];
  const availableBrands = ["Nike", "Adidas", "Puma", "Reebok", "New Balance"];

  const toggleSizeSelection = (size) => {
    setSelectedSizes((prevSizes) =>
      prevSizes.includes(size) ? prevSizes.filter((s) => s !== size) : [...prevSizes, size]
    );
  };

  const toggleBrandSelection = (brand) => {
    setSelectedBrands((prevBrands) =>
      prevBrands.includes(brand) ? prevBrands.filter((b) => b !== brand) : [...prevBrands, brand]
    );
  };

  return (
    <>
      {/* ✅ Затемненный фон при открытом меню */}
      {isSidebarOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-md" onClick={handleCloseSidebar}></div>
      )}

      {/* ✅ Боковое окно фильтрации */}
      <div
        className={`fixed top-0 left-0 h-full w-[450px] bg-white shadow-lg transform transition-transform duration-300 ${
          isSidebarOpen ? "translate-x-0" : "translate-x-[-100%]"
        }`}
      >
        <div className="p-10 flex flex-col h-full">
          <h2 className="text-xl font-bold text-neutral-600 mb-10">Фильтрация товаров</h2>

          {/* ✅ Поле ввода названия кроссовок */}
          <label className="block text-sm font-medium text-gray-600">Название кроссовок</label>
          <input
            type="text"
            className={`w-full mt-3 p-2 border rounded transition ${
              sneakerName.length > 0 ? "border-yellow-500" : "border-gray-300"
            }`}
            placeholder="Введите название..."
            value={sneakerName}
            onChange={(e) => setSneakerName(e.target.value)}
          />

          {/* ✅ Поля ввода минимальной и максимальной цены */}
          <label className="block text-sm font-medium text-gray-600 mt-5">Цена (мин.)</label>
          <input
            type="number"
            className={`w-full mt-3 p-2 border rounded transition ${
              minPrice.length > 0 ? "border-yellow-500" : "border-gray-300"
            }`}
            placeholder="От 0$"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
          />

          <label className="block text-sm font-medium text-gray-600 mt-5">Цена (макс.)</label>
          <input
            type="number"
            className={`w-full mt-3 p-2 border rounded transition ${
              maxPrice.length > 0 ? "border-yellow-500" : "border-gray-300"
            }`}
            placeholder="До 500$"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />

          {/* ✅ Выбор размера (можно выбрать несколько) */}
          <label className="block text-sm font-medium text-gray-600 mt-5">Размер</label>
          <div className="flex gap-2 mt-3 flex-wrap">
            {availableSizes.map((size) => (
              <button
                key={size}
                className={`px-3 py-1 border rounded-md transition-all ${
                  selectedSizes.includes(size)
                    ? "bg-yellow-500 text-white font-bold border-yellow-600"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                }`}
                onClick={() => toggleSizeSelection(size)}
              >
                {size}
              </button>
            ))}
          </div>

          {/* ✅ Выбор бренда (галочка + уменьшенные кубики) */}
          <label className="block text-sm font-medium text-gray-600 mt-5">Бренды</label>
          <div className="flex flex-col mt-3 gap-2">
            {availableBrands.map((brand) => (
              <div
                key={brand}
                className="flex justify-between items-center cursor-pointer"
                onClick={() => toggleBrandSelection(brand)}
              >
                <span className="text-gray-700 font-medium">{brand}</span>
                <button
                  className={`w-5 h-5 border rounded-md flex items-center justify-center transition-all ${
                    selectedBrands.includes(brand)
                      ? "bg-yellow-500 border-yellow-600"
                      : "bg-gray-200 hover:bg-gray-300"
                  }`}
                >
                  {selectedBrands.includes(brand) && <span className="text-black font-bold">✓</span>}
                </button>
              </div>
            ))}
          </div>

          {/* ✅ Кнопка "Применить" в правом нижнем углу */}
          <div className="flex-1 flex items-end justify-end">
            <button
              className="px-6 py-3 border border-yellow-500 text-yellow-500 bg-white rounded-md hover:bg-yellow-500 hover:text-white transition-all"
              onClick={() => applyFilters({ sneakerName, minPrice, maxPrice, selectedSizes, selectedBrands })}
            >
              Применить
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
