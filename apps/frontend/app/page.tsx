"use client";
import React, { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Home() {
  const [token, setToken] = useState<string>("");
  const [leads, setLeads] = useState<any[]>([]);

  async function login() {
    const body = new URLSearchParams();
    body.set("username", "admin@bframe.local");
    body.set("password", "admin123");
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
    const data = await res.json();
    setToken(data.access_token);
  }

  async function fetchLeads() {
    const res = await fetch(`${API_BASE}/crm/leads`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setLeads(data);
  }

  async function createLead() {
    const res = await fetch(`${API_BASE}/crm/leads`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: "Web Lead" }),
    });
    if (res.ok) fetchLeads();
  }

  useEffect(() => {
    if (token) fetchLeads();
  }, [token]);

  return (
    <main style={{ padding: 24 }}>
      <h1>BFrame Admin</h1>
      {!token ? (
        <button onClick={login}>Login</button>
      ) : (
        <>
          <button onClick={createLead}>Create Lead</button>
          <ul>
            {leads.map((l) => (
              <li key={l.id}>{l.name} {l.email ? `(${l.email})` : ""}</li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}
