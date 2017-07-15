pub:
	./_bin/pub

serve:
	JEKYLL_ENV=production bundle exec jekyll serve --host 192.168.1.95 --verbose

server:
	go get -u github.com/jcgregorio/userve/go/userve
	./build_release

