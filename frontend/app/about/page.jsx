"use client";
import React from "react";

export default function AboutPage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-12">
      <img
        src="/lemon_logo.png"
        alt="Логотип магазина"
        className="w-[450px] h-auto mb-12 opacity-90"
      />

      <h1 className="text-6xl font-bold text-white mb-8 tracking-wide">О нас</h1>

      <section className="max-w-3xl text-center text-2xl text-gray-300 leading-relaxed">
        <p>Мы — новый магазин, который предлагает оригинальные кроссовки от мировых брендов.</p>
        <p className="mt-6">Наши цены приятно удивляют, ведь стиль и качество должны быть доступными каждому.</p>
        <p className="mt-6">Выбирайте лучшее — трендовые модели, комфорт и проверенное качество.</p>
        <p className="mt-6">
          Следите за нами в социальных сетях, чтобы быть в курсе новинок и эксклюзивных предложений!
        </p>
      </section>

      <div className="w-full h-[5px] bg-yellow-500 mt-40"></div>

      <div className="flex gap-8 mt-10">
        <button className="cursor-pointer transition duration-300 ease-in-out p-3 hover:brightness-75">
          <img
            src="/instagram.svg"
            alt="Instagram"
            className="h-[68px] w-[68px]"
            style={{ filter: "invert(1)" }}
          />
        </button>
        <button className="cursor-pointer transition duration-300 ease-in-out p-3 hover:brightness-75">
          <img
            src="/telegram.svg"
            alt="Telegram"
            className="h-[68px] w-[68px]"
            style={{ filter: "invert(1)" }}
          />
        </button>
      </div>
    </main>
  );
}
