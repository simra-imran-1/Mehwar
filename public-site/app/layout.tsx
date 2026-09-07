import type { Metadata, Viewport } from "next";
import { Manrope, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const sans = Manrope({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
  adjustFontFallback: true,
});
const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});

const title =
  "MEHWAR — Autonomy-Assurance Evaluation for Navigation Controllers";
const description =
  "Research-backed evaluation of navigation-controller capability boundaries and mission-liveness failures.";
export const metadata: Metadata = {
  metadataBase: new URL("https://mehwar-deftech.vercel.app"),
  title,
  description,
  alternates: { canonical: "https://mehwar-deftech.vercel.app/" },
  icons: { icon: "/icon.svg" },
  openGraph: {
    title,
    description,
    type: "website",
    locale: "en_US",
    siteName: "MEHWAR",
    url: "https://mehwar-deftech.vercel.app/",
    images: [
      {
        url: "/opengraph-image.png",
        width: 1200,
        height: 630,
        alt: "MEHWAR: 0 invalid actions. Mission not completed. Actual C4-0001 trajectory evidence.",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    images: ["/opengraph-image.png"],
  },
};
export const viewport: Viewport = { themeColor: "#f8f8f4" };
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
