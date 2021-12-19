const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  var myArgs = process.argv.slice(2);
  const browser = await puppeteer.connect({ browserWSEndpoint: myArgs[0], defaultViewport: { width: 1920, height: 1080 } });

    console.log("Process CVE: %s", myArgs[1]);

    const page = await browser.newPage();
    await page.goto('https://access.redhat.com/security/cve/' + myArgs[1], {waitUntil: 'networkidle2'});

    //await page.waitForNavigation(10);

    const html = await page.content()

    await fs.writeFileSync('access/' + myArgs[1] + '.html', html);

    //await page.pdf({ path: 'access/' + myArgs[1] + '.pdf', format: 'a4' });

    await page.close();

    await browser.disconnect();
})();

