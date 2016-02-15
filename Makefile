CERTLOC=data/cert
.PHONY: all clean gen_ssl_cert

all: gen_ssl_cert

$(CERTLOC)/server.crt: 
	bash contrib/gen-ssl-certificate.sh

gen_ssl_cert: $(CERTLOC)/server.crt

clean:
	make -C contrib/embed/ clean
	find . -name "*.pyc" -exec rm '{}' \;
	rm -rf build/
	rm -rf data/cert
	rm -f .srl

clean_all: clean
	rm -rf data/
	rm -rf env/
	rm tuby.egg-info
