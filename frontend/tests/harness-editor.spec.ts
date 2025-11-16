import { test, expect } from '@playwright/test';
import type { HarnessData } from '../src/utils/dataTransformer';

test.describe('Harness Editor E2E Tests', () => {
  // This variable will act as our "database" for the test run.
  let harnessState: HarnessData;

  test.beforeEach(async ({ page }) => {
    // Reset state before each test
    harnessState = {
      name: 'Initial Harness',
      connectors: [],
      wires: [],
      connections: [],
    };

    // Mock the components API endpoint
    await page.route('/api/v1/components/', async (route) => {
      const mockComponents = [
        {
          id: '1',
          type: 'connector',
          name: 'CONN1',
          data: { name: 'CONN1', part_number: '123-456', pins: [{ id: '1' }, { id: '2' }] },
        },
        {
          id: '2',
          type: 'connector',
          name: 'CONN2',
          data: { name: 'CONN2', part_number: '789-012', pins: [{ id: '1' }, { id: '2' }] },
        },
      ];
      await route.fulfill({ json: mockComponents });
    });

    // Mock the harness API endpoint for both GET and PUT
    await page.route('/api/v1/harnesses/3fa85f64-5717-4562-b3fc-2c963f66afa6', async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({ status: 200, json: harnessState });
      } else if (route.request().method() === 'PUT') {
        harnessState = route.request().postDataJSON() as HarnessData;
        await route.fulfill({ status: 200, json: harnessState });
      }
    });
    
    // UAT-1: Screen loads correctly
    await page.goto('/');
    await expect(page.getByTestId('sidebar')).toBeVisible();
    await expect(page.getByTestId('rf-canvas-wrapper')).toBeVisible();
  });

  test('allows dragging components, connecting them, and persists the result', async ({ page }) => {
    // The beforeEach hook has already set up the mocks.
    // The test body can now just focus on the user actions.

    // Wait for components to load in the sidebar
    await expect(page.getByTestId('component-CONN1')).toBeVisible();
    await expect(page.getByTestId('component-CONN2')).toBeVisible();

    // UAT-2: Drag and drop components
    const conn1 = page.getByTestId('component-CONN1');
    const conn2 = page.getByTestId('component-CONN2');
    const canvas = page.getByTestId('rf-canvas-wrapper');

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

    // Verify nodes are on the canvas
    const node1 = page.locator('.react-flow__node').filter({ hasText: 'CONN1' });
    const node2 = page.locator('.react-flow__node').filter({ hasText: 'CONN2' });
    await expect(node1).toBeVisible();
    await expect(node2).toBeVisible();

    // UAT-3: Connect two nodes
    const handleSource = page.getByTestId('handle-source-CONN1-1');
    const handleTarget = page.getByTestId('handle-target-CONN2-1');

    await handleSource.dragTo(handleTarget);

    // Verify edge is created
    await expect(page.locator('.react-flow__edge')).toHaveCount(1);

    // UAT-4: Data persistence
    // Wait for the debounced save (a PUT request) to fire
    await page.waitForResponse(response => 
      response.url().includes('/api/v1/harnesses/') && response.request().method() === 'PUT'
    );
    
    await page.reload();

    // Verify nodes and edge still exist after reload
    // The GET request on reload will now be served by our mock, returning the saved `harnessState`.
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN1' })).toBeVisible();
    await expect(page.locator('.react-flow__node').filter({ hasText: 'CONN2' })).toBeVisible();
    await expect(page.locator('.react-flow__edge')).toHaveCount(1);
  });
});
