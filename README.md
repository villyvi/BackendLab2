## Laboratorna 2
# Pylypchuk Vicky IO-32

## How my postman cOlLeCtIoN works:
1. User
   - post user (has body, JSON)
   - get user by user_id
   - delete user by user_id
   - and the last one is get users
2. Category
   - post category (toje has JSON)
   - get category 
   - delete category by id
3. Record
   - post record ( has JSON)
   - get record by id
   - delete record by id
   - get record but with both id (/record?user_id=1&category_id=1)

## Json that is used:
# for user
{
	"name": "Vicky"
}

# for category:
{
    "name": "Піпі пупу"
}

# for record:
{
    "user_id": 2,
    "category_id": 2,
    "amount": 13
}

## Усі посилання:
  - https://villyvi-5088406.postman.co/workspace/Viktoria-Pylypchuk's-Workspace~9489ffb2-66fe-4ca6-8186-1b84958f75a3/collection/49071994-21411135-56a3-491d-bdef-d416958a0d9a?action=share&creator=49071994 (Постман)
  
## lab3

Варіант визначається за остачею від ділення номера моєї групи на 3.
Моя група: ІО-32
Номер групи  32
Розрахунок: 32 % 3 = 2
Остача дорівнює 2

Цей проєкт реалізує REST API на Flask із використанням ORM (SQLAlchemy) для роботи з базою даних PostgreSQL.
Додатковий функціонал за варіантом №2 — створення користувацьких категорій витрат, що прив’язуються до конкретного користувача.

# Requirements
type .\requirements.txt
(кщо помилка з кодування)

# посилання:
