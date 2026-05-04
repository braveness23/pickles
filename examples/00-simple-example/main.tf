locals {
  resource_group_name = "rg-keyvault-simple"
  location            = "eastus"
  key_vault_name      = "kv-simple-${random_string.suffix.result}"
  sku_name            = "standard"

  tags = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}

data "azurerm_client_config" "current" {}

module "key_vault" {
  source = "../../"

  name                = local.key_vault_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = local.sku_name
  
  tags = local.tags
}

resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = local.location
  tags     = local.tags
