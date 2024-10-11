DROP TABLE IF EXISTS article_topic_assignment;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS topic;
DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS subscriber;

CREATE TABLE source (
    source_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_name VARCHAR(250) NOT NULL UNIQUE,
    source_url VARCHAR(500) NOT NULL UNIQUE,
    source_image_url VARCHAR(500) NOT NULL UNIQUE,
    source_political_leaning VARCHAR(50) NOT NULL
);

CREATE TABLE article (
    article_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    article_title VARCHAR(500) NOT NULL,
    article_content TEXT NOT NULL,
    title_polarity_score FLOAT NOT NULL,
    content_polarity_score FLOAT NOT NULL,
    source_id SMALLINT NOT NULL,
    date_published DATE NOT NULL,
    article_url VARCHAR(500) NOT NULL UNIQUE,
    FOREIGN KEY (source_id) REFERENCES source(source_id),
    UNIQUE (article_title, source_id, date_published)
);

CREATE TABLE topic (
    topic_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    topic_name VARCHAR (150) NOT NULL UNIQUE
);

CREATE TABLE article_topic_assignment (
    article_topic_assignment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    topic_id SMALLINT NOT NULL,
    article_id BIGINT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id),
    FOREIGN KEY (article_id) REFERENCES article(article_id),
    UNIQUE (topic_id, article_id)
);

CREATE TABLE subscriber (
    subscriber_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subscriber_email VARCHAR(250) NOT NULL UNIQUE,
    subscriber_first_name VARCHAR (100) NOT NULL,
    subscriber_surname VARCHAR(100) NOT NULL,
    daily BOOLEAN,
    weekly BOOLEAN
);

INSERT INTO topic (topic_name) VALUES
('Donald Trump'),
('Kamala Harris'),
('2024 Presidential Election'),
('Climate Change'),
('Natural Disaster'),
('Abortion'),
('Crime and Law Enforcement'),
('Guns'),
('Israel-Palestine');

INSERT INTO source (source_name, source_url, source_image_url, source_political_leaning) VALUES
('Fox News', 'https://www.foxnews.com/', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Fox_News_Channel_logo.svg/1200px-Fox_News_Channel_logo.svg.png', 'Right'),
('Democracy Now!', 'https://www.democracynow.org/', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6MVq_iSYjCvMqfZHJNb8PIdCGkqZZwOnyEw&s', 'Left');