"""
Pulumi Infrastructure as Code for MLOps Project

This module defines the infrastructure for deploying the MLOps project to GCP:
- GKE cluster for container orchestration
- Container Registry for Docker images
- Cloud Storage buckets for data and models
- Vertex AI setup for ML workflows
- IAM service accounts and permissions
"""

import pulumi
import pulumi_gcp as gcp
from pulumi_kubernetes import Provider

# Get configuration
config = pulumi.Config()
project_name = pulumi.get_project()
stack_name = pulumi.get_stack()

# GCP Configuration
gcp_config = pulumi.Config("gcp")
gcp_project = gcp_config.require("project")
gcp_region = gcp_config.get("region") or "us-central1"
gcp_zone = gcp_config.get("zone") or "us-central1-a"

# ------------------------------------------------------------------------------
# GCS Buckets for Data Storage
# ------------------------------------------------------------------------------

# Data bucket for raw and processed data
data_bucket = gcp.storage.Bucket(
    "data-bucket",
    name=f"{project_name}-{stack_name}-data",
    location=gcp_region,
    force_destroy=False,
    uniform_bucket_level_access=True,
    versioning=gcp.storage.BucketVersioningArgs(
        enabled=True,
    ),
    lifecycle_rules=[
        gcp.storage.BucketLifecycleRuleArgs(
            action=gcp.storage.BucketLifecycleRuleActionArgs(type="Delete"),
            condition=gcp.storage.BucketLifecycleRuleConditionArgs(
                age=90,  # Delete after 90 days
            ),
        )
    ],
)

# Models bucket for trained models
models_bucket = gcp.storage.Bucket(
    "models-bucket",
    name=f"{project_name}-{stack_name}-models",
    location=gcp_region,
    force_destroy=False,
    uniform_bucket_level_access=True,
    versioning=gcp.storage.BucketVersioningArgs(
        enabled=True,
    ),
)

# Vertex AI artifacts bucket
artifacts_bucket = gcp.storage.Bucket(
    "artifacts-bucket",
    name=f"{project_name}-{stack_name}-artifacts",
    location=gcp_region,
    force_destroy=False,
    uniform_bucket_level_access=True,
)

# ------------------------------------------------------------------------------
# GKE Cluster
# ------------------------------------------------------------------------------

# GKE cluster for running containerized services
gke_cluster = gcp.container.Cluster(
    "gke-cluster",
    name=f"{project_name}-{stack_name}-cluster",
    location=gcp_zone,
    initial_node_count=1,
    min_master_version="latest",
    remove_default_node_pool=True,
    deletion_protection=False,  # Set to True in production
)

# Node pool for the cluster
node_pool = gcp.container.NodePool(
    "primary-node-pool",
    cluster=gke_cluster.name,
    location=gcp_zone,
    initial_node_count=2,
    autoscaling=gcp.container.NodePoolAutoscalingArgs(
        min_node_count=1,
        max_node_count=5,
    ),
    node_config=gcp.container.NodePoolNodeConfigArgs(
        machine_type="e2-medium",
        oauth_scopes=[
            "https://www.googleapis.com/auth/cloud-platform",
        ],
        disk_size_gb=50,
        disk_type="pd-standard",
    ),
    management=gcp.container.NodePoolManagementArgs(
        auto_repair=True,
        auto_upgrade=True,
    ),
)

# ------------------------------------------------------------------------------
# Service Accounts
# ------------------------------------------------------------------------------

# Service account for GKE workloads
gke_service_account = gcp.serviceaccount.Account(
    "gke-service-account",
    account_id=f"{project_name}-{stack_name}-gke-sa",
    display_name="GKE Service Account",
)

# Grant necessary permissions to the service account
# Storage permissions
storage_admin_binding = gcp.projects.IAMMember(
    "storage-admin",
    project=gcp_project,
    role="roles/storage.objectAdmin",
    member=gke_service_account.email.apply(lambda email: f"serviceAccount:{email}"),
)

# Vertex AI permissions
vertex_ai_binding = gcp.projects.IAMMember(
    "vertex-ai-user",
    project=gcp_project,
    role="roles/aiplatform.user",
    member=gke_service_account.email.apply(lambda email: f"serviceAccount:{email}"),
)

# ------------------------------------------------------------------------------
# Container Registry
# ------------------------------------------------------------------------------

# Enable Container Registry API (images stored in GCS)
# Note: GCR automatically creates a bucket named artifacts.<project-id>.appspot.com

# ------------------------------------------------------------------------------
# Kubernetes Provider
# ------------------------------------------------------------------------------

# Get cluster credentials
k8s_config = pulumi.Output.all(
    gke_cluster.name, gke_cluster.endpoint, gke_cluster.master_auth
).apply(
    lambda args: f"""apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {args[2].cluster_ca_certificate}
    server: https://{args[1]}
  name: {args[0]}
contexts:
- context:
    cluster: {args[0]}
    user: {args[0]}
  name: {args[0]}
current-context: {args[0]}
kind: Config
users:
- name: {args[0]}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gke-gcloud-auth-plugin
      installHint: Install gke-gcloud-auth-plugin for use with kubectl
      provideClusterInfo: true
"""
)

# Create Kubernetes provider
k8s_provider = Provider(
    "gke-k8s",
    kubeconfig=k8s_config,
)

# ------------------------------------------------------------------------------
# Exports
# ------------------------------------------------------------------------------

pulumi.export("gke_cluster_name", gke_cluster.name)
pulumi.export("gke_cluster_endpoint", gke_cluster.endpoint)
pulumi.export("data_bucket_name", data_bucket.name)
pulumi.export("models_bucket_name", models_bucket.name)
pulumi.export("artifacts_bucket_name", artifacts_bucket.name)
pulumi.export("gke_service_account_email", gke_service_account.email)

# Students can use these exports to deploy their services
pulumi.export("kubeconfig", k8s_config)
