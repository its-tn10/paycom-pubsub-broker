DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    id SERIAL,
    email TEXT NOT NULL,
    publisher BOOLEAN NOT NULL,
    subscriber BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX email ON clients(email);


DROP TABLE IF EXISTS topics;
CREATE TABLE topics (
    id SERIAL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX name ON topics(name);


DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
    id SERIAL,
    topic_id INT NOT NULL,
    message TEXT NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT messages_ibfk_1 FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS read_messages;
CREATE TABLE read_messages (
    client_id INT NOT NULL,
    message_id INT NOT NULL,
    PRIMARY KEY (client_id, message_id),
    CONSTRAINT read_messages_ibfk_1 FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT read_messages_ibfk_2 FOREIGN KEY (message_id) REFERENCES messages (id) ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS subscriptions;
CREATE TABLE subscriptions (
    client_id INT NOT NULL,
    topic_id INT NOT NULL,
    PRIMARY KEY (client_id, topic_id),
    CONSTRAINT subscriptions_ibfk_1 FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT subscriptions_ibfk_2 FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE ON UPDATE CASCADE
);