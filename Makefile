build:
	docker build -t my-docker-repo/streamlit-app:latest .

push:
	docker push my-docker-repo/streamlit-app:latest

deploy:
	kubectl apply -f k8s/deployments/streamlit-deployment.yaml
	kubectl apply -f k8s/services/streamlit-service.yaml
	kubectl apply -f k8s/ingress/ingress.yaml