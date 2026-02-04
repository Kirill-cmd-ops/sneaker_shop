"use client";

import React from "react";
import { useRouter } from "next/navigation";

function PromotionsPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-amber-50 pt-24">
      {/* Фиксированный контейнер для всех компьютеров */}
      <div className="w-[1200px] max-w-[1200px] mx-auto px-8 py-16">
        {/* Декоративные элементы */}
        <div className="absolute top-32 right-[calc(50%-600px+200px)] w-80 h-80 bg-yellow-100 rounded-full opacity-20 blur-3xl"></div>
        <div className="absolute bottom-32 left-[calc(50%-600px+200px)] w-80 h-80 bg-amber-100 rounded-full opacity-20 blur-3xl"></div>

        {/* Основной блок */}
        <div className="relative bg-white rounded-3xl shadow-2xl overflow-hidden border border-amber-200">
          {/* Верхняя декоративная полоса */}
          <div className="h-4 bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-400"></div>

          <div className="p-16 text-center">
            {/* Иконка с центровкой */}
            <div className="flex justify-center mb-12">
              <div className="relative">
                <div className="w-32 h-32 bg-gradient-to-br from-amber-100 to-yellow-100 rounded-full flex items-center justify-center border-4 border-amber-200">
                  <svg
                    className="w-16 h-16 text-amber-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.5"
                      d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div className="absolute -top-4 -right-4 bg-yellow-500 text-white rounded-full w-16 h-16 flex items-center justify-center animate-bounce shadow-lg">
                  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Заголовок */}
            <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
              <span className="bg-gradient-to-r from-amber-500 to-yellow-500 bg-clip-text text-transparent">
                Раздел акций в разработке
              </span>
            </h1>

            {/* Описание */}
            <div className="text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              <p className="mb-6">
                В данный момент активных акций нет. Мы активно работаем над созданием специальных предложений для наших клиентов.
              </p>
              <p>
                Ожидайте запуск раздела в ближайшее время!
              </p>
            </div>

            {/* Статус разработки */}
            <div className="inline-flex items-center px-8 py-4 bg-amber-50 text-amber-700 rounded-full font-bold text-lg mb-12 border-2 border-amber-200 shadow-sm">
              <svg
                className="w-6 h-6 mr-3 animate-spin"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Функция в активной разработке
            </div>

            {/* Блок с преимуществами */}
            <div className="grid grid-cols-3 gap-8 mb-16">
              <div className="bg-amber-50 rounded-2xl p-8 border border-amber-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-6 mx-auto">
                  <svg className="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h4 className="font-bold text-xl text-gray-900 mb-3">Специальные скидки</h4>
                <p className="text-gray-600">Уникальные предложения на популярные модели</p>
              </div>

              <div className="bg-amber-50 rounded-2xl p-8 border border-amber-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-6 mx-auto">
                  <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h4 className="font-bold text-xl text-gray-900 mb-3">Сезонные распродажи</h4>
                <p className="text-gray-600">Большие скидки в конце сезона</p>
              </div>

              <div className="bg-amber-50 rounded-2xl p-8 border border-amber-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mb-6 mx-auto">
                  <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h4 className="font-bold text-xl text-gray-900 mb-3">Эксклюзивные акции</h4>
                <p className="text-gray-600">Ограниченные по времени предложения</p>
              </div>
            </div>

            {/* Прогресс бар */}
            <div className="mb-16 bg-white rounded-2xl p-10 border-2 border-amber-200 shadow-lg">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900">Прогресс разработки</h3>
                <span className="text-2xl font-bold text-amber-600">85%</span>
              </div>

              <div className="w-full bg-amber-100 rounded-full h-4 mb-4">
                <div
                  className="bg-gradient-to-r from-amber-400 to-yellow-400 h-4 rounded-full transition-all duration-1000 ease-out shadow-inner"
                  style={{ width: '85%' }}
                ></div>
              </div>

              <p className="text-lg text-gray-600 text-center">
                Мы активно работаем над разделом акций. Ожидайте запуск в ближайшее время!
              </p>
            </div>

            {/* Кнопки действий */}
            <div className="flex justify-center gap-8 mb-16">
              <button
                onClick={() => router.push('/catalog')}
                className="px-12 py-5 bg-gradient-to-r from-amber-500 to-yellow-500 text-white font-bold text-xl rounded-2xl hover:from-amber-600 hover:to-yellow-600 transition-all hover:shadow-2xl flex items-center justify-center gap-3 min-w-[240px]"
              >
                <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7" />
                </svg>
                Перейти в каталог
              </button>

              <button
                onClick={() => router.push('/')}
                className="px-12 py-5 bg-white text-amber-600 font-bold text-xl rounded-2xl border-3 border-amber-600 hover:bg-amber-50 transition-all hover:shadow-lg min-w-[240px]"
              >
                На главную
              </button>
            </div>

            {/* Контактная информация */}
            <div className="pt-12 border-t-2 border-amber-100">
              <p className="text-xl text-gray-700 mb-6">
                Есть вопросы или предложения по акциям?
              </p>
              <div className="flex flex-col items-center gap-4">
                <a
                  href="mailto:kugoshoping@gmail.com"
                  className="text-2xl text-amber-600 hover:text-amber-800 font-bold inline-flex items-center gap-3 hover:scale-105 transition-transform"
                >
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  kugoshoping@gmail.com
                </a>
                <p className="text-lg text-gray-500 max-w-2xl">
                  Напишите нам, мы всегда рады обратной связи и готовы рассмотреть ваши предложения по будущим акциям
                </p>
              </div>
            </div>

            {/* Социальные сети */}
            <div className="mt-12 pt-10 border-t-2 border-amber-100">
              <p className="text-xl text-gray-600 mb-8">
                Подпишитесь, чтобы первыми узнавать о новых акциях
              </p>
              <div className="flex justify-center gap-6">
                <button className="w-14 h-14 bg-amber-100 rounded-full flex items-center justify-center hover:bg-amber-200 transition-all hover:scale-110 shadow-md">
                  <svg className="w-7 h-7 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                  </svg>
                </button>
                <button className="w-14 h-14 bg-amber-100 rounded-full flex items-center justify-center hover:bg-amber-200 transition-all hover:scale-110 shadow-md">
                  <svg className="w-7 h-7 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                </button>
                <button className="w-14 h-14 bg-amber-100 rounded-full flex items-center justify-center hover:bg-amber-200 transition-all hover:scale-110 shadow-md">
                  <svg className="w-7 h-7 text-amber-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Стили для фиксированной ширины */}
      <style jsx>{`
        @media (max-width: 1200px) {
          .container {
            width: 100% !important;
            max-width: 100% !important;
            padding-left: 24px !important;
            padding-right: 24px !important;
          }
        }

        @media (max-width: 768px) {
          .container {
            padding-left: 16px !important;
            padding-right: 16px !important;
          }

          .grid-cols-3 {
            grid-template-columns: 1fr !important;
            gap: 24px !important;
          }

          .flex {
            flex-direction: column !important;
          }

          .text-5xl {
            font-size: 2.5rem !important;
          }

          .text-2xl {
            font-size: 1.5rem !important;
          }
        }
      `}</style>
    </div>
  );
}

export default PromotionsPage;