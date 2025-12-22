from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from stock_notification_service.stock_notification.models import Sneaker


async def seed_sneakers(session: AsyncSession):
    sneakers = [
        {
            "name": "Air Zoom Pegasus",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_pegasus.png",
        },
        {
            "name": "Ultraboost Classic",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_ultraboost.png",
        },
        {
            "name": "RS-X Bold",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_rsx.png",
        },
        {
            "name": "Old Skool Canvas",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_oldskool.png",
        },
        {
            "name": "XT-6 Trail",
            "brand_id": 5,
            "image_url": "/uploads/sneakers/salomon_xt6.png",
        },
        {
            "name": "Gel-Kayano 28",
            "brand_id": 6,
            "image_url": "/uploads/sneakers/asics_kayano.png",
        },
        {
            "name": "Fresh Foam X",
            "brand_id": 7,
            "image_url": "/uploads/sneakers/newbalance_freshfoam.png",
        },
        {
            "name": "Classic Leather",
            "brand_id": 8,
            "image_url": "/uploads/sneakers/reebok_classic.png",
        },
        {
            "name": "Chuck Taylor All Star",
            "brand_id": 9,
            "image_url": "/uploads/sneakers/converse_chuck.png",
        },
        {
            "name": "Air Jordan 1",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_1.png",
        },
        {
            "name": "HOVR Phantom",
            "brand_id": 11,
            "image_url": "/uploads/sneakers/underarmour_hovr.png",
        },
        {
            "name": "Kinvara Lite",
            "brand_id": 12,
            "image_url": "/uploads/sneakers/saucony_kinvara.png",
        },
        {
            "name": "Disruptor II",
            "brand_id": 13,
            "image_url": "/uploads/sneakers/fila_disruptor.png",
        },
        {
            "name": "Hoka Clifton",
            "brand_id": 14,
            "image_url": "/uploads/sneakers/hoka_clifton.png",
        },
        {
            "name": "Wave Rider",
            "brand_id": 15,
            "image_url": "/uploads/sneakers/mizuno_waverider.png",
        },
        {
            "name": "Diadora N9000",
            "brand_id": 16,
            "image_url": "/uploads/sneakers/diadora_n9000.png",
        },
        {
            "name": "Brooks Ghost",
            "brand_id": 17,
            "image_url": "/uploads/sneakers/brooks_ghost.png",
        },
        {
            "name": "Kappa Retro",
            "brand_id": 18,
            "image_url": "/uploads/sneakers/kappa_retro.png",
        },
        {
            "name": "Trail Runner Pro",
            "brand_id": 5,
            "image_url": "/uploads/sneakers/salomon_trail.png",
        },
        {
            "name": "City Walker",
            "brand_id": 8,
            "image_url": "/uploads/sneakers/reebok_citywalker.png",
        },
        {
            "name": "Skate Pro",
            "brand_id": 4,
            "image_url": "/uploads/sneakers/vans_skatepro.png",
        },
        {
            "name": "Court Classic",
            "brand_id": 9,
            "image_url": "/uploads/sneakers/converse_court.png",
        },
        {
            "name": "Speedster",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_speedster.png",
        },
        {
            "name": "Everyday Comfort",
            "brand_id": 7,
            "image_url": "/uploads/sneakers/newbalance_everyday.png",
        },
        {
            "name": "Court Ace",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_courtace.png",
        },
        {
            "name": "Urban Runner",
            "brand_id": 3,
            "image_url": "/uploads/sneakers/puma_urbanrunner.png",
        },
        {
            "name": "Retro Runner",
            "brand_id": 13,
            "image_url": "/uploads/sneakers/fila_retrorunner.png",
        },
        {
            "name": "All Terrain GTX",
            "brand_id": 5,
            "image_url": "/uploads/sneakers/salomon_gtx.png",
        },
        {
            "name": "Minimal Trainer",
            "brand_id": 12,
            "image_url": "/uploads/sneakers/saucony_minimal.png",
        },
        {
            "name": "Heritage Classic",
            "brand_id": 8,
            "image_url": "/uploads/sneakers/reebok_heritage.png",
        },
        {
            "name": "Air Force 1 Low",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_low.png",
        },
        {
            "name": "Dunk Low Retro",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_low.png",
        },
        {
            "name": "Jordan 4 Retro",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_4.png",
        },
        {
            "name": "Jordan 11 Concord",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_11_concord.png",
        },
        {
            "name": "Jordan 5 Retro",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_5.png",
        },
        {
            "name": "Jordan 6 Retro",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_6.png",
        },
        {
            "name": "Jordan 7 Retro",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_7.png",
        },
        {
            "name": "Air Force 1 High",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_high.png",
        },
        {
            "name": "Dunk High Premium",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_high.png",
        },
        {
            "name": "Air Force 1 Shadow",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_shadow.png",
        },
        {
            "name": "Superstar Classic",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_superstar.png",
        },
        {
            "name": "Spezial OG",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_spezial.png",
        },
        {
            "name": "Forum Low",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_forum.png",
        },
        {
            "name": "Yeezy Runner (inspired)",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_yeezy_like.png",
        },
        {
            "name": "Campus 80s",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_campus.png",
        },
        {
            "name": "Gazelle Vintage",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_gazelle.png",
        },
        {
            "name": "Stan Smith Premium",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_stansmith.png",
        },
        {
            "name": "Superstar Bold",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_superstar_bold.png",
        },
        {
            "name": "Dame Retro (inspired)",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_dame_like.png",
        },
        {
            "name": "Spezial Low",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_spezial_low.png",
        },
        {
            "name": "Air Force 1 Utility",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_utility.png",
        },
        {
            "name": "Dunk SB Pro",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_sb.png",
        },
        {
            "name": "Jordan 4 Retro SE",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_4_se.png",
        },
        {
            "name": "Jordan 5 Off-White (inspired)",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_5_collab.png",
        },
        {
            "name": "Superstar Platform",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_superstar_platform.png",
        },
        {
            "name": "Dunk Low Premium Pack",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_premium.png",
        },
        {
            "name": "Jordan 11 Retro Low",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_11_low.png",
        },
        {
            "name": "Air Force 1 Pixel",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_pixel.png",
        },
        {
            "name": "Superstar Vintage",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_superstar_vintage.png",
        },
        {
            "name": "Dunk Low City Pack",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_citypack.png",
        },
        {
            "name": "Air Force 1 Low Premium",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_premium.png",
        },
        {
            "name": "Dunk Low Retro OG",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_dunk_low_og.png",
        },
        {
            "name": "Jordan 4 Retro OG",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_4_og.png",
        },
        {
            "name": "Jordan 11 Retro IE",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_11_ie.png",
        },
        {
            "name": "Jordan 5 Retro Low",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_5_low.png",
        },
        {
            "name": "Superstar Core",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_superstar_core.png",
        },
        {
            "name": "Spezial Reissue",
            "brand_id": 2,
            "image_url": "/uploads/sneakers/adidas_spezial_reissue.png",
        },
        {
            "name": "Air Jordan 6 Retro",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_6_retro.png",
        },
        {
            "name": "Air Jordan 7 Retro Low",
            "brand_id": 10,
            "image_url": "/uploads/sneakers/jordan_7_low.png",
        },
        {
            "name": "Air Force 1 Utility Mid",
            "brand_id": 1,
            "image_url": "/uploads/sneakers/nike_af1_utility_mid.png",
        },
    ]

    stmt = insert(Sneaker).values(sneakers)
    await session.execute(stmt)
    await session.commit()
