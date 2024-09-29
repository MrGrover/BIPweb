/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    images: {
      remotePatterns: [
        {
          protocol: 'https',
          hostname: 'www.gravatar.com',
          pathname: '/avatar/**',
        },
      ],
    },
};

export default nextConfig;
