/** @type {import('next').NextConfig} */

// Same-origin API proxy: the browser calls the frontend's own origin (/api/v1/*)
// and Next forwards to the backend server-side. This removes the browser's
// dependency on reaching a separate :8000 origin (which fails behind port
// forwarding / containers) and avoids CORS entirely. Target is configurable via
// API_PROXY_TARGET (defaults to localhost:8000 for local dev).
const apiTarget = process.env.API_PROXY_TARGET || "http://localhost:8000";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${apiTarget}/api/v1/:path*`
      }
    ];
  }
};

export default nextConfig;
