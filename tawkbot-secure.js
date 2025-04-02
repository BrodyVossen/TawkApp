const { chromium } = require('playwright');

// Configuration from environment variables
const config = {
  loginUrl: process.env.TAWK_LOGIN_URL || 'https://dashboard.tawk.to/login',
  email: process.env.TAWK_EMAIL,
  password: process.env.TAWK_PASSWORD,
  exportEmail: process.env.TAWK_EXPORT_EMAIL,
  waitTime: parseInt(process.env.TAWK_WAIT_TIME || '3000') // Wait time in milliseconds
};

// Validate required environment variables
const requiredVars = ['TAWK_EMAIL', 'TAWK_PASSWORD', 'TAWK_EXPORT_EMAIL'];
const missingVars = requiredVars.filter(varName => !process.env[varName]);

if (missingVars.length > 0) {
  console.error(`Error: Missing required environment variables: ${missingVars.join(', ')}`);
  console.error('Please set these environment variables before running the script.');
  console.error('Example:');
  console.error('  On Windows: set TAWK_EMAIL=your-email@example.com');
  console.error('  On macOS/Linux: export TAWK_EMAIL=your-email@example.com');
  process.exit(1);
}

async function run() {
  console.log('Starting Tawk.to automation...');
  
  // Launch browser
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Login to dashboard
    await page.goto(config.loginUrl);
    console.log('Navigated to login page');
    
    // Fill in login credentials
    await page.fill('xpath=//*[@id="email"]', config.email);
    await page.fill('xpath=//*[@id="password"]', config.password);
    await page.click('xpath=//*[@id="submit-login"]');
    console.log('Logged in successfully');
    
    // Wait for dashboard to load
    await page.waitForLoadState('networkidle');
    
    // Navigate to inbox
    await page.click('xpath=//*[@id="tawk-inbox-nav"]');
    console.log('Navigated to inbox');
    
    // Click active chat
    await page.click('xpath=//*[@id="tawk-content-view"]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/a/i');
    
    let hasMore = true;
    let pageCount = 0;
    
    while (hasMore) {
      pageCount++;
      console.log(`Processing page ${pageCount}...`);
      
      // Wait for loading
      await page.waitForTimeout(config.waitTime);
      
      // Select all conversations (checkbox)
      await page.click('xpath=//*[@id="tawk-content-view"]/div[2]/div[1]/div/div/div[2]/div/div/div/div[3]/div/div/table/thead/tr/th[1]/div/label/span');
      console.log('Selected all conversations');
      
      // Click export button
      await page.click('xpath=//*[@id="tawk-content-view"]/div[2]/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/button[2]');
      console.log('Clicked export button');
      
      // Enter export email
      await page.fill('xpath=//*[@id="vue-modal"]/div/div[2]/div/div[2]/div/div/div/input', config.exportEmail);
      
      // Click send button
      await page.click('xpath=//*[@id="vue-modal"]/div/div[2]/div/div[3]/button[2]');
      console.log('Export sent to email');
      
      // Wait for the modal to close
      await page.waitForTimeout(config.waitTime);
      
      // Check if there's a next page by looking for the right arrow
      try {
        const nextButton = page.locator('xpath=//*[@id="tawk-content-view"]/div[2]/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/button[2]/i');
        const isEnabled = await nextButton.isEnabled();
        
        if (isEnabled) {
          // Click next page
          await nextButton.click();
          console.log('Navigated to next page');
        } else {
          hasMore = false;
          console.log('No more pages to process');
        }
      } catch (error) {
        hasMore = false;
        console.log('No more pages to process');
      }
    }
    
    console.log('Automation completed successfully!');
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    // Close browser
    await browser.close();
  }
}

// Run the automation
run().catch(console.error); 