"use client";
import { useState } from "react";
import Link from "next/link";
import SearchBar from "./SearchBar";

export default function Navbar() {
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 w-full bg-neutral-900 text-white shadow-md py-1 z-50">
      <nav className="container mx-auto px-6">
        <ul className="flex justify-between w-full items-center">

          {/* Логотип */}
          <li className="ml-1">
            <a href="/" className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
              <img src="/lemon_logo.png" alt="Логотип" className="h-9 w-14" />
            </a>
          </li>

          {/* Навигационное меню */}
          <div className="flex space-x-4 text-xl">
            <li className="text-center">
              <Link href="/catalog" className="hover:text-gray-400 transition inline-block px-2 py-2">
                Каталог
              </Link>
            </li>
            <li className="text-center">
              <Link href="/catalog?gender=Мужские" className="hover:text-gray-400 transition inline-block px-2 py-2">
                Мужские
              </Link>
            </li>
            <li className="text-center">
              <Link href="/catalog?gender=Женские" className="hover:text-gray-400 transition inline-block px-2 py-2">
                Женские
              </Link>
            </li>
            <li className="text-center">
              <Link href="/catalog?gender=Унисекс" className="hover:text-gray-400 transition inline-block px-2 py-2">
                Унисекс
              </Link>
            </li>
            <li className="text-center">
              <Link href="/sales" className="hover:text-gray-400 transition inline-block px-2 py-2">
                Акции
              </Link>
            </li>
            <li className="text-center">
              <Link href="/about" className="hover:text-gray-400 transition inline-block px-2 py-2">
                О нас
              </Link>
            </li>
          </div>

          <div className="flex items-center space-x-3 mr-6">
  <li className="text-center">
    <button
      onClick={() => setIsSearchOpen(!isSearchOpen)}
      className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75"
    >
      <img src="/search.svg" alt="Поиск" className="h-7 w-7" style={{ filter: "invert(1)" }} />
    </button>
  </li>
  <li className="text-center">
    <button className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
      <img src="/heart.svg" alt="Избранное" className="h-7 w-7" style={{ filter: "invert(1)" }} />
    </button>
  </li>
  <li className="text-center">
    <button className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
      <img src="/basket.svg" alt="Корзина" className="h-7 w-7" style={{ filter: "invert(1)" }} />
    </button>
  </li>
  <li className="text-center">
    <Link href="/register" className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
      <img src="/avatar.svg" alt="Аватарка" className="h-7 w-7" style={{ filter: "invert(1)" }} />
    </Link>
  </li>
</div>

        </ul>
      </nav>

      {/* ✅ Показываем `SearchBar`, если `isSearchOpen === true` */}
      {isSearchOpen && <SearchBar isOpen={isSearchOpen} toggleSearch={() => setIsSearchOpen(false)} />}
    </header>
  );
}
