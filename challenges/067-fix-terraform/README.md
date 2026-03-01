# Challenge 067: Fix Terraform Config

## Difficulty: Hard

## Task

The file `setup/main.tf` is a broken Terraform configuration. Fix all the issues so the configuration is valid and follows Terraform best practices.

## Setup

- `setup/main.tf` — A broken Terraform configuration file

## Requirements

Fix the Terraform configuration so that:

1. There are no circular resource references
2. All variables that are used are properly declared
3. Resource type names follow proper Terraform naming conventions (`provider_resource`)
4. Output blocks reference attributes that actually exist on the declared resources
5. The provider is properly configured
6. Resource configurations are syntactically valid

## Rules

- Only modify `setup/main.tf`
- Maintain the original intent of the infrastructure (an AWS VPC with a subnet, security group, and EC2 instance)
- All resources should be logically connected without circular dependencies
