import requests

def test_product_create():
    response = requests.post(
        "http://localhost:8000/products",
        json={"name": "Fanta", "price": 50, "is_18_plus": False},
    )
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    test_product_create()
