# python-blog-lab

To run the database: `docker run --name flask-blog-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=flask-db mysql:5.7`
To run the project: `python manage.py runserver`
To run SQLALCHEMY shell: `python manage.py shell`
To create the tables run the SQLALCHEMY shell, import the `db`, import the models, then run `db.create_all()`