"use client";
import React, { ReactNode, useEffect, useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function RootLayout({ children }: { children: ReactNode }) {
  const [q, setQ] = useState("");
  const [token, setToken] = useState<string>("");
  const [open, setOpen] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (t) setToken(t);
  }, []);

  useEffect(() => {
    if (!q || !token) { setResults([]); return; }
    const handle = setTimeout(async () => {
      try {
        const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) return;
        const data = await res.json();
        setResults(data.results || []);
        setOpen(true);
      } catch {}
    }, 250);
    return () => clearTimeout(handle);
  }, [q, token]);

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
          <div style={{ display: "grid", gridTemplateRows: "56px 1fr", position: "relative" }}>
            <header style={{ borderBottom: "1px solid #eee", display: "flex", alignItems: "center", padding: "0 16px", gap: 12, position: "relative" }}>
              <input
                placeholder="Search..."
                value={q}
                onChange={(e) => setQ(e.target.value)}
                onFocus={() => q && setOpen(true)}
                style={{ flex: 1, padding: 8, border: "1px solid #e5e7eb", borderRadius: 6 }}
              />
              {open && results.length > 0 && (
                <div onMouseLeave={() => setOpen(false)} style={{ position: "absolute", top: 52, left: 16, right: 16, background: "#fff", border: "1px solid #e5e7eb", borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.08)", zIndex: 50 }}>
                  {results.map((r, idx) => (
                    <div key={idx} style={{ padding: 10, borderTop: idx ? "1px solid #f1f5f9" : "none", display: "flex", gap: 8 }}>
                      <span style={{ fontSize: 12, color: "#64748b", minWidth: 70, textTransform: "capitalize" }}>{r.type}</span>
                      {r.type === "lead" ? (
                        <Link href="/crm" style={{ color: "#0f172a" }} onClick={() => setOpen(false)}>
                          {r.name} {r.email ? `(${r.email})` : ""}
                        </Link>
                      ) : (
                        <Link href="/invoices" style={{ color: "#0f172a" }} onClick={() => setOpen(false)}>
                          {r.number} — {r.customer_name}
                        </Link>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </header>
            <section>
              {children}
            </section>
          {/* close outer grid container */}
          </div>
        </div>
      </body>
    </html>
  );
}
