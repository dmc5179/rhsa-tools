const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  var myArgs = process.argv.slice(2);
  const browser = await puppeteer.connect({ browserWSEndpoint: myArgs[0], defaultViewport: { width: 1280, height: 1024 } });
  const page = await browser.newPage();
  await page.goto('https://access.redhat.com/security/cve/' + myArgs[1]);
  //await page.screenshot({ path: 'example.png' });
  //await page.pdf({ path: 'CVE-2020-27838.pdf', format: 'a4' });

  const html = await page.content()

  fs.writeFile('access/' + myArgs[1] + '.html', html, err => {
    if (err) {
      console.error(err)
      return
    }
    //file written successfully
  })

  await page.close();

  await browser.disconnect();
})();

