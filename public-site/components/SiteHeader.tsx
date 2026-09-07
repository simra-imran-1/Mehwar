"use client";
import { useRef } from "react";
import { Brand } from "./Brand";
const links = [
  ["Evidence", "evidence"],
  ["Workflow", "workflow"],
  ["Boundaries", "boundaries"],
  ["Roadmap", "roadmap"],
  ["Team", "team"],
];
export function SiteHeader() {
  const menu = useRef<HTMLDetailsElement>(null);
  return (
    <header className="site-header">
      <div className="header-inner">
        <a href="#main" aria-label="MEHWAR home">
          <Brand />
        </a>
        <nav className="desktop-nav" aria-label="Main navigation">
          {links.map(([label, id]) => (
            <a href={`#${id}`} key={id}>
              {label}
            </a>
          ))}
        </nav>
        <a className="header-cta" href="#evidence">
          Inspect Evidence <span aria-hidden="true">↗</span>
        </a>
        <details
          className="mobile-menu"
          ref={menu}
          onKeyDown={(event) => {
            if (event.key === "Escape" && menu.current) {
              menu.current.open = false;
              menu.current.querySelector("summary")?.focus();
            }
          }}
        >
          <summary>
            Menu <span aria-hidden="true">+</span>
          </summary>
          <nav aria-label="Mobile navigation">
            {links.map(([label, id]) => (
              <a
                href={`#${id}`}
                key={id}
                onClick={() => {
                  if (menu.current) menu.current.open = false;
                }}
              >
                {label}
                <span aria-hidden="true">↗</span>
              </a>
            ))}
            <a href="/deftech-2026">
              DEFTECH 2026 snapshot <span aria-hidden="true">↗</span>
            </a>
          </nav>
        </details>
      </div>
    </header>
  );
}
