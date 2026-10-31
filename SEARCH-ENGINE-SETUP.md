# Google Search setup

The public build generates sitemap.xml with the homepage and all seven guide
URLs. Each page has a unique title, description, absolute canonical URL, and
structured data. Utility pages and the legacy redirect are marked noindex and
excluded from the sitemap. All guide text and navigation are in the initial
HTML; crawlers do not need to run JavaScript to read the guides.

## Submit the site to Google

1. Open https://search.google.com/search-console and add a **URL-prefix**
   property for `https://doomoorboomoor.github.io/AI-Desktop-guides/`.
   Use the full repository path and trailing slash.
2. Choose **HTML tag** ownership verification. Copy only the `content` value
   of Google's verification meta tag into `google_site_verification` in
   `Authoring/site.json`. Rebuild and deploy, then click **Verify** in Search
   Console. Keep the value in configuration after successful verification.
   This is a public verification token, not a password or API key.
3. In **Sitemaps**, submit
   `https://doomoorboomoor.github.io/AI-Desktop-guides/sitemap.xml`.
4. Use **URL Inspection** on the homepage and select **Request indexing**.
   Monitor the sitemap and Page indexing reports for Google's results.

Search Console authentication and ownership verification are account-side steps;
publishing these files does not perform them. No submission or indexing success
is implied until confirmed in Search Console. Crawling may take days or weeks,
and Google does not guarantee inclusion or rankings. Google can discover sites
without manual notification. Its old unauthenticated sitemap ping endpoint is
retired; do not use it.

## GitHub Pages robots.txt limitation

Google checks `https://doomoorboomoor.github.io/robots.txt`, not a robots.txt
inside `/AI-Desktop-guides/`. This repository's generated robots.txt is a ready
template for a host-root deployment; its project-path copy does not control
crawling or submit the sitemap. Submit directly in Search Console for this site.

If you maintain the separate `doomoorboomoor.github.io` host-root repository,
merge this line into its existing robots.txt without replacing other rules:

```text
Sitemap: https://doomoorboomoor.github.io/AI-Desktop-guides/sitemap.xml
```

An absent host-root robots.txt returning 404 normally permits crawling. A host
root rule that disallows this project must be corrected at the host root.

## Maintenance and verification

- Edit site identity, canonical base URL, and optional verification token in
  `Authoring/site.json`. Rebuild with `python Build-Pages.py`.
- The sitemap deliberately omits lastmod timestamps rather than reporting build
  time as the date of a significant content change.
- Verify sitemap URLs return 200 and their canonical URLs match. Keep private
  repository URLs, utility pages, redirects, query strings, and fragments out
  of the sitemap. Structured data describes the content; it does not promise
  a rich-result feature.

Official guidance:
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://developers.google.com/crawling/docs/robots-txt/create-robots-txt
- https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
