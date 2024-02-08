from typing import List, Optional

import pymysql

from models import Product, ProductPayload, UserInDB, User
from utils import get_password_hash


def connect():
    conn = pymysql.connect(host='localhost', user='root', password='', database='hillelfastapi')

    return conn


def get_products() -> List[Product]:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products_rows = cursor.fetchall()
    conn.close()

    products = []
    for product in products_rows:
        products.append(Product(id=product[0], name=product[1], price=product[2], is_18_plus=product[3]))

    return products


def create_product(product: ProductPayload):
    conn = connect()
    cursor = conn.cursor()
    result = cursor.execute(f'INSERT INTO products (name, price, is_18_plus) VALUES ("{product.name}", {product.price}, {product.is_18_plus})')
    print(result)
    conn.commit()
    conn.close()
    return product


def get_product_by_id(product_id: int) -> Product:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM products WHERE id={product_id}')
    product = cursor.fetchone()
    conn.close()

    return Product(id=product[0], name=product[1], price=product[2], is_18_plus=product[3])


def update_product(product_id: int, product: ProductPayload):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f'UPDATE products SET name="{product.name}", price={product.price}, is_18_plus={product.is_18_plus} WHERE id={product_id}')
    conn.commit()
    conn.close()


def delete_product(product_id: int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM products WHERE id={product_id}')
    conn.commit()
    conn.close()


def get_user(username: str) -> Optional[UserInDB]:
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT username, email, full_name, disabled, hashed_password FROM users WHERE username="{username}"')
    user_row = cursor.fetchone()
    conn.close()

    if user_row:
        return UserInDB(
            username=user_row[0],
            email=user_row[1],
            full_name=user_row[2],
            disabled=user_row[3],
            hashed_password=user_row[4]
        )
    else:
        return None


def create_user(user: User, password: str) -> UserInDB:
    password_hash = get_password_hash(password)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO users (username, email, full_name, disabled, hashed_password) VALUES ("{user.username}", "{user.email}", "{user.full_name}", {user.disabled}, "{password_hash}")')

    conn.commit()
    conn.close()

    user_in_db = UserInDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
        hashed_password=password_hash
    )

    return user_in_db


if __name__ == "__main__":
    user = User(username="admin", email="vitalii@vitalii.tech", full_name="Vitalii", disabled=False)
    password = "adminadmin"
    create_user(
        user, password
    )