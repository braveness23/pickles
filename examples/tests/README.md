# Terraform Module Tests

Automated tests for Azure Key Vault Terraform module using [Terratest](https://terratest.gruntwork.io/).

## Prerequisites

- Go 1.21+
- Azure subscription
- Azure CLI authenticated
- Terraform installed

## Running Tests

```bash
make test              # Run all tests
make test-00-simple-example
make test-01-key-vault-with-secrets
make cleanup           # Cleanup artifacts
```
