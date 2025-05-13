"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <header className="fixed top-0 left-0 w-full bg-neutral-900 text-white shadow-md py-1 z-50">
      <nav className="container mx-auto px-6">
        <ul className="flex justify-between w-full items-center">

            <li className="ml-1">
  <a href="/" className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
    <img src="/Lemon.png" alt="Логотип" className="h-7 w-7"/>
  </a>
</li>


          <div className="flex space-x-4 text-xl">
              <li className="text-center">
                <Link href="/catalog" className="hover:text-gray-400 transition inline-block px-2 py-2">
                  Каталог
                </Link>
              </li>
              <li className="text-center">
                <Link href="/men" className="hover:text-gray-400 transition inline-block px-2 py-2">
                  Мужское
                </Link>
              </li>
              <li className="text-center">
                <Link href="/women" className="hover:text-gray-400 transition inline-block px-2 py-2">
                  Женское
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

          <div className="flex space-x-3 mr-6">
              <li className="text-center">
                <button className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
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
          </div>
        </ul>
      </nav>
    </header>
  );
}
