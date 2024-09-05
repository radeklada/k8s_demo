# Project Setup and Deployment Guide

## Prerequisites

Ensure the following tools are installed and properly configured on your system before proceeding:

- **Docker Desktop** (with Kubernetes enabled)
- **kubectl** (for interacting with your Kubernetes cluster)
- **Helm** (for managing Kubernetes applications)

**Optional but recommended:**
- **k9s** (for a better CLI experience when working with Kubernetes)

---

## Step 1: Create Required Kubernetes Namespaces

Namespaces help organize resources in your cluster. Run the following commands to create the necessary namespaces:

```bash
kubectl create namespace staging
kubectl create namespace jenkins
kubectl create namespace prometheus
kubectl create namespace grafana
```

---

## Step 2: Build the Application

Navigate to your application directory and build the Docker image:

```bash
docker build -t app:1.0 .
```

---

## Step 3: Deploy Services and Applications

Navigate to your main directory and deploy the required services and applications as follows:

1. **NGINX Ingress Controller** (to handle external access to your services):
    ```bash
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
    ```

2. **PostgreSQL**:
    ```bash
    kubectl apply -f postgresql.yaml
    ```

3. **Application**:
    ```bash
    kubectl apply -f app.yaml
    ```

4. **Jenkins PVC** (Persistent Volume for Jenkins):
    ```bash
    kubectl apply -f jenkins-pvc.yaml
    ```

5. **Jenkins**: 
    Add the Jenkins Helm repo and deploy Jenkins using Helm:
    ```bash
    helm repo add jenkins https://charts.jenkins.io
    helm install jenkins jenkins/jenkins --namespace jenkins -f jenkins-values.yaml
    ```

6. **Prometheus**: 
    Add the Prometheus Helm repo and deploy Prometheus using Helm:
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm install prometheus prometheus-community/prometheus -n prometheus -f prometheus-values.yaml
    ```

7. **Grafana**: 
    Add the Grafana Helm repo and deploy Grafana:
    ```bash
    helm repo add grafana https://grafana.github.io/helm-charts
    helm install grafana grafana/grafana -n grafana -f grafana-values.yaml
    ```

---

## Step 4: Exposing Applications

### Accessing the Application

The main application is accessible via the **NGINX Ingress Controller** on:

```
http://localhost
```

### Exposing Jenkins

Run the following command to forward Jenkins service to your local machine:

```bash
kubectl port-forward --namespace jenkins svc/jenkins 18080:8080
```

Access Jenkins at:  
```
http://localhost:18080
```

### Exposing Prometheus

Prometheus can be accessed locally by forwarding the following ports:

- Prometheus Server:
    ```bash
    kubectl port-forward --namespace prometheus svc/prometheus-server 9090:80
    ```
    Access Prometheus at:  
    ```
    http://localhost:9090
    ```

- Prometheus Alertmanager:
    ```bash
    kubectl port-forward --namespace prometheus svc/prometheus-alertmanager 9093:9093
    ```
    Access Alertmanager at:  
    ```
    http://localhost:9093
    ```

### Exposing Grafana

To access Grafana locally, forward the Grafana service port:

```bash
kubectl port-forward -n grafana svc/grafana 3000:3000
```

Access Grafana at:  
```
http://localhost:3000
```

---

## Step 5: Connecting Prometheus to Grafana

To visualize Prometheus metrics in Grafana, add the following Prometheus URL as a data source in Grafana:

```
http://prometheus-server.prometheus.svc.cluster.local:9090
```

You can import k8s dashboard from file k8s_dashboard.json
