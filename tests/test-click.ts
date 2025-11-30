import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000/');
  await page.getByText('48', { exact: true }).click();
  await page.getByRole('link', { name: 'Manual Control' }).click();
  await page.getByRole('button', { name: 'Connect Camera stream' }).click();
  await page.getByRole('button', { name: 'EMERGENCY STOP' }).click();
  await page.getByRole('button', { name: 'TRIGGER STOP' }).click();
  await page.getByRole('link', { name: 'Configuration' }).click();
  await page.getByRole('button', { name: 'Save Configuration' }).click();
  await page.getByRole('link', { name: 'System Logs' }).click();
  await page.getByRole('button', { name: 'Switch to contrast theme' }).click();
  await page.getByRole('button', { name: 'Switch to light theme' }).click();
  await page.getByRole('button', { name: 'Switch to dark theme' }).click();
});