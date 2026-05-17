# Kerrco

Static website for KERRCO Construction.

## Site Structure

- `web/index.html` - home page with services, project gallery, and contact footer
- `web/*-project-details.html` - real project detail pages
- `web/assets/css/main.css` - site styles
- `web/assets/js/main.js` - site behavior
- `web/forms/*.php` - optional PHP mail handlers for form posts

The site intentionally excludes the original BootstrapMade template demo pages so unfinished placeholder content is not deployed.

## Local Preview

From the repository root:

```sh
python3 -m http.server 8080 --directory web
```

Then open `http://localhost:8080/`.

## Deployment Notes

- Deploy the contents of `web/`.
- PHP form handlers require a host with PHP mail support. If the host does not provide mail delivery, route forms through the hosting provider's SMTP or a transactional email service.
- Before publishing, check that all internal links and image references resolve.
- Keep images compressed before committing; oversized originals should stay outside the deployed `web/assets/img` tree.
