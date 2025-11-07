from fastapi import FastAPI, File, HTTPException,UploadFile,Form,Depends
from app.schemas import PostCreate
from app.db import Post,create_db_and_table,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(""),
    session:AsyncSession=Depends(get_async_session)
      
):
    post=Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(PostCreate)
    return post


@app.get("/feed")
async def get_feed(
    session=AsyncSession=Depends(get_async_session)
):
    result=await session.execute(select(Post).order_by(Post.created_at_desc()))
    