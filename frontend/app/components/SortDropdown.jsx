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
        className="w-full px-4 py-2 bg-yellow-500 border border-yellow-600 rounded-lg shadow-md text-black font-semibold cursor-pointer focus:outline-none hover:bg-yellow-600 transition-all"
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
