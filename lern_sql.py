from fastapi import FastAPI


from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column


app = FastAPI()


engine = create_async_engine('sqlite+aiosqlite:///users.db')

new_session = async_sessionmaker(engine,expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session
        
class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    second_name: Mapped[str]
    
@app.post("/setup_database/")   
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}
