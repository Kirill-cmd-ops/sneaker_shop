const SneakerGrid = ({ sneakers, cols }) => (
  <div className={`grid ${cols} gap-x-6 gap-y-10 mt-6 justify-center`}>
    {sneakers?.map(({ id, name, price, brand, image_url }) => (
      <div
        key={id}
        className="w-[400px] h-[500px] text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white"
      >
        <img
          src={`http://localhost:8000${image_url}`}
          alt={name}
          className="w-full h-[250px] object-cover rounded-md mx-auto"
        />
        <h2 className="text-2xl text-gray-500 mt-3">{brand.name}</h2>
        <h2 className="text-2xl text-gray-500 mt-2">{name}</h2>
        <p className="text-2xl text-gray-600 mt-2">
          <span className="font-bold text-black">{price}</span> Br
        </p>
      </div>
    ))}
  </div>
);

export default SneakerGrid;
