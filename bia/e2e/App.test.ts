import { test, expect } from '@playwright/test';

test('Bia component displays and animates text correctly', async ({ page }) => {
  // Navigate to the test page
  await page.goto('http://localhost:5174');

  // Wait for the component to load
  await page.waitForSelector('.BIA');

  // Get the initial text of the component
  const initialText = await page.$eval('.BIA', el => el.textContent);

  // Ensure the initial text is 'BIA'
  expect(initialText).toBe('BIA');

  // Wait for the animation to complete
  await page.waitForSelector('.BIA span.expanded:last-child');
  await page.waitForTimeout(10000);

  // Get the final text of the component
  const finalText = await page.$eval('.BIA', el => el.textContent);

  await page.waitForTimeout(10000);

  // Ensure the final text is 'BIA'
  expect(finalText).toBe('BIA');
});