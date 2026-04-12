import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",   // статическая сборка → frontend/out/
  trailingSlash: true,
};

export default nextConfig;
