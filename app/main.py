from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Schema outline for each post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Storage of all posts
my_posts = [{"Title": "Favorite Animal", "Content": "Elephants", "Published": False, "id": 1}, {"Title": "Favorite Food", "Content": "Pizza", "id": 2}]

# Returns a post with a specified "id" if it exists in "my_posts"
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
# Return the index of a post with a specific "id" if it exists in "my_posts"
def find_index_of_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
        
# Gets message at root directory
@app.get("/")
def root():
    return {"Message": "Python API Development"}

# Get all the posts
@app.get("/posts")
def get_posts():
    return {"All Post Data": my_posts}

# Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)

    return {"New Post Data": post_dict}

# Get one specific post
@app.get("/posts/{id}")
def get_post(id: int):
    requested_post = find_post(id)
    if not requested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    return {"Requested Post Details": requested_post}

# Delete a specific post
@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    requested_index = find_index_of_post(id)
    if not requested_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found for deletion")
    
    my_posts.pop(requested_index)

    # Can't return data with delete requests
    return Response(status_code=status_code)

# Update a specific post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    requested_update_index = find_index_of_post(id)
    if requested_update_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found for updating")
    
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[requested_update_index] = post_dict

    return {"Updated Post Data": post_dict}