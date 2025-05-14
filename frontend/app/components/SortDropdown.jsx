import { useState } from "react";

const SortDropdown = ({ setSortBy, setOrder }) => {
  const [selected, setSelected] = useState("default");

  const sortOptions = [
    { value: "default", label: "По умолчанию", sortBy: "", order: "" },
    { value: "new", label: "Новинки", sortBy: "created_at", order: "desc" },
    { value: "price-asc", label: "Цена (по возрастанию)", sortBy: "price", order: "asc" },
    { value: "price-desc", label: "Цена (по убыванию)", sortBy: "price", order: "desc" },
  ];

  const handleSelect = (event) => {
    const selectedOption = sortOptions.find(option => option.value === event.target.value);
    setSelected(event.target.value);
    setSortBy(selectedOption.sortBy);
    setOrder(selectedOption.order);
  };

  return (
    <div className="w-[200px] mt-4">
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
