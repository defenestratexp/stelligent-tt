# Module 15 sample app on the Node.js 22 LTS Alpine image.
# The app has no npm dependencies, so there is no npm install step.
#
# Build for the architecture your nodes run. EKS Auto Mode's built-in
# general-purpose NodePool launches amd64 (x86_64) instances only, so on an
# Apple silicon Mac build with:
#   docker build --platform linux/amd64 -t sample-app:v1 .
FROM node:22-alpine

ENV NODE_ENV=production \
    PORT=8080

WORKDIR /app
COPY package.json server.js ./

# The official image ships an unprivileged "node" user, uid/gid 1000. Use the
# numbers, not the name: with runAsNonRoot: true, the kubelet can only verify
# a numeric user and refuses to start a container whose USER is a name.
USER 1000:1000

EXPOSE 8080

# Run node directly (not "npm start") so it receives SIGTERM from Kubernetes.
CMD ["node", "server.js"]
