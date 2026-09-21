# Module 15 Sample App

A small web server on Node.js 22 with no npm dependencies. It shows a
background color, a version string and the hostname of the container
that served the request, which in Kubernetes is the Pod name. That makes
rolling updates and load balancing visible in a browser.

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `8080` | Port the server listens on |
| `BG_COLOR` | `white` | Page background: a CSS color name or `#hex` value |
| `APP_VERSION` | `v1` | Shown on the page |

`GET /healthz` returns `ok` for readiness and liveness probes.

The 2022 version was a Create React App on Node.js 12. React read
`REACT_APP_BG_COLOR` only when the bundle was built, so the color could
change at runtime only because the container ran the development server.
This version reads its variables when the process starts, which is how
container configuration is meant to work.

## Run it locally

```bash
docker build -t sample-app:v1 .
docker run --rm -p 8080:8080 -e BG_COLOR=teal sample-app:v1
```

Open `http://localhost:8080`, then stop the container with Ctrl+C.

On an Apple silicon Mac, add `--platform linux/amd64` to `docker build`
before you push the image for EKS. The Auto Mode `general-purpose`
NodePool runs only amd64 nodes, and an arm64-only image fails there with
`exec format error`.
