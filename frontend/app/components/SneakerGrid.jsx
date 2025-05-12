const SneakerGrid = ({ sneakers, cols }) => (
  <div className={`grid ${cols} gap-6 mt-6`}>
    {sneakers?.map(({ id, name, price, brand, image_url }) => (
      <div key={id} className="w-[450px] h-[450px] text-center transition-transform duration-300 hover:scale-105">
        <img src={`http://localhost:8000${image_url}`} alt={name} className="w-100 h-70 object-cover mx-auto" />
        <h2 className="text-3xl text-gray-500 mt-3">{brand.name}</h2>
        <h2 className="text-3xl text-gray-500 mt-2">{name}</h2>
        <p className="text-3xl text-gray-600 mt-2">
          <span className="font-bold text-black">{price}</span> Br
        </p>
      </div>
    ))}
  </div>
);

export default SneakerGrid;
