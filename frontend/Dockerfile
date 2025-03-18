# Stage 1: Build the Next.js app
FROM node:20 AS builder

WORKDIR /taller

# Install pnpm manually
RUN npm install -g pnpm

# Copy dependencies and install only production dependencies
COPY ./taller/pnpm-lock.yaml ./taller/package.json ./
RUN pnpm install --frozen-lockfile

# Copy the rest of the app and build
COPY ./taller .
RUN pnpm build

# Stage 2: Run the app
FROM node:20 AS runner

WORKDIR /taller

# Copy the standalone output
COPY --from=builder /taller/.next/standalone ./
COPY --from=builder /taller/public ./public
COPY --from=builder /taller/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
