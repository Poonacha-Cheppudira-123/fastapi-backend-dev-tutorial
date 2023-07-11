from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# Schema + Data Validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "Favorite Animal", "content": "I like monkeys!", "id": 1},
    {"title": "Favorite Food", "content": "I like pizza!", "id": 2},
]


def find_post(id):
    for my_post in my_posts:
        if my_post["id"] == id:
            return my_post


def find_post_index(id):
    for index, my_post in enumerate(my_posts):
        if my_post["id"] == id:
            return index


# CRUD Operations
@app.get("/")
def root():
    """Retreive data from root directory and return message."""
    return {"message": "Welcome to my API!"}


@app.get("/posts")
def get_posts():
    """Retreive all posts from my_posts."""
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """Create a new post and append."""
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    """Get one specified post."""
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    """Delete a specified post"""
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, new_post: Post):
    """Update a specifed post"""
    index = find_post_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = id
    my_posts[index] = new_post_dict
    return {"message": new_post_dict}
