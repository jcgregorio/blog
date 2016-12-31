default: out/prefixed.css js/b.min.js
	piccolo

out/prefixed.css: out/built.css
	./node_modules/.bin/cssmin out/built.css | ./node_modules/.bin/autoprefixer --output out/prefixed.css

out/built.css: css/b/base.css bower_components/google-code-prettify/src/prettify.css
	-mkdir out
	awk 'FNR==1{print ""}{print}' $^ > out/built.css

js/b.min.js: bower_components/google-code-prettify/src/prettify.js js/base.js
	awk 'FNR==1{print ""}{print}' $^ | ./node_modules/.bin/uglifyjs --compress --output $@ -

pub:
	piccolo
	./bin/pub
	./bin/hubping

deps:
	npm update
	./node_modules/.bin/bower update
	sudo apt install texlive-latex-recommended imagemagick

clean:
	find ./dst -name "*.html" | xargs rm

watch:
	./bin/waitforit.sh

serve:
	cd ./dst ; http-server

setup:
	go get -u github.com/jcgregorio/piccolo

server:
	go get -u github.com/jcgregorio/userve/go/userve
	go install -v hawx.me/code/riviera
	./build_release

