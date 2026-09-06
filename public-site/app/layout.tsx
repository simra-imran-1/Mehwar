import type { Metadata } from "next";
import "./globals.css";

const title =
  "MEHWAR — Autonomy-Assurance Evaluation for Navigation Controllers";
const description =
  "Research-backed evaluation of navigation-controller capability boundaries and mission-liveness failures.";
export const metadata: Metadata = {
  title,
  description,
  icons: { icon: "/icon.svg" },
  openGraph: {
    title,
    description,
    type: "website",
    locale: "en_US",
    siteName: "MEHWAR",
  },
};
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
