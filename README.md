# TechSalary-Microservices-BE

## Manual Deployment Instructions

1. **Build the Docker Images:**
   `docker build -t techsalary-identity ./src/identity-service`
   `docker build -t techsalary-salary ./src/salary-service`
   `docker build -t techsalary-vote ./src/vote-service`
   `docker build -t techsalary-search ./src/search-service`
   `docker build -t techsalary-stats ./src/stats-service`
   `docker build -t techsalary-bff ./src/bff-service`

3. **Deploy to Kubernetes:**
   `kubectl apply -f k8s/data-namespace/`
   `kubectl apply -f k8s/app-namespace/`
   `kubectl apply -f k8s/ingress/`

4. **Verify Pods are Running:**
   `kubectl get pods -n app`
