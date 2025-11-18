import { test, expect } from '@playwright/test';

test.describe('Harness Editor E2E Tests', () => {

  test.beforeEach(async ({ page }) => {
    // UAT-1: Screen loads correctly.
    // We are now hitting a live backend, which should provide an initial harness state.
    await page.goto('/');
    await expect(page.getByTestId('sidebar')).toBeVisible();
    await expect(page.getByTestId('rf-canvas-wrapper')).toBeVisible();
  });

  test('allows dragging components, connecting them, and persists the result', async ({ page }) => {
    // The backend should provide these components via the real API
    await expect(page.getByText('CONN1')).toBeVisible();
    await expect(page.getByText('CONN2')).toBeVisible();

    // UAT-2: Drag and drop components
    const conn1 = page.getByText('CONN1');
    const conn2 = page.getByText('CONN2');
    // Target the pane, which is the actual element that receives pointer events.
    const canvas = page.locator('.react-flow__pane');

    // Drag the first connector
    await conn1.dragTo(canvas, {
      targetPosition: { x: 200, y: 150 },
    });

    // Verify the first node is on the canvas before proceeding
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN1' })).toBeVisible();
    
    // Drag the second connector
    await conn2.dragTo(canvas, {
      targetPosition: { x: 500, y: 250 },
    });

    // Verify both nodes are on the canvas
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN1' })).toBeVisible();
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN2' })).toBeVisible();

    // UAT-3: Connect two nodes
    // Note: The data-testid for handles might need to be adjusted if the real data is different.
    // Assuming the real component data also creates pins with IDs '1' and '2'.
    const handleSource = page.getByTestId('handle-source-CONN1-1');
    const handleTarget = page.getByTestId('handle-target-CONN2-1');

    await handleSource.dragTo(handleTarget);

    // Verify edge is created
    await expect(page.locator('.react-flow__edge')).toHaveCount(1);

    // UAT-4: Data persistence
    // Wait for the debounced save (a PUT request) to fire.
    // We wait for the response from the real API.
    await page.waitForResponse(response => 
      response.url().includes('/api/v1/harnesses/') && response.request().method() === 'PUT'
    );
    
    await page.reload();

    // Verify nodes and edge still exist after reload
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN1' })).toBeVisible();
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN2' })).toBeVisible();
    await expect(page.locator('.react-flow__edge')).toHaveCount(1);
  });
});
