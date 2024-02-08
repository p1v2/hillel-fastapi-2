from datetime import timedelta

from fastapi import FastAPI, HTTPException
from fastapi.openapi.models import Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError

from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, ALGORITHM
from db import get_products, create_product, get_product_by_id, update_product, delete_product, get_user
from models import Product, ProductPayload, User

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/products")
async def read_products_api(current_user: User = Depends(get_current_user)):
    products = get_products()

    return { "user": current_user, "products": products }


@app.post("/products", response_model=ProductPayload)
async def create_product_api(product_data: ProductPayload):
    create_product(product_data)
    return product_data


@app.get("/products/{product_id}", response_model=Product)
async def read_product_api(product_id: int):
    product = get_product_by_id(product_id)
    return product


@app.put("/products/{product_id}", response_model=ProductPayload)
async def update_product_api(product_id: int, product_data: ProductPayload):
    product = get_product_by_id(product_id)

    update_product(product_id, product)

    return product_data


@app.delete("/products/{product_id}")
async def delete_product_api(product_id: int):
    delete_product(product_id)

    return Response(status_code=204)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
