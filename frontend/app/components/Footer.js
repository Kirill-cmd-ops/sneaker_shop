export default function Footer() {
  return (
    <footer className="bg-neutral-900 text-white text-center py-6 mt-auto border-t border-neutral-700">
      <div className="flex flex-col items-center space-y-2">
        <p className="text-lg font-semibold">Контактная информация:</p>
        <p className="text-sm">
          📞 Телефон:
          <a href="tel:+375291480025" className="text-white font-medium hover:text-gray-300 transition">
            +375-29-148-00-25
          </a>
        </p>
        <p className="text-sm">
          📞 Телефон поддержки:
          <a href="tel:+375442471203" className="text-white font-medium hover:text-gray-300 transition">
            +375-44-247-12-03
          </a>
        </p>
        <p className="text-sm">
          📧 Почта:
          <a href="mailto:kugoshoping@gmail.com" className="text-white font-medium hover:text-gray-300 transition">
            kugoshoping@gmail.com
          </a>
        </p>
        <p className="text-sm">🕒 Время работы: <span className="font-medium">10:00 - 20:00 (без выходных)</span></p>
        <p className="text-sm">📍 Адреса магазинов:</p>
        <p className="text-sm">
          📌 Минск:
          <a href="https://yandex.ru/maps/?text=Минск, Ленинская 12" className="text-white font-medium hover:text-gray-300 transition" target="_blank">
            Ленинская 12
          </a>
        </p>
        <p className="text-sm">
          📌 Брест:
          <a href="https://yandex.ru/maps/?text=Брест, Витовская 3" className="text-white font-medium hover:text-gray-300 transition" target="_blank">
            Витовская 3
          </a>
        </p>
      </div>
    </footer>
  );
}
