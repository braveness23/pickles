.PHONY: test cleanup test-00-simple-example test-01-key-vault-with-secrets test-02-key-vault-with-private-endpoint

test: test-00-simple-example test-01-key-vault-with-secrets test-02-key-vault-with-private-endpoint
	@echo "All tests completed"

test-00-simple-example:
	@echo "Testing 00-simple-example..."
	go test -v -timeout 30m -run TestSimpleExample

test-01-key-vault-with-secrets:
	@echo "Testing 01-key-vault-with-secrets..."
	go test -v -timeout 30m -run TestKeyVaultWithSecrets

test-02-key-vault-with-private-endpoint:
	@echo "Testing 02-key-vault-with-private-endpoint..."
	go test -v -timeout 30m -run TestKeyVaultWithPrivateEndpoint

cleanup:
	@echo "Cleaning up..."
	find .. -type d -name ".terraform" -exec rm -rf {} + 2>/dev/null || true
	find .. -type f -name ".terraform.lock.hcl" -delete 2>/dev/null || true
	find .. -type f -name "terraform.tfstate*" -delete 2>/dev/null || true
	@echo "Cleanup complete"
