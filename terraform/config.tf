terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Terraform Cloud configuration for GitHub Actions
  #  cloud {
  #    organization = "escobarana"
  #
  #    workspaces {
  #      name = "gh-actions-datapipelines"
  #    }
  #  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
  # You don't need these variables if you use the aws cli and login to aws
  # access_key = var.access_key
  # secret_key = var.secret_access_key
}

# Another option, but aws cli is recommended
# export AWS_ACCESS_KEY_ID=your_access_key
# export AWS_SECRET_ACCESS_KEY=your_access_secret
# export AWS_REGION=eu-west-1