
setup: GeoLite2-City.mmdb

pip-requirements:
	< requirements.txt | xargs pip3 install -U

clean:
	rm -rf GeoLite2*

GeoLite2-City.mmdb:
	wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz
	tar -xvf GeoLite2-City.tar.gz
	mv GeoLite2-City*/GeoLite2-City.mmdb GeoLite2-City.mmdb 
	echo "==========\nGeoLite2 Database License\n==========\n" >> LICENSE.txt
	cat GeoLite2-City*/LICENSE.txt >> LICENSE.txt
	rm -rf GeoLite2-City_*
	rm GeoLite2-City.tar.gz
	echo "\n==========\nPress Q to quit...\n==========" >> LICENSE.txt
	less LICENSE.txt
	rm LICENSE.txt