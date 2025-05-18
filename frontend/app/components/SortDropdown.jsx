"use client";
import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation"; // ✅ App Router для управления URL

const SortDropdown = () => {
  const searchParams = useSearchParams();
  const router = useRouter();

  // ✅ Берём текущую сортировку из URL
  const currentSortBy = searchParams.get("sort_by") || "";
  const currentOrder = searchParams.get("order") || "";
  const [selected, setSelected] = useState("default");

  const sortOptions = [
    { value: "default", label: "По умолчанию", sortBy: "", order: "" },
    { value: "new", label: "Новинки", sortBy: "created_at", order: "desc" },
    { value: "price-asc", label: "Цена (по возрастанию)", sortBy: "price", order: "asc" },
    { value: "price-desc", label: "Цена (по убыванию)", sortBy: "price", order: "desc" },
  ];

  // ✅ Автоматически обновляем `selected`, если меняется URL
  useEffect(() => {
    const matchedOption = sortOptions.find(
      (option) => option.sortBy === currentSortBy && option.order === currentOrder
    );
    setSelected(matchedOption ? matchedOption.value : "default");
  }, [currentSortBy, currentOrder]); // Обновляем при изменении параметров

  const handleSelect = (event) => {
    const selectedOption = sortOptions.find((option) => option.value === event.target.value);
    setSelected(event.target.value);

    const newParams = new URLSearchParams(searchParams.toString());

    if (selectedOption.sortBy) {
      newParams.set("sort_by", selectedOption.sortBy);
      newParams.set("order", selectedOption.order);
    } else {
      newParams.delete("sort_by");
      newParams.delete("order");
    }

    router.push(`/catalog${newParams.toString() ? "?" + newParams.toString() : ""}`);
  };

  return (
    <div className="w-[200px]">
      <select
        value={selected}
        onChange={handleSelect}
        className="w-full px-6 py-3 border border-yellow-500 text-yellow-500 bg-white rounded-md hover:bg-yellow-500 hover:text-white shadow-md font-semibold cursor-pointer transition-all focus:outline-none"
      >
        {sortOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SortDropdown;
