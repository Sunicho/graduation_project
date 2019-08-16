# graduationp roject
A tool for novice writers of crime fiction

usage: like any other personal project management system, but with relationship extraction function after you edit your story summary. The website can visualise the characters relationship graph using force graph. You can interact with the graph. The graph will show related part on your highlight part. A tutorial video is contained in the home page.


Language: Python 3.6.xFramework: Flask 1.0.3

Database: SQLite

Dependent Packages: AllenNLP, SQLAlchemy, Flask


Html pages are the webpage named after their function

__init__.py: the startup

form.py: receiving users input information

models.py: model layer of the project

relation_extraction: relationship extraction function and link prediction method

site.db: our database
