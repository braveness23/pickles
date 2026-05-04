package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/azure"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestSimpleExample(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../00-simple-example",
		NoColor:      true,
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	keyVaultID := terraform.Output(t, terraformOptions, "key_vault_id")
	keyVaultName := terraform.Output(t, terraformOptions, "key_vault_name")
	keyVaultURI := terraform.Output(t, terraformOptions, "key_vault_uri")
	resourceGroupName := terraform.Output(t, terraformOptions, "resource_group_name")

	assert.NotEmpty(t, keyVaultID)
	assert.NotEmpty(t, keyVaultName)
	assert.NotEmpty(t, keyVaultURI)
	assert.NotEmpty(t, resourceGroupName)

	keyVaultExists := azure.KeyVaultExists(t, keyVaultName, resourceGroupName, "")
	assert.True(t, keyVaultExists)
}
