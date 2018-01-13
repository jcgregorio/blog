pub:
	./_bin/pub

edit:
	JEKYLL_ENV=production bundle exec jekyll serve --host 192.168.1.95 --incremental --limit_posts 2 --verbose --drafts

serve:
	JEKYLL_ENV=production bundle exec jekyll serve --host 192.168.1.95 --verbose

server:
	go install github.com/jcgregorio/userve/go/userve
	BYPASS_UPLOAD=1 ./build_release buildit
	gcloud compute scp /tmp/userve/userve.deb default@bitworking2:/home/default/userve.deb --zone=us-central1-b

