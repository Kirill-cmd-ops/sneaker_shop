import { useState } from "react";

const SortDropdown = ({ onChange }) => {
  const [selected, setSelected] = useState("default");
  const sortOptions = [
    { value: "new", label: "Новинки" },
    { value: "price-asc", label: "Цена (по возрастанию)" },
    { value: "price-desc", label: "Цена (по убыванию)" },
  ];

  const handleSelect = (event) => {
    setSelected(event.target.value);
    onChange(event.target.value);
  };

  return (
    <div className="w-[150px] mt-4">
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
