default: build-deb

.PHONY: run
run: pypltagent-eth.py
	python3 ./pypltagent-eth.py


# See the rootless-builds.txt in dpkg-dev.
.PHONY: build-deb
build-deb:
	mkdir -p build/pypltagent/usr/bin
	cp pypltagent-eth.py build/pypltagent/usr/bin/pypltagent-eth
	chmod +x build/pypltagent/usr/bin/pypltagent-eth
	
	mkdir -p build/pypltagent/DEBIAN
	cp debian/control build/pypltagent/DEBIAN/
	cp debian/postinst build/pypltagent/DEBIAN/
	cp debian/prerm build/pypltagent/DEBIAN/
	
	mkdir -p build/pypltagent/lib/systemd/system
	cp debian/pypltagent.service build/pypltagent/lib/systemd/system/
	dpkg-deb --build --root-owner-group build/pypltagent
	mv build/pypltagent.deb pypltagent.noarch.deb
	rm -rf build

.PHONY: stub
stub:
