import { test, expect } from '@playwright/test';

test.describe('Validation and BOQ Tests (E2E Integration)', () => {
  test('BOQ Validation should show success and failure states with real backend', async ({ page }) => {
    // We are no longer mocking API calls
    await page.goto('/');
    
    // Navigate to BOQ Validation tab
    await page.getByRole('button', { name: /boq/i }).click();

    const textArea = page.getByPlaceholder(/e.g. P52562-B21/i);
    
    // Test Success using a real seeded SKU
    await textArea.fill('P80390-B21');
    await page.getByRole('button', { name: 'Validate BOQ' }).click();

    // The backend should return Validation Passed and list some engineering rules
    await expect(page.locator('body')).toContainText('Validation Passed', { timeout: 20000 });
    // Expect some rule text to appear in the evaluation output
    await expect(page.locator('body')).toContainText('Rule', { timeout: 20000 });

    // Test Failure using a garbage SKU that the backend will reject or flag
    await textArea.fill('INVALID-SKU-999');
    await page.getByRole('button', { name: 'Validate BOQ' }).click();
    
    // It should either say invalid or fail to find a valid solution
    await expect(page.locator('body')).toContainText(/error|invalid|fail/i, { timeout: 15000 });
  });

  test('Validation Portal should load queue and function normally', async ({ page }) => {
    // We will just verify the queue loads without crashing since the queue might be empty in a real DB
    await page.goto('/');
    await page.getByRole('button', { name: /Validation Portal/i }).click();

    // In a real state, it might say "Queue is empty" or "Pending Review"
    // Let's just ensure it renders one of those states and does not error out.
    await expect(page.locator('body')).toContainText(/Queue is empty|Pending Review/i, { timeout: 10000 });
  });
});
