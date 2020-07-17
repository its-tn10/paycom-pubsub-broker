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


INSERT INTO clients (id, email, publisher, subscriber) VALUES
    (1, 'tientavu@tamu.edu', FALSE, TRUE),
    (2, 'tientavu@hotmail.com', FALSE, TRUE),
    (3, 'advising@cse.tamu.edu', TRUE, FALSE),
    (4, 'somebody@paycomonline.com', TRUE, FALSE),
    (5, 'shipment-tracking@amazon.com', TRUE, FALSE);

INSERT INTO topics (id, name) VALUES
    (1, 'TAMUCSCSE'),
    (2, 'PAYCOMONLINE'),
    (3, 'AMAZONDELIVERY');

INSERT INTO messages (id, topic_id, message) VALUES
    (1, 1, 'Force requests for classes are currently at a halt.'),
    (2, 3, 'Clean Code and The Phoenix Project have been shipped.'),
    (3, 2, 'The Virtual Summer Engagement Program has kicked off!'),
    (4, 1, 'A new, updated schedule for Fall 2020 classes is now up.'),
    (5, 2, 'We are now approaching the end of the SEP program!');

INSERT INTO subscriptions (client_id, topic_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 3);
