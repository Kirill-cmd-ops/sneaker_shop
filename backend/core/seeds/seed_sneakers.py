from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.models.sneaker import Sneaker

async def seed_sneakers(db: AsyncSession):
    sneakers = [
        Sneaker(name="Air Max 90", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_air_max.jpg"),
        Sneaker(name="Yellow", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_yellow.jpg"),
        Sneaker(name="AL8", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_al8.png"),
        Sneaker(name="DH", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_dh.jpeg"),
        Sneaker(name="DN", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_dn.jpg"),
        Sneaker(name="Jordan", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_jordan.jpg"),
        Sneaker(name="React", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_react.jpg"),
        Sneaker(name="Intertop", description="Классический дизайн", price=120.99, brand_id=1, image_url="/uploads/sneakers/nike_intertop.jpg"),

        Sneaker(name="Ferrari", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_ferrari.jpg"),
        Sneaker(name="Palermo", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_palermo.png"),
        Sneaker(name="Park", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_Park.png"),
        Sneaker(name="Roma", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_Roma.jpg"),
        Sneaker(name="RS-X", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_rs-x.png"),
        Sneaker(name="SL", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_sl.png"),
        Sneaker(name="Suede", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_suede.jpg"),
        Sneaker(name="Trinity", description="Классический дизайн", price=120.99, brand_id=3, image_url="/uploads/sneakers/puma_trinity.jpg"),

        Sneaker(name="Authetic", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_authetic.png"),
        Sneaker(name="Hevy", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_hevy.png"),
        Sneaker(name="Old", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_old.jpg"),
        Sneaker(name="Old Scholl", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_old_scholl.png"),
        Sneaker(name="Primary", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_Primary.png"),
        Sneaker(name="Ssk8", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_Sk8.png"),
        Sneaker(name="Skooll", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_skool.png"),
        Sneaker(name="Slip", description="Классический дизайн", price=120.99, brand_id=4, image_url="/uploads/sneakers/vans_slip.jpg"),

        Sneaker(name="Centennial", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_centennial.jpg"),
        Sneaker(name="Byuty", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_daroga.jpg"),
        Sneaker(name="Eclyptix", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_eclyptix.png"),
        Sneaker(name="Fenesi", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_fenesi.jpg"),
        Sneaker(name="Ozweego", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_ozweego.png"),
        Sneaker(name="Runfalcon", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_runfalcon.jpg"),
        Sneaker(name="Temper", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_runfalcon.png"),
        Sneaker(name="Daffy", description="Максимальная амортизация", price=123.50, brand_id=2, image_url="/uploads/sneakers/adidas_temper.jpg"),

    ]
    db.add_all(sneakers)
    await db.flush()
    await db.commit()

