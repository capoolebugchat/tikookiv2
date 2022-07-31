from ctypes import Union
import http
from unicodedata import category
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Any, List, Dict, Union
from time import time
from bson.json_util import dumps, loads
from bson.objectid import ObjectId


from pymongo import MongoClient, ASCENDING, DESCENDING, errors
import uvicorn

class Review(BaseModel):
    username: str
    content: str
    img_urls: List[str] = ["Blank"]
    ranking: int

class Step(BaseModel):
    img_urls: List[Any]
    content: str

class Ingre(BaseModel):
    category: str
    name: str
    Ngon_url: str

class Recipe(BaseModel):
    title: str
    reviews: List[Union[Review, None]]
    category: str
    est_cook_mins: int
    n0_likes: int
    n0_servings: int
    user_id: str
    ratings: float
    n0_ratings: int
    img_urls: List[str]
    steps: List[Union[Step,None]]
    ingredients: List[Union[Ingre,None]]

class User(BaseModel):
    user_id: str
    name: str
    pfp_url: str
    n0_follows: int
    n0_followers: int
    n0_recipes: int

class TikiNgonItem(BaseModel):
    name: str
    img_url: str
    ratings: float
    n0_ratings: int
    in_stock: int


class RecipeQuery(BaseModel):
    title: str = "unknown"
    category: str = "unknown"


tags_metadata = [
    {
        "name": "get-all-recipes",
        "description": "get all recipes sorted by rating"
    },
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
        "name":"get-recipe-by-category",
        "description": "query recipes using category, return list of 10 matches"
    },
    {
        "name":"get-tikiNgon-by-ingredient-name",
        "description": "return data for a specified ingredient"
    },
    {
        "name":"list-all-categories",
        "description":"return list of all categories"
    },
    {
        "name":"get-recipe-by-category",
        "description":"return recipes belonging to a category"
    },
    {
        "name":"get-recipe-by-id",
        "description":"return recipe with given id"
    },

    # {
    #     "name":"insert-UGC-recipe",
    #     "description": "insert user's generated recipe into db"
    # }
]

app = FastAPI(openapi_tags = tags_metadata)
mg_client = MongoClient(host="104.154.184.230", port=27017)

try:
    mg_client = MongoClient(host="104.154.184.230", port=27017, username="tikook_admin", password="T!k00k", authSource="TikookDB", authMechanism="SCRAM-SHA-256")
    mg_client.server_info() # force connection on a request as the
                         # connect=True parameter of MongoClient seems
                         # to be useless here 
except errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print(err)

@app.get("/", tags=["check-status"],status_code=status.HTTP_200_OK)
async def check_status():
    return {"sup":"ite den"}

@app.get("/get-all-recipes",tags=['get-all-recipes'],status_code=status.HTTP_200_OK)
async def get_all_recipes():
    #TODOS: 
    # connect to MGDB 
    # find all recipes in DB and sort them by rating
    
    db = mg_client["TikookDB"]
    RcpCollection = db.recipes
    rcps_cursor = RcpCollection.find()
    rcps_data = []
    for rcp in rcps_cursor:
        rcp['_id'] = str(rcp['_id'])
        rcps_data.append(rcp)
    return {"recipes":rcps_data}
    
@app.get("/get-recipe-by-id",tags=["get-recipe-by-id"],status_code=status.HTTP_200_OK)
async def get_recipe_by_id(id: str=""):
    #TODOS: 
    # connect to MGDB 
    # find one recipe in DB corresponding to given id
    # category="món chiên"
    db = mg_client["TikookDB"]
    RcpCollection = db.recipes
    # rcps = list(RcpCollection.find({},{"_id":0}))
    obj_id = ObjectId(id)
    rcp_cursor = RcpCollection.find({"_id": obj_id})
    rcp_data = []
    for rcp in rcp_cursor:
        rcp['_id'] = str(rcp['_id'])
        rcp_data.append(rcp)
    # print(rcp_data[0]["category"])
    # print(category==rcp_data[0]["category"])
    return {"recipes":rcp_data}

@app.post("/insert-one-recipe",tags=["insert-one-recipe"],status_code=status.HTTP_200_OK)
async def insert_one_recipe(recipe_data: Recipe):
    
    #TODOS: 
    # connect to MGDB 
    # parse and insert 1 recipe into MGDB 
    
    db = mg_client["TikookDB"]
    RcpCollection = db.recipes
    insRes = RcpCollection.insert_one(recipe_data.dict())
    print(recipe_data)
    return {"InsertionResult":str(insRes.acknowledged)}

@app.post("/get-recipe-by-title",tags=["get-recipe-by-title"],status_code=status.HTTP_200_OK)
async def get_recipe_by_title(recipe_query: RecipeQuery):
    
    #TODOS: 
    # connect to MGDB 
    # closing code: client.close()

    db = mg_client["TikookDB"]
    RcpCollection = db.recipes

    if recipe_query.title != "unknown":
        cursors = RcpCollection.find({"title":recipe_query.title}, {"_id":0})
        return {"matching recipes": list(cursors)}
    else: 
        return {"Message": "Unknown recipe name"}

@app.get("/get-recipe-by-category",tags=["get-recipe-by-category"],status_code=status.HTTP_200_OK)
async def get_recipe_by_cate(category: str=""):
    #TODOS: 
    # connect to MGDB
    db = mg_client["TikookDB"]
    RcpCollection = db.recipes
    if category != "":
        category=category.replace('"','')
        print(category)
        rcp_cursor = RcpCollection.find({"category": category})
        rcp_data = []
        for rcp in rcp_cursor:
            rcp['_id'] = str(rcp['_id'])
            rcp_data.append(rcp)
        return {"recipes": rcp_data}
    else: 
        return {"Message": "Unknown recipe name"}

@app.get("/get-tikiNgon-by-ingredient-name", tags=["get-tikiNgon-by-ingredient-name"], status_code=status.HTTP_200_OK)
async def get_tikiNgon_item_by_ingredient_name(ingredient_name: str=""):
    #TODOS:
    # connect to MGDB
    # return tikiNgon item data corresponding to the ingredient name
    db = mg_client["TikookDB"]
    TikiNgonCollection = db.tikingon_item

    if ingredient_name != "":
        cursors = TikiNgonCollection.find({"name":ingredient_name}, {"_id":0})
        return {"Matching TikiNgon items": list(cursors)}
    else:
        return {"Message": "Couldn't find a tikiNgon item with the provided ingredient name"}

@app.get("/get-all-categories",tags=["list-all-categories"],status_code=status.HTTP_200_OK)
async def get_all_categories():
    #TODOS: 
    # connect to MGDB 
    # find all categories and return 'em
    
    db = mg_client["TikookDB"]
    RcpCollection = db.recipes
    rcps_cursor = RcpCollection.find()
    categories = []
    for rcp in rcps_cursor:
        # rcp['category'] = str(rcp['_id'])
        if rcp['category'] not in categories:
            categories.append(rcp['category'])
    return {"categories":categories}
