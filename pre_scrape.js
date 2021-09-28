const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const endpoint = browser.wsEndpoint();
  console.log(endpoint);
  const page = await browser.newPage();
  await page.goto('https://access.redhat.com/security/cve/CVE-2020-27838');
  //await page.screenshot({ path: 'example.png' });

  //await browser.close();
})();

