import { test, expect } from '@playwright/test';

test.describe('Validation Portal', () => {
  test('should load the validation page if it exists', async ({ page }) => {
    await page.goto('/');
    
    // Check if we can navigate to validation or if it's the main page
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Our basic sanity check that the application renders without crashing
    const root = page.locator('#root, #app');
    if (await root.count() > 0) {
      await expect(root).not.toBeEmpty();
    }
  });
});
