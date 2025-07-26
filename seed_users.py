import asyncio
from datetime import datetime, timedelta
from app.database.models import User
from app.database.session import async_session


async def seed_users():
    async with async_session() as session:
        now = datetime.utcnow()
        users = [
            User(id=1, username="user1", referrals_count=5, joined_at=now - timedelta(days=1)),
            User(id=2, username="user2", referrals_count=8, joined_at=now - timedelta(days=3)),
            User(id=3, username="user3", referrals_count=3, joined_at=now - timedelta(days=10)),
            User(id=4, username="user4", referrals_count=0, joined_at=now),
        ]
        session.add_all(users)
        await session.commit()
        print("✅ База заполнена тестовыми пользователями.")

if __name__ == "__main__":
    asyncio.run(seed_users())
