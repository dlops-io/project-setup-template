# Infrastructure as Code with Pulumi

This directory contains Pulumi infrastructure definitions for deploying the MLOps project to Google Cloud Platform (GCP).

## What Gets Deployed

### Google Cloud Resources

1. **GKE Cluster**
   - Kubernetes cluster for running containerized services
   - Autoscaling node pool (1-5 nodes)
   - Machine type: e2-medium
   - Auto-repair and auto-upgrade enabled

2. **Cloud Storage Buckets**
   - Data bucket: For raw and processed data
   - Models bucket: For trained ML models
   - Artifacts bucket: For Vertex AI pipeline artifacts

3. **Service Accounts**
   - GKE service account with necessary permissions
   - Storage admin access
   - Vertex AI user access

4. **Container Registry**
   - For storing Docker images (GCR)

## Prerequisites

### Required Tools
- [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)
- Python 3.11+
- GCP project with billing enabled

### GCP APIs to Enable
```bash
gcloud services enable container.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Authentication
```bash
# Login to GCP
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Login to Pulumi (or use local backend)
pulumi login
```

## Setup

### 1. Install Dependencies
```bash
cd infrastructure
pip install -r requirements.txt
```

### 2. Initialize Pulumi Stack

Create a new stack (e.g., "dev", "staging", "prod"):
```bash
pulumi stack init dev
```

### 3. Configure GCP Project
```bash
pulumi config set gcp:project YOUR_GCP_PROJECT_ID
pulumi config set gcp:region us-central1
pulumi config set gcp:zone us-central1-a
```

## Deployment

### Preview Changes
```bash
pulumi preview
```

### Deploy Infrastructure
```bash
pulumi up
```

Review the proposed changes and confirm to deploy.

### View Outputs
```bash
pulumi stack output
```

Key outputs:
- `gke_cluster_name`: Name of the GKE cluster
- `gke_cluster_endpoint`: Cluster endpoint URL
- `data_bucket_name`: GCS bucket for data
- `models_bucket_name`: GCS bucket for models
- `kubeconfig`: Kubernetes configuration

### Get Kubeconfig
```bash
pulumi stack output kubeconfig > kubeconfig.yaml
export KUBECONFIG=kubeconfig.yaml
kubectl get nodes
```

## Managing Infrastructure

### Update Infrastructure
Modify `__main__.py` and run:
```bash
pulumi up
```

### Destroy Infrastructure
**Warning: This will delete all resources!**
```bash
pulumi destroy
```

### Switch Between Stacks
```bash
pulumi stack select dev
pulumi stack select prod
```

## Deploying Services to GKE

After infrastructure is deployed:

### 1. Build and Push Docker Images
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Build and tag images
docker build -t gcr.io/YOUR_PROJECT_ID/api-service:latest ./src/api-service
docker build -t gcr.io/YOUR_PROJECT_ID/data-collector:latest ./src/data-collector

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/api-service:latest
docker push gcr.io/YOUR_PROJECT_ID/data-collector:latest
```

### 2. Deploy to Kubernetes
Students should create Kubernetes manifests (deployments, services) or use Helm charts.

Example deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      containers:
      - name: api-service
        image: gcr.io/YOUR_PROJECT_ID/api-service:latest
        ports:
        - containerPort: 8000
```

Apply:
```bash
kubectl apply -f deployment.yaml
```

## Cost Optimization

### Development Environment
- Use preemptible nodes for cost savings
- Reduce node count to minimum
- Use smaller machine types

### Production Environment
- Enable cluster autoscaling
- Use committed use discounts
- Implement proper resource requests/limits

## Security Best Practices

1. **Service Accounts**
   - Use Workload Identity for GKE pods
   - Follow principle of least privilege
   - Rotate service account keys regularly

2. **Network Security**
   - Enable Private GKE clusters in production
   - Use VPC-native clusters
   - Configure firewall rules

3. **Secrets Management**
   - Use Kubernetes Secrets or Secret Manager
   - Never commit secrets to Git
   - Rotate secrets regularly

## Troubleshooting

### GKE Cluster Not Accessible
```bash
gcloud container clusters get-credentials CLUSTER_NAME --zone ZONE
```

### Permission Denied
Ensure your account has necessary IAM roles:
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/container.admin"
```

### Pulumi State Issues
```bash
pulumi stack export > stack-backup.json
pulumi stack import < stack-backup.json
```

## Additional Resources

- [Pulumi GCP Documentation](https://www.pulumi.com/registry/packages/gcp/)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

## Next Steps

Students should:
1. Deploy infrastructure to their GCP project
2. Build and push Docker images to GCR
3. Create Kubernetes manifests for each service
4. Deploy services to GKE
5. Set up CI/CD pipeline for automated deployments
