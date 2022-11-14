pub:
	./_bin/pub

edit:
	hugo serve --verbose --disableFastRender

build_and_push_image:
	docker build -t jcgregorio/blog:latest ./image 
	docker push jcgregorio/blog:latest