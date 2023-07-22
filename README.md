## Little Lemon Restaurant API Documentation ##

**Description:**  
The Little Lemon Restaurant API provides developers with endpoints to interact with the restaurant's services programmatically. The API allows users to access menu items, place orders, manage bookings, view categories, and perform various other operations related to the restaurant's functionality. To access certain endpoints, developers need to obtain an authentication token using the `/api-token-auth/` endpoint.

**Base URL:**  
`https://api.littlelemonrestaurant.com`

**Authentication:**  
Authentication is required to access protected endpoints. Developers must include an authentication token in the request headers for endpoints that require authorization.

```http

Headers:
Authorization: Token YOUR_AUTH_TOKEN
```

**Error Handling:**  
Errors are returned with appropriate HTTP status codes and JSON-formatted error messages in the response body.  

```
json

{
  "error": {
    "code": 404,
    "message": "Resource not found"
  }
}
```

**Endpoints:**  

**Get All Menu Items**  

*Endpoint: /menu-items/*  
*Method: GET*  
*Description: Retrieve a list of all menu items available at Little Lemon Restaurant.*
*Response Example:*  

```
    json

[
  {
    "id": 1,
    "name": "Pasta Carbonara",
    "description": "Spaghetti with creamy egg sauce, pancetta, and parmesan.",
    "price": 12.99
  },
  {
    "id": 2,
    "name": "Grilled Salmon",
    "description": "Freshly grilled salmon with lemon and herbs.",
    "price": 16.50
  }
]
```

**Get Single Menu Item**

*Endpoint: /menu-items/<int:menuItem>*  
*Method: GET*  
*Description: Retrieve details of a specific menu item by its ID.*  
*Response Example:*  

```
json

{
  "id": 1,
  "name": "Pasta Carbonara",
  "description": "Spaghetti with creamy egg sauce, pancetta, and parmesan.",
  "price": 12.99
}
```

**Get All Categories**

*Endpoint: /category/*  
*Method: GET*  
*Description: Retrieve a list of all menu categories.*  
*Response Example:*  

```
json

[
  {
    "id": 1,
    "name": "Pasta"
  },
  {
    "id": 2,
    "name": "Seafood"
  }
]
```

**Place Order**

*Endpoint: /orders/*  
*Method: POST*  
*Description: Place a new order with the specified menu items and quantities.*  
*Request:*  

```
json

{
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    },
    {
      "menu_item_id": 2,
      "quantity": 1
    }
  ]
}
```
Response Example:

```
json

{
  "order_id": 1234,
  "total": 41.48
}
````

**Get Single Order**

*Endpoint: /orders/<int:orderId>*  
*Method: GET*  
*Description: Retrieve details of a specific order by its ID.*  
*Response Example:*  

```
json

{
  "order_id": 1234,
  "total": 41.48,
  "status": "Pending",
  "items": [
    {
      "menu_item_id": 1,
      "name": "Pasta Carbonara",
      "quantity": 2
    },
    {
      "menu_item_id": 2,
      "name": "Grilled Salmon",
      "quantity": 1
    }
  ]
}
```
* Customers can use this endpoint to update their orders via a `PUT` request   
* Managers can also use this endpoint to allocate orders to delivery crew members via a `PUT` request and delete orders via `DELETE` request   
* Delivery crew Members update the status of their allocated orders to either delivered or out for delivery via a `PATCH` request  
  
**Get All Bookings**

*Endpoint: /bookings/*  
*Method: GET*  
*Description: Retrieve a list of all bookings made at Little Lemon Restaurant.*  
*Response Example:*  

```
json

[
  {
    "booking_id": 1001,
    "name": "John Doe",
    "email": "john@example.com",
    "date_time": "2023-07-25 19:30",
    "party_size": 4
  },
  {
    "booking_id": 1002,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "date_time": "2023-08-02 18:00",
    "party_size": 2
  }
]
```

**Get Single Booking**

*Endpoint: /bookings/<int:bookingId>*  
*Method: GET*  
*Description: Retrieve details of a specific booking by its ID.*  
*Response Example:*    

```
json

{
  "booking_id": 1001,
  "name": "John Doe",
  "email": "john@example.com",
  "date_time": "2023-07-25 19:30",
  "party_size": 4
}
```

**Get Cart**

*Endpoint: /cart/menu-items/*  
*Method: GET*  
*Description: Retrieve the current contents of the user's cart.*  
*Response Example:*  

```
json

[
  {
    "menu_item_id": 1,
    "name": "Pasta Carbonara",
    "quantity": 2,
    "price": 25.98
  }
]
```

**Get All Managers**

*Endpoint: /groups/manager/users/*  
*Method: GET*  
*Description: Retrieve a list of all users with manager permissions.*  
*Response Example:*  

```
json

[
  {
    "user_id": 101,
    "username": "manager1"
  },
  {
    "user_id": 102,
    "username": "manager2"
  }
]
```

**Remove Manager**

*Endpoint: /groups/manager/users/<int:userId>*  
*Method: DELETE*  
*Description: Remove manager permissions from a user.*  
*Response Example:*  

```
json

{
  "message": "Manager permissions removed successfully."
}
```

**Get All Delivery Crew**

*Endpoint: /groups/delivery-crew/users/*  
*Method: GET*  
*Description: Retrieve a list of all users with delivery crew permissions.*  
*Response Example:*  

```
json

[
  {
    "user_id": 201,
    "username": "delivery1"
  },
  {
    "user_id": 202,
    "username": "delivery2"
  }
]
```

**Remove Delivery Crew**

*Endpoint: /groups/delivery-crew/users/<int:userId>*  
*Method: DELETE*  
*Description: Remove delivery crew permissions from a user.*  
*Response Example:*  

```
json

{
  "message": "Delivery crew permissions removed successfully."
}
```

**Add user to manager group**

*Method: POST*    
*Restriction: managers only*  
*Response: `{"Message": "User added successfully to manager group}`*  

**Add user to delivery crew group**

*Method: POST*  
*Restriction: managers only*  
*Response: `{"Message": "User added successfully to manager group}`*  
