const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  var myArgs = process.argv.slice(2);
  const browser = await puppeteer.connect({ browserWSEndpoint: myArgs[0], defaultViewport: { width: 1280, height: 1024 } });

  for (let j = 1; j < myArgs.length; j++) {

    console.log("Process CVE: %s", myArgs[j]);

    const page = await browser.newPage();
    await page.goto('https://access.redhat.com/security/cve/' + myArgs[j]);

    const html = await page.content()

    fs.writeFile('access/' + myArgs[j] + '.html', html, err => {
      if (err) {
        console.error(err);
        //return
      }
      //file written successfully
    })

    await page.close();

  }

  await browser.disconnect();
})();

