terraform {
  backend "s3" {
    bucket = "environment-scaler-automation-infra-state"
    key    = "autoscale-iac/terraform.tfstate"
    dynamodb_table = "autoscale-iac-dynamodb-state-lock-terraform"
    region = "us-east-1"
  }
}

