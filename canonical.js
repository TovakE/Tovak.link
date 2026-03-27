(() => {
  const CANONICAL_HOST = "tovak.net";
  const LEGACY_HOSTS = new Set(["tovak.link", "www.tovak.link", "www.tovak.net"]);

  const { hostname, pathname, search, hash } = window.location;
  if (!LEGACY_HOSTS.has(hostname)) {
    return;
  }

  const target = `https://${CANONICAL_HOST}${pathname}${search}${hash}`;
  if (window.location.href !== target) {
    window.location.replace(target);
  }
})();
