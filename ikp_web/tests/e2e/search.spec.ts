import { test, expect } from '@playwright/test';

test.describe('Semantic Search (E2E Integration)', () => {
  test('should load search page, query real backend, and show results', async ({ page }) => {
    // Navigate to the main page
    await page.goto('/');
    
    // Check backend connection status implicitly by seeing if the page loads properly
    // Navigate to Semantic Search tab
    await page.getByRole('button', { name: /search/i }).click();

    // Find the search input
    const searchInput = page.getByPlaceholder(/search the vector/i).or(page.getByPlaceholder(/e.g. Memory configuration/i));
    await expect(searchInput).toBeVisible();

    // Test a real query that exists in the seeded OKF repository
    await searchInput.fill('ProLiant');
    await searchInput.press('Enter');
    
    // Check results containing real seeded data
    await expect(page.locator('body')).toContainText('HPE ProLiant');
    
  });
});
