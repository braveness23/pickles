output "key_vault_id" {
  description = "Key Vault resource ID"
  value       = module.key_vault.id
}

output "key_vault_name" {
  description = "Key Vault name"
  value       = module.key_vault.name
}

output "key_vault_uri" {
  description = "Key Vault URI"
  value       = module.key_vault.vault_uri
}

output "private_endpoint_id" {
  description = "Private endpoint resource ID"
  value       = azurerm_private_endpoint.key_vault.id
}

output "private_ip_address" {
  description = "Private IP address"
  value       = azurerm_private_endpoint.key_vault.private_service_connection[0].private_ip_address
}

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}
