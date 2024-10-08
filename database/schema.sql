DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS topic;
DROP TABLE IF EXISTS article_topic_assignment;
DROP TABLE IF EXISTS subscriber;
DROP TABLE IF EXISTS subscriber_topic_assignment;

CREATE TABLE source (
    source_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_name VARCHAR(250) NOT NULL,
    source_url VARCHAR(500) NOT NULL,
    source_image_url VARCHAR(500) NOT NULL,
    source_political_leaning VARCHAR(50) NOT NULL
);

CREATE TABLE article (
    article_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    article_title VARCHAR(500) NOT NULL,
    polarity_score FLOAT NOT NULL,
    source_id SMALLINT NOT NULL,
    date_published DATE NOT NULL,
    article_url VARCHAR(500) NOT NULL,
    FOREIGN KEY (source_id) REFERENCES source(source_id)
);

CREATE TABLE topic (
    topic_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    topic_name VARCHAR (150) NOT NULL
);

CREATE TABLE article_topic_assignment (
    article_topic_assignment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    topic_id SMALLINT NOT NULL,
    article_id BIGINT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id),
    FOREIGN KEY (article_id) REFERENCES article(article_id)
);

CREATE TABLE subscriber (
    subscriber_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subscriber_email VARCHAR(250) NOT NULL,
    subscriber_first_name VARCHAR (100) NOT NULL,
    subscriber_surname VARCHAR(100) NOT NULL
);

CREATE TABLE subscriber_topic_assignment (
    subscriber_topic_assignment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subscriber_id INT NOT NULL,
    topic_id SMALLINT NOT NULL,
    FOREIGN KEY (subscriber_id) REFERENCES subscriber(subscriber_id),
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);

INSERT INTO topic (topic_name) VALUES
("Immigration"),
("Justice System"),
("Diddy"),
("Supreme Court Decisions"),
("Religion"),
("Natural Disasters"),
("Hurricane Helene"),
("World News"),
("Climate Change"),
("China"),
("Education"),
("Woke activism"),
("Crime and law enforcement"),
("Guns"),
("Economics"),
("Recession"),
("Inflation"),
("Cost of Living"),
("Politics"),
("Donald Trump"),
("Kamala Harris"),
("Voting"),
("JD Vance"),
("Tim Walz"),
("War"),
("Israel-Gaza"),
("Russia-Ukraine"),
("Iran"),
("Lebanon"),
("Race relations"),
("LGBTQ+ issues"),
("Abortion");

INSERT INTO source (source_name, source_url, source_image_url, source_political_leaning) VALUES
("Fox News", "https://www.foxnews.com/", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Fox_News_Channel_logo.svg/1200px-Fox_News_Channel_logo.svg.png", "Right"),
("Democracy Now!", "https://www.democracynow.org/", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6MVq_iSYjCvMqfZHJNb8PIdCGkqZZwOnyEw&s", "Left");