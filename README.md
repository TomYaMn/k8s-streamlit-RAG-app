# Streamlit with Kubernetes

This project demonstrates how to deploy a **Streamlit** app to **Kubernetes** with **Qdrant** as the vector store.

## How to run:

### 1. Build and Push the Docker Image:
```bash
bash scripts/build_and_push.sh




## Running at local
docker-compose up --build

## Running at Kub
eksctl create cluster --name streamlit-cluster --region us-west-2 --nodegroup-name standard-workers --node-type t3.medium --nodes 3 --nodes-min 1 --nodes-max 4




1️⃣ Set Up AWS EKS Cluster
-You need an EKS cluster to run your application.

-A. Install AWS CLI & kubectl
-Ensure you have:
-AWS CLI → To interact with AWS
-kubectl → To interact with Kubernetes
-eksctl → To create and manage EKS clusters


# Install AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/


B. Create an EKS Cluster

# command
eksctl create cluster --name my-cluster --region us-east-1 --nodegroup-name my-nodes --nodes 2

-This creates an EKS cluster with 2 worker nodes.
-The region can be changed based on your AWS setup.

2️⃣ Configure kubectl to Use EKS Cluster
-Once the cluster is ready, update your kubectl config:


#commaned
aws eks update-kubeconfig --region us-east-1 --name my-cluster
-Verify that it’s working:

#commaned
kubectl get nodes
-This should show the worker nodes running.

3️⃣ Push Your Docker Images to AWS ECR
-AWS EKS does not pull from local Docker images. You need to push them to Amazon Elastic Container Registry (ECR).

-A. Create an ECR Repository
#command
aws ecr create-repository --repository-name k8s-streamlit-rag-app
-Copy the repository URI from the response.

-B. Authenticate Docker with ECR
#command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-ecr-repo-uri>

C. Build and Push Docker Images

# Build
docker build -t k8s-streamlit-rag-app ./src
docker build -t k8s-streamlit-rag-app-nginx ./nginx

# Tag
docker tag k8s-streamlit-rag-app <your-ecr-repo-uri>:latest
docker tag k8s-streamlit-rag-app-nginx <your-ecr-repo-uri>:latest

# Push
docker push <your-ecr-repo-uri>:latest

4️⃣ Deploy Kubernetes Manifests
-Modify your k8s YAML files to use ECR images instead of local ones.
-A. Update streamlit-deployment.yaml
-Edit k8s/deployments/streamlit-deployment.yaml to use the ECR image:

#command
containers:
  - name: streamlit
    image: <your-ecr-repo-uri>:latest  # Replace with your actual ECR image
    ports:
      - containerPort: 8501

-B. Update nginx-deployment.yaml
-Similarly, update k8s/deployments/nginx-deployment.yaml:

#command
containers:
  - name: nginx
    image: <your-ecr-repo-uri>:latest  # Replace with your actual ECR image
    ports:
      - containerPort: 80

5️⃣ Apply Manifests to EKS
-Deploy your app to EKS:

#command
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress/
-Verify if the pods are running:

#command
kubectl get pods

6️⃣ Expose Your Application with AWS Load Balancer
-To make your app accessible, use an AWS Load Balancer.

-A. Install AWS Load Balancer Controller

#command
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
-B. Modify ingress.yaml
-Ensure your k8s/ingress/ingress.yaml uses an AWS Load Balancer:

#command
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: streamlit-ingress
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
spec:
  rules:
    - host: my-app.example.com  # Replace with your domain
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80

-C. Deploy Ingress
#command
kubectl apply -f k8s/ingress/
-Check if it’s created:

#command
kubectl get ingress
-You should get an ALB URL, which you can use to access your app.

7️⃣ Test Your Deployment
-Get the Load Balancer URL:

#command
kubectl get ingress
-Visit the given URL in your browser.

🎯 Summary
✅ Set up AWS EKS
✅ Push Docker images to AWS ECR
✅ Deploy Kubernetes manifests to EKS
✅ Expose your application via AWS Load Balancer
✅ Access the application using the Load Balancer URL



docker compose down
docker compose up --build