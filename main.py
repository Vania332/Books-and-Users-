from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel,Field,EmailStr,ConfigDict

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "53e4ytetrчудес",
        "author": "oleg tinkoff"
    },
    {
        "id": 2,
        "title": "паша капец",
        "author": "roma ribin"
    },
]

@app.get("/books", tags=["книги"], summary=["получить все книги"])
async def read_books():
    return books

@app.get("/books/{book_id}", tags=["книги"], summary=["получить конкретную книгу"])
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="book is not found")

class User_new(BaseModel):
    id: int
    name: str
    bio:str = Field(max_length=10)
    age:int = Field(ge=0,le=100)

users = []

@app.get("/users",tags=["участники"])
async def get_all_users():
    return users

@app.post("/users/",tags= ["участники"])
async def create_user(user_new: User_new):
    users.append({
        "id": len(users) + 1,
        "name": user_new.name,
        "bio": user_new.bio,
        "age": user_new.age ,
    })
    return {"success": True,"msg": f"user {str(id)} has created"}
   
@app.get("/users/{user_id}",tags=["участники"]) 
async def get_user(user_id:int):
    for user in users:
        if user["id"]==user_id:
            return user
    raise HTTPException(status_code=404, detail="user is not found")

class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books/", tags=["книги"])
async def create_book(new_book: NewBook):  # Исправляем имя параметра
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,  # Исправляем обращение
        "author": new_book.author,  # Исправляем обращение
    })
    return {"success": True,}

class DelBook(BaseModel):
    id: int

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):  # Используем enumerate дает мне чтото типа 0 book1 ; 1 book2 ... для доступа к индексу
        if book["id"] == book_id:
            del books[i]  # Удаляем книгу по индексу
            return {"message": f"Book with id {book_id} has been deleted"}
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":##хз зачем оно надо
    uvicorn.run(app, host="localhost", port=8000)