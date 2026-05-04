locals {
  resource_group_name = "rg-keyvault-secrets"
  location            = "eastus"
  key_vault_name      = "kv-secrets-${random_string.suffix.result}"
  sku_name            = "standard"
  }

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

  access_policies = [
    {
      tenant_id = data.azurerm_client_config.current.tenant_id
      object_id = data.azurerm_client_config.current.object_id

      secret_permissions = [
        "Get",
        "List",
        "Set",
        "Delete"
      ]
    }
  ]

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
}

resource "azurerm_key_vault_secret" "secrets" {
  for_each     = local.secrets
  name         = each.key
  value        = each.value
  key_vault_id = module.key_vault.id
}
