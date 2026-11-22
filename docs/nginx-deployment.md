# Deploying KERRCO to an Nginx VPS

Target: `https://kerrco.us`. These are preparation instructions, not a record of deployment. The VPS operating system, SSH destination, permissions, certificate manager, and current Nginx layout still need confirmation. Existing `order.kerrco.us` configuration must remain intact.

## Prepare a release locally

Install/use Node.js and a `tar` command available on PATH. The website itself remains buildless and needs no Node.js process on the VPS.

```sh
node scripts/prepare-release.mjs --check
node scripts/prepare-release.mjs
```

The first command checks links, fragments, image dimensions, metadata, email recipients, canonical URLs, and sitemap destinations. The second repeats those checks and creates a new release directory and `.tar.gz` in ignored `artifacts/`, plus a JSON manifest, a file-level `-SHA256SUMS`, and an archive `.sha256` checksum. Only referenced static assets and the nine pages/search files are packaged; PHP handlers, unused originals, and old vendor assets are excluded. No network calls or deployment occur.

Resolve the browser checks in `website-browser-review.md` before calling the release ready. Regenerate the bundle after any change to `web/`.

## VPS layout and initial configuration

Use a layout such as:

```text
/var/www/kerrco/
  releases/
    <release-id>/
      index.html
      assets/
      ...
  current -> releases/<release-id>
```

Create this directory with ownership appropriate to the existing deployment user. Nginx needs read/traverse access, not write access. Keep deployment archives, checksums, Nginx snippets, and planning documents outside the served directory. Do not change ownership or permissions on unrelated sites.

`deploy/nginx/kerrco-static.conf` is a snippet for the HTTPS server. It serves files from `current`, retains established `.html` URLs, uses the site's 404 document with a 404 response, and applies short asset caching. It does not provide a PHP runtime.

`deploy/nginx/kerrco.us.conf.example` shows how to include the snippet in an HTTPS server and redirect HTTP. Certificate paths and the ACME webroot are examples. Adapt them to the VPS's certificate provisioning and renewal process; the example does not obtain certificates. Ensure Nginx's main configuration includes MIME types, normally via `include /etc/nginx/mime.types;`, so CSS and SVG are served correctly.

If there is already a `kerrco.us` server block, back it up and update that block rather than adding a conflicting duplicate. Preserve all other virtual hosts. Run `sudo nginx -t` before reloading; on a systemd host, reload with `sudo systemctl reload nginx` only after a successful test. These commands have not been run on the VPS.

## Upload and switch releases

Once publication is authorized, upload the `.tar.gz`, its `.sha256`, and the matching `-SHA256SUMS` to a nonpublic staging directory using the existing SSH/SFTP workflow. Substitute the actual generated names below; do not type placeholder angle brackets literally.

```sh
# In the nonpublic upload directory:
sha256sum -c <archive>.tar.gz.sha256
tar -tzf <archive>.tar.gz

# Create a NEW directory with a unique release ID; do not reuse an old release.
mkdir /var/www/kerrco/releases/<release-id>
tar -xzf <archive>.tar.gz -C /var/www/kerrco/releases/<release-id>
cd /var/www/kerrco/releases/<release-id>
sha256sum -c <absolute-upload-path>/<release-name>-SHA256SUMS
```

The directory must contain `index.html` directly, not an extra `web/` directory. Check `current` with `ls -ld /var/www/kerrco/current` and record its existing target before the switch. On an initial deployment it may not exist. If it is a real directory rather than a symlink, plan that one-time migration separately; do not overwrite it with these commands.

On a GNU/Linux VPS, switch a symlink using a new, unique temporary name in the same parent directory:

```sh
ln -s /var/www/kerrco/releases/<release-id> /var/www/kerrco/current-next-<release-id>
mv -T /var/www/kerrco/current-next-<release-id> /var/www/kerrco/current
```

Use the deployment account or the VPS's existing privilege process. Keep the previous release directory. This switch changes only the document-root target; do not reload or restart the separate water application.

## Verify and roll back

Check production HTTPS, homepage, all navigation paths, CSS/SVG MIME types, photography, consultation links, robots.txt, and sitemap.xml. Request an unknown URL and confirm status 404 with the custom page; request `/forms/contact.php` and confirm it is not served. Check the three historical construction URLs. Confirm HTTP redirects to the canonical HTTPS origin.

```sh
curl -I https://kerrco.us/
curl -I https://kerrco.us/assets/css/home.css
curl -I https://kerrco.us/assets/img/favicon.svg
curl -I https://kerrco.us/this-page-does-not-exist
curl -I http://kerrco.us/
```

If the release fails, create another uniquely named temporary symlink to the recorded previous release, then use the same `mv -T` pattern to replace `current`. Recheck the site. If Nginx configuration also changed, restore its recorded backup, run `nginx -t`, and reload only after it passes. Do not delete old releases until the owner chooses a retention policy.

## Validation limits and references

The configuration follows Nginx's documented [file lookup and 404 handling](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files) and [HTTPS server configuration](https://nginx.org/en/docs/http/configuring_https_servers.html). No VPS connection, Nginx syntax test, certificate provisioning, routing test, or deployment has been performed locally. Browser review remains separate from static packaging checks.
