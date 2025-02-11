terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-3"
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
      command     = "aws"
    }
  }
}

# Configure a VPC for the Cloud Platform
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.17.0"

  name            = "5gmeta-cloud-platform-vpc"
  cidr            = "10.0.0.0/16"
  azs             = ["eu-west-3a", "eu-west-3b", "eu-west-3c"]
  private_subnets = ["10.0.111.0/24", "10.0.121.0/24", "10.0.131.0/24"]
  public_subnets  = ["10.0.141.0/24", "10.0.151.0/24", "10.0.161.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-eld" = 1
  }
}


module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name    = "5gmetacloudplatform"
  cluster_version = "1.31"


  cluster_endpoint_public_access           = true
  enable_cluster_creator_admin_permissions = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_group_defaults = {
    instance_types = ["t3a.large"]
  }

  eks_managed_node_groups = {
    managed-ng-1 = {
      name           = "managed-ng-1"
      ami_type       = "AL2_x86_64"
      instance_types = ["t3a.large"]
      min_size       = 2
      desired_size   = 2
      max_size       = 4
    }
  }
}



module "eks_blueprints_addons" {
  source            = "aws-ia/eks-blueprints-addons/aws"
  version           = "1.19.0"
  cluster_name      = module.eks.cluster_name
  cluster_endpoint  = module.eks.cluster_endpoint
  cluster_version   = module.eks.cluster_version
  oidc_provider_arn = module.eks.oidc_provider_arn

  eks_addons = {
    aws-ebs-csi-driver = {
      most_recent = true
    }
    coredns = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
  }

  enable_cluster_autoscaler           = true
  enable_ingress_nginx                = true

  ingress_nginx = {
    name          = "ingress-nginx"
    chart_version = "4.12.0"
    repository    = "https://kubernetes.github.io/ingress-nginx"
    namespace     = "ingress-nginx"
    values        = [templatefile("${path.module}/values.yaml", {})]
  }
}
