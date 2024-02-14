<h1>Booking RESTful API</h1>
<h3>Docker:</h3>
<p>
Container erstellen:
docker build -t booking-api:latest .

Container für den Cloud Server erstellen:
docker buildx build --platform linux/amd64 -t booking-api:latest .

Container taggen:
docker tag booking-api:latest twoaace/booking-api:latest

Container pushen:
docker push booking-api:latest

Container ausführen auf der lokalen Maschine mit workingdir:
docker run -d -p 8000:8000 -w /app -v "$(pwd):/app" booking-api:latest
</p>

<h3>Schema:</h3>
<p>
Validieren und Umwandeln von JSON in Python Objekt und umgekehrt.

Um unendliches nesting zu vermeiden, wird ein PlainSchema erstellt mit den Grundattributen.
Dann ein Schema welches von PlainSchema erbt mit den nested Attributen.
</p>

<h3>Models:</h3>
<p>
Datenbankstruktur mit SQLAlchemy
</p>



<h3>Notizen:</h3>
<p>
sudo docker exec -it mariadbdocker mariadb --user root -pPasswort<br>
CREATE DATABASE deine_datenbank;<br>
CREATE USER 'dein_benutzer'@'%' IDENTIFIED BY 'dein_passwort';<br>
GRANT ALL PRIVILEGES ON deine_datenbank.* TO 'dein_benutzer'@'%';<br>
FLUSH PRIVILEGES;
</p>
