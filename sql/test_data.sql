INSERT INTO Users VALUES
(1, "admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "administrator"),
(2, "user1", "0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90", "user"),
(3, "user2", "6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3", "user");

INSERT INTO Recipes VALUES
(1, "Recipe A", "10", "20", "Recipe A description", 1, 2),
(2, "Recipe B", "20", "20", "Recipe B description", 2, 2),
(3, "Recipe C", "30", "60", "Recipe C description", 4, 2),
(4, "Recipe D", "40", "60", "Recipe D description", 2, 2),
(5, "Recipe E", "40", "60", "Recipe E description", 2, 3),
(6, "Recipe F", "40", "60", "Recipe F description", 2, 3);


INSERT INTO Steps VALUES
(1,1,"Recipe A-1"),
(1,2,"Recipe A-2"),
(1,3,"Recipe A-3");

INSERT INTO Steps VALUES
(2,1,"Recipe B-1"),
(2,2,"Recipe B-2"),
(2,3,"Recipe B-3"),
(3,1,"Recipe C-1"),
(3,2,"Recipe C-2"),
(3,3,"Recipe C-3");

INSERT INTO Books VALUES(1, "Book X");

INSERT INTO Ingredients VALUES
(1, "Ing 1"),
(2, "Ing 2"),
(3, "Ing 3"),
(4, "Ing 4"),
(5, "Ing 5"),
(6, "Ing 6");

INSERT INTO Tags VALUES
("Tag 1"),
("Tag 2"),
("Tag 3");

INSERT INTO RecipeIngredients VALUES
(1, 1, 10, "grams"),
(1, 2, 20, "grams"),
(1, 3, 30, "grams"),
(2, 4, 10, "grams"),
(2, 5, 20, NULL);

INSERT INTO RecipeTags VALUES
(1,"Tag 1"),
(1,"Tag 2"),
(2,"Tag 1"),
(2,"Tag 2"),
(3,"Tag 1"),
(3,"Tag 2"),
(3,"Tag 3");

INSERT INTO BookRecipes VALUES
(1, 5),
(1, 6);

INSERT INTO BookTags VALUES
(1,"Tag 1"),
(1,"Tag 2");