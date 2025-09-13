# Deployment Guide

## Prerequisites
- Docker installed
- kubectl configured to connect to your cluster (for Kubernetes deployment)
- Access to a container registry (Docker Hub, ECR, GCR, etc.) (for Kubernetes deployment)

## Local Development

### Running with Streamlit
```bash
# Navigate to the application directory
cd text_similarity_app

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Running with Docker Locally
```bash
# Build the image (uses .dockerignore to exclude unnecessary files)
docker build -t text-similarity-app:latest .

# Run locally
docker run -p 8501:8501 text-similarity-app:latest
```

Access the application at: `http://localhost:8501`

## Production Deployment

### 1. Build and Push Docker Image
```bash
# Build the image (now optimized with .dockerignore)
docker build -t text-similarity-app:latest .

# Tag for your registry (replace with your registry URL)
docker tag text-similarity-app:latest YOUR_REGISTRY/text-similarity-app:latest

# Push to registry
docker push YOUR_REGISTRY/text-similarity-app:latest
```

### 2. Update Deployment Manifest (Kubernetes)
Update the image name in `k8s-deployment.yaml`:
```yaml
image: YOUR_REGISTRY/text-similarity-app:latest
```

### 3. Deploy to Kubernetes Cluster
```bash
# Apply the deployment
kubectl apply -f k8s-deployment.yaml

# Apply the service
kubectl apply -f k8s-service.yaml
```

### 4. Check Deployment Status
```bash
# Check pods
kubectl get pods -l app=text-similarity-app

# Check service
kubectl get service text-similarity-app-service

# Get external IP (for LoadBalancer)
kubectl get service text-similarity-app-service -o wide
```

### 5. Access the Application
Once the LoadBalancer assigns an external IP, access your app at:
`http://<EXTERNAL-IP>`

## Scaling
To scale the deployment:
```bash
kubectl scale deployment text-similarity-app --replicas=5
```

## Cleanup
To remove the deployment:
```bash
kubectl delete -f k8s-service.yaml
kubectl delete -f k8s-deployment.yaml
```