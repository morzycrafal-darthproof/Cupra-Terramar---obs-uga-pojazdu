const CACHE = "cupra-terramar-v13";
const ASSETS = ["./", "./index.html", "./manifest.json", "./icon-192.png", "./icon-512.png", "./emblem.png",
  "./apple-touch-icon.png", "./favicon-16.png", "./favicon-32.png"];

self.addEventListener("install", (e) => {
  // cache: "reload" — a new version must not pick up an older icon from the browser's HTTP cache
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS.map((u) => new Request(u, { cache: "reload" })))).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  // Google sign-in / Sheets API and other hosts: straight to the network, never cached
  if (new URL(e.request.url).origin !== self.location.origin) return;
  const isHTML =
    e.request.mode === "navigate" ||
    (e.request.method === "GET" && (e.request.headers.get("accept") || "").includes("text/html"));

  if (isHTML) {
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});
