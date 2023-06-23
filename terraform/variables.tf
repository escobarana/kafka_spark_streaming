# This variable defines the AWS Region.
variable "region" {
  description = "region to use for AWS resources"
  type        = string
  default     = "eu-west-1"
}

variable "global_prefix" {
  type    = string
  default = "dsti-msk"
}

variable "private_cidr_blocks" {
  type = list(string)
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24",
  ]
}

variable "cidr_blocks_bastion_host" {
  type = list(string)
  default = ["10.0.4.0/24"]
}
