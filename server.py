from unicodedata import category
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import List, Dict
from time import time
import uvicorn
from pymongo import MongoClient

class Review(BaseModel):
    username: str
    content: str
    img_urls: List[str] = ["Blank"]
    ranking: int

class Step(BaseModel):
    img_urls: List[str]
    content: str

class Ingre(BaseModel):
    category: str
    name: str
    Ngon_url: str

class Recipe(BaseModel):
    title: str
    reviews: Dict[str, Review]
    category: str
    est_cook_mins: int
    n0_likes: int
    n0_servings: int
    UserID: str
    rating: float
    n0_ratings: int
    img_urls: List[str] = ["Blank"]
    steps: Dict[str, Step]
    ingredients: List[Dict[str, Ingre]]

class RecipeQuery(BaseModel):
    title: str
    category: str = "unknown"


tags_metadata = [
    {
        "name": "health-check",
        "description": "check health"
    },
    {
        "name":"insert-one-recipe",
        "description":"insert 1 recipe into DB"
    },
    {
        "name":"get-recipe-by-title",
        "description": "query recipes using name, return list of 10 matches"
    },
    {
        "name":"insert-UGC-recipe",
        "description": "insert user's generated recipe into db"
    }
]

app = FastAPI(openapi_tags = tags_metadata)
mg_client = MongoClient(host="104.154.184.230", port=27017)

@app.get("/", tags=["check-status"],status_code=status.HTTP_200_OK)
async def check_status():
    return {"sup":"ite den"}

@app.post("/insert-one-recipe",tags=["insert-one-recipe"],status_code=status.HTTP_200_OK)
async def insert_one(recipe_data: Recipe):
    
    #TODOS: 
    # connect to MGDB 
    # parse and insert 1 recipe into MGDB 
    
    db = mg_client["TikookDBv2"]
    RcpCollection = db.Recipes
    insRes = RcpCollection.insert_one(recipe_data.dict())

    return {"InsertionResult":str(insRes.acknowledged)}

@app.post("/get-recipe-by-title",tags=["get-recipe-by-title"],status_code=status.HTTP_200_OK)
async def get_recipe_by_title(recipe_query: RecipeQuery):
    
    #TODOS: 
    # connect to MGDB 
    # closing code: client.close()

    db = mg_client["TikookDBv2"]
    RcpCollection = db.Recipes
    insRes = RcpCollection.find(recipe_query.dict())

    return {"InsertionResult":str(insRes.acknowledged)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8802)