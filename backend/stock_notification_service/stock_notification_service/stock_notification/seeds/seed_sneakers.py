from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import Sneaker


async def seed_sneakers(session: AsyncSession):
    sneakers = [
        {
            "name": "Air Max",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_air_max.png",
        },
        {
            "name": "Yellow",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_yellow.jpg",
        },
        {
            "name": "AL8",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_al8.png",
        },
        {
            "name": "DH",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dh.jpeg",
        },
        {
            "name": "DN",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dn.jpg",
        },
        {
            "name": "Jordan",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_jordan.jpg",
        },
        {
            "name": "React",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_react.jpg",
        },
        {
            "name": "Intertop",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_intertop.jpg",
        },
        {
            "name": "Ferrari",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_ferrari.jpg",
        },
        {
            "name": "Palermo",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_palermo.png",
        },
        {
            "name": "Park",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_Park.png",
        },
        {
            "name": "Roma",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_Roma.jpg",
        },
        {
            "name": "RS-X",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_rs-x.png",
        },
        {
            "name": "SL",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_sl.png",
        },
        {
            "name": "Suede",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_suede.jpg",
        },
        {
            "name": "Trinity",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_trinity.jpg",
        },
        {
            "name": "Authetic",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_authetic.png",
        },
        {
            "name": "Hevy",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_hevy.png",
        },
        {
            "name": "Old",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_old.jpg",
        },
        {
            "name": "Old Scholl",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_old_scholl.png",
        },
        {
            "name": "Primary",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_Primary.png",
        },
        {
            "name": "Ssk8",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_Sk8.png",
        },
        {
            "name": "Skooll",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_skool.png",
        },
        {
            "name": "Slip",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_slip.jpg",
        },
        {
            "name": "Centennial",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_centennial.jpg",
        },
        {
            "name": "Byuty",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_daroga.jpg",
        },
        {
            "name": "Eclyptix",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_eclyptix.png",
        },
        {
            "name": "Fenesi",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_fenesi.jpg",
        },
        {
            "name": "Ozweego",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_ozweego.png",
        },
        {
            "name": "Runfalcon",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_runfalcon.jpg",
        },
        {
            "name": "Temper",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_runfalcon.png",
        },
        {
            "name": "Daffy",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_temper.jpg",
        },
    ]

    stmt = insert(Sneaker).values(sneakers)
    await session.execute(stmt)
    await session.commit()
