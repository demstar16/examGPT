CREATE TABLE customer_data (
    customer_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE conversation_data (
    conversation_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    conversation_name TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id)
);
CREATE TABLE chat_message_data (
    conversation_id INTEGER,
    message_number INTEGER NOT NULL,
    sender TEXT NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversation_data(conversation_id)
);
