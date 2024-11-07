# Импортируем необходимые модули из FastAPI и библиотеки random
from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
import random

# Создаем экземпляр FastAPI для настройки API
app = FastAPI()

# Пример словаря для хранения информации о товарах
# Здесь каждый товар представлен ID, именем и ценой
products = {
    1: {"name": "Product 1", "price": 100.0},
    2: {"name": "Product 2", "price": 200.0},
}

# Определяем endpoint для получения цены товара с применением скидки
@app.get("/product/{product_id}/price")
async def get_discounted_price(
    product_id: int = Path(..., description="ID товара"),  # Параметр пути, указывающий на ID товара
    discount_percentage: float = Query(None, ge=0, le=100, description="Процент скидки")  # Процент скидки как Query-параметр
):
    # Проверяем, существует ли товар с данным ID
    product = products.get(product_id)
    if not product:
        # Если товар не найден, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="Товар не найден")

    # Получаем исходную цену товара
    price = product["price"]

    # Если процент скидки указан, применяем его к цене
    if discount_percentage is not None:
        # Рассчитываем цену со скидкой
        discounted_price = price * (1 - discount_percentage / 100)
        return {
            "product_id": product_id,
            "original_price": price,
            "discount_percentage": discount_percentage,
            "discounted_price": discounted_price
        }

    # Если скидка не указана, возвращаем исходную цену товара
    return {"product_id": product_id, "name": product["name"], "price": price}

# Определяем endpoint для получения всех продуктов с случайной скидкой
@app.get("/products")
async def get_all_products():
    # Создаем новый словарь для хранения информации о товарах с примененной случайной скидкой
    products_with_random_discounts = {}
    # Проходим по каждому товару из словаря products
    for product_id, product in products.items():
        # Генерируем случайный процент скидки от 1 до 100
        random_discount = random.randint(1, 100)
        # Рассчитываем цену со случайной скидкой
        discounted_price = product["price"] * (1 - random_discount / 100)
        # Добавляем информацию о товаре и примененной скидке в новый словарь
        products_with_random_discounts[product_id] = {
            "name": product["name"],
            "original_price": product["price"],
            "random_discount_percentage": random_discount,
            "discounted_price": discounted_price
        }
    # Возвращаем словарь с товарами и их ценами со случайными скидками
    return products_with_random_discounts

# Если этот файл запускается как основной, запускаем приложение FastAPI с помощью Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
