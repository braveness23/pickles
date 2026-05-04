package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/azure"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestKeyVaultWithSecrets(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../01-key-vault-with-secrets",
		NoColor:      true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	keyVaultID := terraform.Output(t, terraformOptions, "key_vault_id")
	keyVaultName := terraform.Output(t, terraformOptions, "key_vault_name")
	resourceGroupName := terraform.Output(t, terraformOptions, "resource_group_name")

	assert.NotEmpty(t, keyVaultID)
	assert.NotEmpty(t, keyVaultName)
	assert.NotEmpty(t, resourceGroupName)

	keyVaultExists := azure.KeyVaultExists(t, keyVaultName, resourceGroupName, "")
	assert.True(t, keyVaultExists)

	secretIDs := terraform.OutputMap(t, terraformOptions, "secret_ids")
	assert.Len(t, secretIDs, 2)
	assert.Contains(t, secretIDs, "db-connection-string")
	assert.Contains(t, secretIDs, "api-key")
}
