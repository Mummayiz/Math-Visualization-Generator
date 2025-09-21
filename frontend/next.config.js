/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_API_URL: 'https://math-vis-backend-production.up.railway.app',
  },
};

module.exports = nextConfig;
