from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from stock_notification_service.stock_notification.models import (
    SneakerSizeAssociation,
)


async def seed_sneaker_sizes(session: AsyncSession):

    sneaker_sizes = [
        # sneaker 1
        {"sneaker_id": 1, "size_id": 6, "quantity": 10},
        {"sneaker_id": 1, "size_id": 7, "quantity": 8},
        {"sneaker_id": 1, "size_id": 8, "quantity": 5},
        {"sneaker_id": 1, "size_id": 9, "quantity": 2},
        # sneaker 2
        {"sneaker_id": 2, "size_id": 6, "quantity": 12},
        {"sneaker_id": 2, "size_id": 7, "quantity": 7},
        {"sneaker_id": 2, "size_id": 8, "quantity": 4},
        {"sneaker_id": 2, "size_id": 9, "quantity": 1},
        # sneaker 3
        {"sneaker_id": 3, "size_id": 5, "quantity": 6},
        {"sneaker_id": 3, "size_id": 6, "quantity": 9},
        {"sneaker_id": 3, "size_id": 7, "quantity": 3},
        {"sneaker_id": 3, "size_id": 8, "quantity": 2},
        # sneaker 4
        {"sneaker_id": 4, "size_id": 4, "quantity": 15},
        {"sneaker_id": 4, "size_id": 5, "quantity": 10},
        {"sneaker_id": 4, "size_id": 6, "quantity": 6},
        {"sneaker_id": 4, "size_id": 7, "quantity": 2},
        # sneaker 5
        {"sneaker_id": 5, "size_id": 8, "quantity": 7},
        {"sneaker_id": 5, "size_id": 9, "quantity": 5},
        {"sneaker_id": 5, "size_id": 10, "quantity": 3},
        {"sneaker_id": 5, "size_id": 11, "quantity": 1},
        # sneaker 6
        {"sneaker_id": 6, "size_id": 7, "quantity": 8},
        {"sneaker_id": 6, "size_id": 8, "quantity": 6},
        {"sneaker_id": 6, "size_id": 9, "quantity": 4},
        {"sneaker_id": 6, "size_id": 10, "quantity": 2},
        # sneaker 7
        {"sneaker_id": 7, "size_id": 6, "quantity": 11},
        {"sneaker_id": 7, "size_id": 7, "quantity": 9},
        {"sneaker_id": 7, "size_id": 8, "quantity": 5},
        {"sneaker_id": 7, "size_id": 9, "quantity": 3},
        # sneaker 8
        {"sneaker_id": 8, "size_id": 5, "quantity": 14},
        {"sneaker_id": 8, "size_id": 6, "quantity": 10},
        {"sneaker_id": 8, "size_id": 7, "quantity": 6},
        {"sneaker_id": 8, "size_id": 8, "quantity": 2},
        # sneaker 9
        {"sneaker_id": 9, "size_id": 6, "quantity": 7},
        {"sneaker_id": 9, "size_id": 7, "quantity": 5},
        {"sneaker_id": 9, "size_id": 8, "quantity": 3},
        {"sneaker_id": 9, "size_id": 9, "quantity": 1},
        # sneaker 10
        {"sneaker_id": 10, "size_id": 6, "quantity": 4},
        {"sneaker_id": 10, "size_id": 7, "quantity": 3},
        {"sneaker_id": 10, "size_id": 8, "quantity": 2},
        {"sneaker_id": 10, "size_id": 9, "quantity": 1},
        # sneaker 11
        {"sneaker_id": 11, "size_id": 7, "quantity": 8},
        {"sneaker_id": 11, "size_id": 8, "quantity": 6},
        {"sneaker_id": 11, "size_id": 9, "quantity": 4},
        {"sneaker_id": 11, "size_id": 10, "quantity": 2},
        # sneaker 12
        {"sneaker_id": 12, "size_id": 5, "quantity": 9},
        {"sneaker_id": 12, "size_id": 6, "quantity": 7},
        {"sneaker_id": 12, "size_id": 7, "quantity": 5},
        {"sneaker_id": 12, "size_id": 8, "quantity": 2},
        # sneaker 13
        {"sneaker_id": 13, "size_id": 5, "quantity": 6},
        {"sneaker_id": 13, "size_id": 6, "quantity": 4},
        {"sneaker_id": 13, "size_id": 7, "quantity": 3},
        {"sneaker_id": 13, "size_id": 8, "quantity": 1},
        # sneaker 14
        {"sneaker_id": 14, "size_id": 8, "quantity": 12},
        {"sneaker_id": 14, "size_id": 9, "quantity": 8},
        {"sneaker_id": 14, "size_id": 10, "quantity": 5},
        {"sneaker_id": 14, "size_id": 11, "quantity": 2},
        # sneaker 15
        {"sneaker_id": 15, "size_id": 7, "quantity": 7},
        {"sneaker_id": 15, "size_id": 8, "quantity": 5},
        {"sneaker_id": 15, "size_id": 9, "quantity": 3},
        {"sneaker_id": 15, "size_id": 10, "quantity": 1},
        # sneaker 16
        {"sneaker_id": 16, "size_id": 6, "quantity": 10},
        {"sneaker_id": 16, "size_id": 7, "quantity": 6},
        {"sneaker_id": 16, "size_id": 8, "quantity": 4},
        {"sneaker_id": 16, "size_id": 9, "quantity": 2},
        # sneaker 17
        {"sneaker_id": 17, "size_id": 7, "quantity": 9},
        {"sneaker_id": 17, "size_id": 8, "quantity": 6},
        {"sneaker_id": 17, "size_id": 9, "quantity": 4},
        {"sneaker_id": 17, "size_id": 10, "quantity": 2},
        # sneaker 18
        {"sneaker_id": 18, "size_id": 5, "quantity": 11},
        {"sneaker_id": 18, "size_id": 6, "quantity": 8},
        {"sneaker_id": 18, "size_id": 7, "quantity": 5},
        {"sneaker_id": 18, "size_id": 8, "quantity": 2},
        # sneaker 19
        {"sneaker_id": 19, "size_id": 8, "quantity": 7},
        {"sneaker_id": 19, "size_id": 9, "quantity": 5},
        {"sneaker_id": 19, "size_id": 10, "quantity": 3},
        {"sneaker_id": 19, "size_id": 11, "quantity": 1},
        # sneaker 20
        {"sneaker_id": 20, "size_id": 6, "quantity": 12},
        {"sneaker_id": 20, "size_id": 7, "quantity": 9},
        {"sneaker_id": 20, "size_id": 8, "quantity": 6},
        {"sneaker_id": 20, "size_id": 9, "quantity": 3},
        # sneaker 21
        {"sneaker_id": 21, "size_id": 5, "quantity": 10},
        {"sneaker_id": 21, "size_id": 6, "quantity": 7},
        {"sneaker_id": 21, "size_id": 7, "quantity": 4},
        {"sneaker_id": 21, "size_id": 8, "quantity": 2},
        # sneaker 22
        {"sneaker_id": 22, "size_id": 5, "quantity": 8},
        {"sneaker_id": 22, "size_id": 6, "quantity": 6},
        {"sneaker_id": 22, "size_id": 7, "quantity": 4},
        {"sneaker_id": 22, "size_id": 8, "quantity": 1},
        # sneaker 23
        {"sneaker_id": 23, "size_id": 6, "quantity": 5},
        {"sneaker_id": 23, "size_id": 7, "quantity": 3},
        {"sneaker_id": 23, "size_id": 8, "quantity": 2},
        {"sneaker_id": 23, "size_id": 9, "quantity": 1},
        # sneaker 24
        {"sneaker_id": 24, "size_id": 6, "quantity": 14},
        {"sneaker_id": 24, "size_id": 7, "quantity": 10},
        {"sneaker_id": 24, "size_id": 8, "quantity": 6},
        {"sneaker_id": 24, "size_id": 9, "quantity": 3},
        # sneaker 25
        {"sneaker_id": 25, "size_id": 6, "quantity": 9},
        {"sneaker_id": 25, "size_id": 7, "quantity": 6},
        {"sneaker_id": 25, "size_id": 8, "quantity": 4},
        {"sneaker_id": 25, "size_id": 9, "quantity": 2},
        # sneaker 26
        {"sneaker_id": 26, "size_id": 6, "quantity": 11},
        {"sneaker_id": 26, "size_id": 7, "quantity": 8},
        {"sneaker_id": 26, "size_id": 8, "quantity": 5},
        {"sneaker_id": 26, "size_id": 9, "quantity": 2},
        # sneaker 27
        {"sneaker_id": 27, "size_id": 6, "quantity": 7},
        {"sneaker_id": 27, "size_id": 7, "quantity": 5},
        {"sneaker_id": 27, "size_id": 8, "quantity": 3},
        {"sneaker_id": 27, "size_id": 9, "quantity": 1},
        # sneaker 28
        {"sneaker_id": 28, "size_id": 8, "quantity": 10},
        {"sneaker_id": 28, "size_id": 9, "quantity": 7},
        {"sneaker_id": 28, "size_id": 10, "quantity": 4},
        {"sneaker_id": 28, "size_id": 11, "quantity": 2},
        # sneaker 29
        {"sneaker_id": 29, "size_id": 6, "quantity": 13},
        {"sneaker_id": 29, "size_id": 7, "quantity": 9},
        {"sneaker_id": 29, "size_id": 8, "quantity": 5},
        {"sneaker_id": 29, "size_id": 9, "quantity": 2},
        # sneaker 30
        {"sneaker_id": 30, "size_id": 6, "quantity": 8},
        {"sneaker_id": 30, "size_id": 7, "quantity": 6},
        {"sneaker_id": 30, "size_id": 8, "quantity": 4},
        {"sneaker_id": 30, "size_id": 9, "quantity": 2},
        # 31 Air Force 1 Low
        {"sneaker_id": 31, "size_id": 6, "quantity": 12},
        {"sneaker_id": 31, "size_id": 7, "quantity": 9},
        {"sneaker_id": 31, "size_id": 8, "quantity": 6},
        {"sneaker_id": 31, "size_id": 9, "quantity": 3},
        # 32 Dunk Low Retro
        {"sneaker_id": 32, "size_id": 6, "quantity": 10},
        {"sneaker_id": 32, "size_id": 7, "quantity": 8},
        {"sneaker_id": 32, "size_id": 8, "quantity": 5},
        {"sneaker_id": 32, "size_id": 9, "quantity": 2},
        # 33 Jordan 4 Retro
        {"sneaker_id": 33, "size_id": 7, "quantity": 7},
        {"sneaker_id": 33, "size_id": 8, "quantity": 5},
        {"sneaker_id": 33, "size_id": 9, "quantity": 3},
        {"sneaker_id": 33, "size_id": 10, "quantity": 1},
        # 34 Jordan 11 Concord
        {"sneaker_id": 34, "size_id": 6, "quantity": 6},
        {"sneaker_id": 34, "size_id": 7, "quantity": 4},
        {"sneaker_id": 34, "size_id": 8, "quantity": 3},
        {"sneaker_id": 34, "size_id": 9, "quantity": 1},
        # 35 Jordan 5 Retro
        {"sneaker_id": 35, "size_id": 7, "quantity": 8},
        {"sneaker_id": 35, "size_id": 8, "quantity": 6},
        {"sneaker_id": 35, "size_id": 9, "quantity": 4},
        {"sneaker_id": 35, "size_id": 10, "quantity": 2},
        # 36 Jordan 6 Retro
        {"sneaker_id": 36, "size_id": 7, "quantity": 6},
        {"sneaker_id": 36, "size_id": 8, "quantity": 5},
        {"sneaker_id": 36, "size_id": 9, "quantity": 3},
        {"sneaker_id": 36, "size_id": 10, "quantity": 1},
        # 37 Jordan 7 Retro
        {"sneaker_id": 37, "size_id": 6, "quantity": 7},
        {"sneaker_id": 37, "size_id": 7, "quantity": 5},
        {"sneaker_id": 37, "size_id": 8, "quantity": 3},
        {"sneaker_id": 37, "size_id": 9, "quantity": 1},
        # 38 Air Force 1 High
        {"sneaker_id": 38, "size_id": 6, "quantity": 11},
        {"sneaker_id": 38, "size_id": 7, "quantity": 8},
        {"sneaker_id": 38, "size_id": 8, "quantity": 5},
        {"sneaker_id": 38, "size_id": 9, "quantity": 2},
        # 39 Dunk High Premium
        {"sneaker_id": 39, "size_id": 6, "quantity": 9},
        {"sneaker_id": 39, "size_id": 7, "quantity": 7},
        {"sneaker_id": 39, "size_id": 8, "quantity": 4},
        {"sneaker_id": 39, "size_id": 9, "quantity": 2},
        # 40 Air Force 1 Shadow
        {"sneaker_id": 40, "size_id": 5, "quantity": 8},
        {"sneaker_id": 40, "size_id": 6, "quantity": 6},
        {"sneaker_id": 40, "size_id": 7, "quantity": 4},
        {"sneaker_id": 40, "size_id": 8, "quantity": 2},
        # 41 Superstar Classic
        {"sneaker_id": 41, "size_id": 6, "quantity": 14},
        {"sneaker_id": 41, "size_id": 7, "quantity": 10},
        {"sneaker_id": 41, "size_id": 8, "quantity": 6},
        {"sneaker_id": 41, "size_id": 9, "quantity": 3},
        # 42 Spezial OG
        {"sneaker_id": 42, "size_id": 6, "quantity": 9},
        {"sneaker_id": 42, "size_id": 7, "quantity": 7},
        {"sneaker_id": 42, "size_id": 8, "quantity": 5},
        {"sneaker_id": 42, "size_id": 9, "quantity": 2},
        # 43 Forum Low
        {"sneaker_id": 43, "size_id": 6, "quantity": 12},
        {"sneaker_id": 43, "size_id": 7, "quantity": 9},
        {"sneaker_id": 43, "size_id": 8, "quantity": 6},
        {"sneaker_id": 43, "size_id": 9, "quantity": 3},
        # 44 Yeezy Runner (inspired)
        {"sneaker_id": 44, "size_id": 6, "quantity": 8},
        {"sneaker_id": 44, "size_id": 7, "quantity": 6},
        {"sneaker_id": 44, "size_id": 8, "quantity": 4},
        {"sneaker_id": 44, "size_id": 9, "quantity": 1},
        # 45 Campus 80s
        {"sneaker_id": 45, "size_id": 6, "quantity": 11},
        {"sneaker_id": 45, "size_id": 7, "quantity": 8},
        {"sneaker_id": 45, "size_id": 8, "quantity": 5},
        {"sneaker_id": 45, "size_id": 9, "quantity": 2},
        # 46 Gazelle Vintage
        {"sneaker_id": 46, "size_id": 6, "quantity": 10},
        {"sneaker_id": 46, "size_id": 7, "quantity": 7},
        {"sneaker_id": 46, "size_id": 8, "quantity": 5},
        {"sneaker_id": 46, "size_id": 9, "quantity": 2},
        # 47 Stan Smith Premium
        {"sneaker_id": 47, "size_id": 6, "quantity": 13},
        {"sneaker_id": 47, "size_id": 7, "quantity": 10},
        {"sneaker_id": 47, "size_id": 8, "quantity": 7},
        {"sneaker_id": 47, "size_id": 9, "quantity": 3},
        # 48 Superstar Bold
        {"sneaker_id": 48, "size_id": 6, "quantity": 8},
        {"sneaker_id": 48, "size_id": 7, "quantity": 6},
        {"sneaker_id": 48, "size_id": 8, "quantity": 4},
        {"sneaker_id": 48, "size_id": 9, "quantity": 1},
        # 49 Dame Retro (inspired)
        {"sneaker_id": 49, "size_id": 6, "quantity": 9},
        {"sneaker_id": 49, "size_id": 7, "quantity": 7},
        {"sneaker_id": 49, "size_id": 8, "quantity": 5},
        {"sneaker_id": 49, "size_id": 9, "quantity": 2},
        # 50 Spezial Low
        {"sneaker_id": 50, "size_id": 6, "quantity": 11},
        {"sneaker_id": 50, "size_id": 7, "quantity": 8},
        {"sneaker_id": 50, "size_id": 8, "quantity": 5},
        {"sneaker_id": 50, "size_id": 9, "quantity": 2},
        # 51 Air Force 1 Utility
        {"sneaker_id": 51, "size_id": 6, "quantity": 10},
        {"sneaker_id": 51, "size_id": 7, "quantity": 8},
        {"sneaker_id": 51, "size_id": 8, "quantity": 5},
        {"sneaker_id": 51, "size_id": 9, "quantity": 2},
        # 52 Dunk SB Pro
        {"sneaker_id": 52, "size_id": 6, "quantity": 9},
        {"sneaker_id": 52, "size_id": 7, "quantity": 7},
        {"sneaker_id": 52, "size_id": 8, "quantity": 4},
        {"sneaker_id": 52, "size_id": 9, "quantity": 2},
        # 53 Jordan 4 Retro SE
        {"sneaker_id": 53, "size_id": 7, "quantity": 6},
        {"sneaker_id": 53, "size_id": 8, "quantity": 4},
        {"sneaker_id": 53, "size_id": 9, "quantity": 3},
        {"sneaker_id": 53, "size_id": 10, "quantity": 1},
        # 54 Jordan 5 Off-White (inspired)
        {"sneaker_id": 54, "size_id": 7, "quantity": 5},
        {"sneaker_id": 54, "size_id": 8, "quantity": 4},
        {"sneaker_id": 54, "size_id": 9, "quantity": 2},
        {"sneaker_id": 54, "size_id": 10, "quantity": 1},
        # 55 Superstar Platform
        {"sneaker_id": 55, "size_id": 6, "quantity": 8},
        {"sneaker_id": 55, "size_id": 7, "quantity": 6},
        {"sneaker_id": 55, "size_id": 8, "quantity": 4},
        {"sneaker_id": 55, "size_id": 9, "quantity": 2},
        # 56 Dunk Low Premium Pack
        {"sneaker_id": 56, "size_id": 6, "quantity": 7},
        {"sneaker_id": 56, "size_id": 7, "quantity": 5},
        {"sneaker_id": 56, "size_id": 8, "quantity": 3},
        {"sneaker_id": 56, "size_id": 9, "quantity": 1},
        # 57 Jordan 11 Retro Low
        {"sneaker_id": 57, "size_id": 6, "quantity": 6},
        {"sneaker_id": 57, "size_id": 7, "quantity": 4},
        {"sneaker_id": 57, "size_id": 8, "quantity": 3},
        {"sneaker_id": 57, "size_id": 9, "quantity": 1},
        # 58 Air Force 1 Pixel
        {"sneaker_id": 58, "size_id": 6, "quantity": 10},
        {"sneaker_id": 58, "size_id": 7, "quantity": 8},
        {"sneaker_id": 58, "size_id": 8, "quantity": 5},
        {"sneaker_id": 58, "size_id": 9, "quantity": 2},
        # 59 Superstar Vintage
        {"sneaker_id": 59, "size_id": 6, "quantity": 9},
        {"sneaker_id": 59, "size_id": 7, "quantity": 7},
        {"sneaker_id": 59, "size_id": 8, "quantity": 5},
        {"sneaker_id": 59, "size_id": 9, "quantity": 2},
        # 60 Dunk Low City Pack
        {"sneaker_id": 60, "size_id": 6, "quantity": 11},
        {"sneaker_id": 60, "size_id": 7, "quantity": 8},
        {"sneaker_id": 60, "size_id": 8, "quantity": 5},
        {"sneaker_id": 60, "size_id": 9, "quantity": 3},
        # 61
        {"sneaker_id": 61, "size_id": 6, "quantity": 14},
        {"sneaker_id": 61, "size_id": 7, "quantity": 10},
        {"sneaker_id": 61, "size_id": 8, "quantity": 7},
        {"sneaker_id": 61, "size_id": 9, "quantity": 3},
        # 62
        {"sneaker_id": 62, "size_id": 6, "quantity": 12},
        {"sneaker_id": 62, "size_id": 7, "quantity": 9},
        {"sneaker_id": 62, "size_id": 8, "quantity": 5},
        {"sneaker_id": 62, "size_id": 9, "quantity": 2},
        # 63
        {"sneaker_id": 63, "size_id": 7, "quantity": 8},
        {"sneaker_id": 63, "size_id": 8, "quantity": 6},
        {"sneaker_id": 63, "size_id": 9, "quantity": 4},
        {"sneaker_id": 63, "size_id": 10, "quantity": 1},
        # 64
        {"sneaker_id": 64, "size_id": 6, "quantity": 6},
        {"sneaker_id": 64, "size_id": 7, "quantity": 4},
        {"sneaker_id": 64, "size_id": 8, "quantity": 3},
        {"sneaker_id": 64, "size_id": 9, "quantity": 1},
        # 65
        {"sneaker_id": 65, "size_id": 7, "quantity": 9},
        {"sneaker_id": 65, "size_id": 8, "quantity": 6},
        {"sneaker_id": 65, "size_id": 9, "quantity": 4},
        {"sneaker_id": 65, "size_id": 10, "quantity": 2},
        # 66
        {"sneaker_id": 66, "size_id": 6, "quantity": 15},
        {"sneaker_id": 66, "size_id": 7, "quantity": 11},
        {"sneaker_id": 66, "size_id": 8, "quantity": 8},
        {"sneaker_id": 66, "size_id": 9, "quantity": 4},
        # 67
        {"sneaker_id": 67, "size_id": 6, "quantity": 10},
        {"sneaker_id": 67, "size_id": 7, "quantity": 8},
        {"sneaker_id": 67, "size_id": 8, "quantity": 5},
        {"sneaker_id": 67, "size_id": 9, "quantity": 2},
        # 68
        {"sneaker_id": 68, "size_id": 7, "quantity": 7},
        {"sneaker_id": 68, "size_id": 8, "quantity": 5},
        {"sneaker_id": 68, "size_id": 9, "quantity": 3},
        {"sneaker_id": 68, "size_id": 10, "quantity": 1},
        # 69
        {"sneaker_id": 69, "size_id": 6, "quantity": 9},
        {"sneaker_id": 69, "size_id": 7, "quantity": 7},
        {"sneaker_id": 69, "size_id": 8, "quantity": 5},
        {"sneaker_id": 69, "size_id": 9, "quantity": 2},
        # 70
        {"sneaker_id": 70, "size_id": 6, "quantity": 11},
        {"sneaker_id": 70, "size_id": 7, "quantity": 9},
        {"sneaker_id": 70, "size_id": 8, "quantity": 6},
        {"sneaker_id": 70, "size_id": 9, "quantity": 3},
    ]

    stmt = insert(SneakerSizeAssociation).values(sneaker_sizes)
    await session.execute(stmt)
    await session.commit()
