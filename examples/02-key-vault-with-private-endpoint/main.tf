locals {
  resource_group_name           = "rg-keyvault-private"
  location                      = "eastus"
  key_vault_name                = "kv-private-${random_string.suffix.result}"
  vnet_name                     = "vnet-keyvault"
  subnet_name                   = "snet-private-endpoints"
  sku_name                      = "premium"
  public_network_access_enabled = false
  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

data "azurerm_client_config" "current" {}

module "key_vault" {
  source = "../../"

  name                          = local.key_vault_name
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  sku_name                      = local.sku_name
  public_network_access_enabled = local.public_network_access_enabled

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

resource "azurerm_virtual_network" "main" {
  name                = local.vnet_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.tags
}

resource "azurerm_subnet" "private_endpoints" {
  name                 = local.subnet_name
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_private_endpoint" "key_vault" {
  name                = "pe-${local.key_vault_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_endpoints.id

  private_service_connection {
    name                           = "psc-keyvault"
    private_connection_resource_id = module.key_vault.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  tags = local.tags
}
