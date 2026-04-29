# TechSalary-Microservices-BE

## Manual Deployment Instructions

1. **Build the Docker Images:**
   `docker build -t techsalary-salary ./src/salary-service`
   *(Repeat for other services)*

2. **Deploy to Kubernetes:**
   `kubectl apply -f k8s/data-namespace/`
   `kubectl apply -f k8s/app-namespace/`
   `kubectl apply -f k8s/ingress/`

3. **Verify Pods are Running:**
   `kubectl get pods -n app`
