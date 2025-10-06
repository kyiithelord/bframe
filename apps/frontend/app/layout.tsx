import React, { ReactNode } from "react";
import Link from "next/link";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "Inter, ui-sans-serif, system-ui" }}>
        <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
          <aside style={{ background: "#0f172a", color: "white", padding: 16 }}>
            <div style={{ fontWeight: 700, marginBottom: 16 }}>BFrame</div>
            <nav style={{ display: "grid", gap: 8 }}>
              <Link href="/" style={{ color: "#e2e8f0" }}>Home</Link>
              <Link href="/crm" style={{ color: "#e2e8f0" }}>CRM</Link>
              <Link href="/invoices" style={{ color: "#e2e8f0" }}>Invoices</Link>
              <Link href="/admin" style={{ color: "#e2e8f0" }}>Admin</Link>
            </nav>
          </aside>
          <div style={{ display: "grid", gridTemplateRows: "56px 1fr" }}>
            <header style={{ borderBottom: "1px solid #eee", display: "flex", alignItems: "center", padding: "0 16px", gap: 12 }}>
              <input placeholder="Search..." style={{ flex: 1, padding: 8, border: "1px solid #e5e7eb", borderRadius: 6 }} />
              <div style={{ color: "#475569" }}>admin@bframe.local</div>
            </header>
            <section>
              {children}
            </section>
          </div>
        </div>
      </body>
    </html>
  );
}
