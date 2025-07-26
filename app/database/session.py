from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "mysql+aiomysql://root@localhost/trtbot"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
