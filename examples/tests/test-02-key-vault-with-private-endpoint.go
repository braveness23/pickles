package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/azure"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestKeyVaultWithPrivateEndpoint(t *testing.T) {
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../02-key-vault-with-private-endpoint",
		NoColor:      true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	keyVaultID := terraform.Output(t, terraformOptions, "key_vault_id")
	keyVaultName := terraform.Output(t, terraformOptions, "key_vault_name")
	privateEndpointID := terraform.Output(t, terraformOptions, "private_endpoint_id")
	privateIPAddress := terraform.Output(t, terraformOptions, "private_ip_address")
	resourceGroupName := terraform.Output(t, terraformOptions, "resource_group_name")

	assert.NotEmpty(t, keyVaultID)
	assert.NotEmpty(t, keyVaultName)
	assert.NotEmpty(t, privateEndpointID)
	assert.NotEmpty(t, privateIPAddress)
	assert.NotEmpty(t, resourceGroupName)

	keyVaultExists := azure.KeyVaultExists(t, keyVaultName, resourceGroupName, "")
	assert.True(t, keyVaultExists)

	assert.Regexp(t, `^10\.0\.1\.\d+$`, privateIPAddress)
}
