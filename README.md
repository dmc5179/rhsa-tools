# rhsa-tools
Tools and Scripts for interacting with the Red Hat Security API

Note: The browser session is not started in headless mode because access.redhat.com has a cookies warning.
      When running the pre_scrape.js script, click accept/x/dismiss on any cookie warnings to dismiss them.
      Since the browser session persists across page scrapes, the cookie warning will not appear. If this is not done
      the cookie warning will be present on all scraped pages.

- Install puppeteer

```
npm i puppeteer
```

- Run the pre_scrape.js to start the browser session

```
node pre_scrape.js
```

- Run scrape.js with the headless session link and CVEs to scrape

```
node scrape.js ws://127.0.0.1:38681/devtools/browser/c6252250-d5ea-4e00-b7eb-e1ca4efc1bbc CVE-2017-12806 CVE-2017-3085
```
