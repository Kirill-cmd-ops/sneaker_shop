export default function Footer() {
  return (
    <footer className="bg-neutral-900 text-white py-6 mt-auto border-t border-neutral-700">
      <div className="container mx-auto flex justify-between items-start text-sm px-6">

        {/* ✅ Колонка 1: Телефон + Email */}
        <div className="flex flex-col space-y-2">
          <p className="text-lg font-semibold">Контактная информация:</p>
          <p>
            📞 Телефон:
            <a href="tel:+375291480025" className="text-white font-medium hover:text-gray-300 transition">
              +375-29-148-00-25
            </a>
          </p>
          <p>
            📞 Телефон поддержки:
            <a href="tel:+375442471203" className="text-white font-medium hover:text-gray-300 transition">
              +375-44-247-12-03
            </a>
          </p>
          <p>
            📧 Почта:
            <a href="mailto:kugoshoping@gmail.com" className="text-white font-medium hover:text-gray-300 transition">
              kugoshoping@gmail.com
            </a>
          </p>
        </div>

        {/* ✅ Колонка 2: Время работы + Адреса (теперь центрировано) */}
        <div className="flex flex-col space-y-4 items-center text-center">
          <p className="text-lg font-semibold">Время работы:</p>
          <p className="font-medium">10:00 - 20:00 (без выходных)</p>

          <p className="text-lg font-semibold">Адреса магазинов:</p>
          <p>
            Минск:
            <a href="https://yandex.ru/maps/?text=Минск, Ленинская 12" className="text-white font-medium hover:text-gray-300 transition" target="_blank">
              Ленинская 12
            </a>
          </p>
          <p>
            Брест:
            <a href="https://yandex.ru/maps/?text=Брест, Витовская 3" className="text-white font-medium hover:text-gray-300 transition" target="_blank">
              Витовская 3
            </a>
          </p>
        </div>

        {/* ✅ Колонка 3: Социальные сети (опущена ниже) */}
        <div className="flex flex-col items-center space-y-4 mt-6">
          <p className="text-lg font-semibold">Мы в соцсетях:</p>
          <div className="flex gap-6">
            <button className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
              <img src="/instagram.svg" alt="Instagram" className="h-10 w-10" style={{ filter: "invert(1)" }} />
            </button>
            <button className="cursor-pointer transition duration-300 ease-in-out p-2 hover:brightness-75">
              <img src="/telegram.svg" alt="Telegram" className="h-10 w-10" style={{ filter: "invert(1)" }} />
            </button>
          </div>
        </div>

      </div>
    </footer>
  );
}
