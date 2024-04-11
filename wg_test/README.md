## Client-Server Application 

This application provides a simple way to manage items using a client-server architecture. The server is launched using the `manager.py` file in the `server` directory, and the client connects to the server using the file in the `client` directory.

### Installation and Running Instructions

1. Start the server by running the `manager.py` file in the `server` directory.
   
    ```
    python3 server/manager.py
    ```

2. Then run the client by executing the file in the `client` directory.

    ```
    python3 client/manager.py
    ```

### Available Client Commands

- `exit`: Terminate the client.
- `logout`: Return to the login step.
- `items`: Show available items.
- `my_items`: Show user data.
- `credits`: Show user credits.
- `buy item_name`: Buy one item from the items list.
- `sell item_name`: Sell one item from user resources.

### Example Usage

1. Start the server and client.
2. Type `items` to see the available items.
3. Execute `buy item_name` to purchase the selected item.
4. Check your items using `my_items`.
5. If needed, sell an item using `sell item_name`.


### Notes

- User authentication is required for purchasing and selling operations.



