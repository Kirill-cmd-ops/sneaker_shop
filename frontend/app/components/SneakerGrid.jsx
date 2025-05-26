"use client";
import { useEffect } from "react";

const SneakerGrid = ({ data, cols }) => {
  useEffect(() => {
    const savedPosition = sessionStorage.getItem("scrollPosition");
    if (savedPosition) {
      window.scrollTo(0, Number(savedPosition));
    }
  }, []);

  if (!data || !data.items)
    return <p className="text-center mt-10">Товары не найдены.</p>;

  return (
    <div className={`grid ${cols} gap-x-6 gap-y-10 mt-6 justify-center`}>
      {data.items.map(({ id, name, price, brand, image_url }) => (
        <a
          key={id}
          href={`/details?sneakerId=${id}`}
          className="relative w-[400px] h-[500px] text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white block hover:border-2 hover:border-yellow-500"
          onClick={() => sessionStorage.setItem("scrollPosition", window.scrollY)}
        >
          <div className="group relative">
            <img
              src={`http://localhost:8000${image_url}`}
              alt={name}
              className="w-full h-[250px] object-cover rounded-md mx-auto transition-all duration-300"
            />
            <div className="absolute inset-0 bg-white bg-opacity-30 flex flex-col items-center justify-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  e.preventDefault();
                }}
                className="w-40 bg-white border border-yellow-500 text-yellow-500 px-4 py-2 rounded-md transition-colors duration-300 hover:bg-yellow-500 hover:text-white"
              >
                В корзину
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  e.preventDefault();
                }}
                className="w-40 bg-white border border-yellow-500 text-yellow-500 px-4 py-2 rounded-md transition-colors duration-300 hover:bg-yellow-500 hover:text-white"
              >
                В избранное
              </button>
            </div>
          </div>
          <h2 className="text-2xl text-gray-500 mt-3">
            {brand?.name || "Без бренда"}
          </h2>
          <h2 className="text-2xl text-gray-500 mt-2">{name}</h2>
          <p className="text-xl text-gray-600 mt-2">
            <span className="font-bold text-black">{price}</span> Br
          </p>
        </a>
      ))}
    </div>
  );
};

export default SneakerGrid;
