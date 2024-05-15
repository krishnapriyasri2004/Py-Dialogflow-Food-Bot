import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dinesh@2003",
    database="pandeyji_eatery"
)

# Function to call the MySQL stored procedure and insert an order item
async def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

# Function to insert a record into the order_tracking table
async def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    data = (order_id, status)
    cursor.execute(insert_query, data)

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

    print("Order tracking status inserted successfully!")


# Function to get the next order ID from the orders table
def get_next_order_id():
    cursor = cnx.cursor()

    # Getting the maximum order_id from the orders table
    cursor.execute("SELECT MAX(order_id) FROM orders")

    # Fetching the result
    result = cursor.fetchone()
    if result[0] is None:
        return 1
    else:
        return result[0] + 1

# Function to get the total price of an order
# Function to get the total price of an order using the MySQL function
async def get_total_order_price(order_id):
    try:
        cursor = cnx.cursor()

        # Execute the MySQL function to get the total price of the order
        query = "SELECT get_total_order_price(%s) AS total_price"
        cursor.execute(query, (order_id,))

        # Fetching the result
        result = cursor.fetchone()

        # Closing the cursor
        cursor.close()

        if result:
            total_price = result[0]
            return total_price
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error getting total order price: {err}")
        return None


# Function to get the order status from the order_tracking table
async def get_order_status(order_id):
    cursor = cnx.cursor()

    # Query to get the order status from the order_tracking table
    query = "SELECT status FROM order_tracking WHERE order_id = %s"

    # Executing the query
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    if result:
        return result[0]
    else:
        return None
