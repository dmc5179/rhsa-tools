const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:39781/devtools/browser/fdd8d8f8-9538-4df6-91a0-0828cdb5605b' });
  const page = await browser.newPage();
  await page.goto('https://access.redhat.com/security/cve/CVE-2020-27838');
  //await page.screenshot({ path: 'example.png' });
  //await page.pdf({ path: 'CVE-2020-27838.pdf', format: 'a4' });

  const html = await page.content()

  fs.writeFile('./CVE-2020-27838.html', html, err => {
    if (err) {
      console.error(err)
      return
    }
    //file written successfully
  })

  await browser.disconnect();
})();

