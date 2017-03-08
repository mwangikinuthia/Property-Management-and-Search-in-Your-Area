
# locaton_indexing simplified

This app is used for managing rental properties.It makes it convinient for Tenants to be able to access your property online and make bookings.
This saves time to avoid future tenents from walking around estates to physicaly find places to rent.
Houses are uploaded by caretakers/managers.They must include at least two photos,contanct and location.
Future feutures such as us of googlemaps arent yet implimented.
This web-app is written in Python and Python popular web-framework Django.
Requirements:

    Python 2.7 or higher 
    Django 1.8 or higher 
    Mysql 5.5.4 or higher 
    Most preferably a Linux machine eg Ubuntu 14.04

run python manage.py makemigrations && migrate

log in to 127.0.0.1:8000/admin and create to groups of users:

    i)caretakers who have permissions to add remove delete plots and houses 
    ii)tenant who have permissions to book and comment

in searching our houses and plots will be using a third-party extension solr-apache with python binding haystack. 
Requirements:
    Java Runtime Enviroment version 1.7 or higher you can download it from http://www.oracle.com/technetwork/java/javase/downloads/index.html . 
    Solr version 4.10.4 or get it from http://archive.apache.org/dist/lucene/solr/ django-haystack pip install django-haystack==2.4.0

Unzip the downloaded file and go to the example directory within the Solr installation directory (that is, cd solr- 4.10.4/example/ ). This directory contains a ready to use Solr configuration. From this directory, run Solr with the built-in Jetty web server using the command:

    java -jar start.jar

create our app core in example/solr directory

location_indexing/

    data/ conf/ protwords.txt schema.xml solrconfig.xml stopwords.txt synonyms.txt lang/

        stopwords_en.txt

python manage.py build_solr_schema inputed in schema.xnl 
python manage.py rebuild_index index your models 
python manage.py update_index update after adding new items


