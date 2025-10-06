"use client";
import React, { useEffect, useMemo, useState } from "react";
import { Toasts, ToastItem } from "../../components/Toast";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

type InvoiceItem = {
  id?: number;
  description: string;
  quantity: number;
  unit_price: number;
  line_total?: number;
};

type Invoice = {
  id: number;
  number: string;
  customer_name: string;
  status: string;
  issue_date: string;
  due_date?: string | null;
  currency: string;
  total: number;
  items: InvoiceItem[];
  files?: { name: string; url: string }[];
};

export default function InvoicesPage() {
  const [token, setToken] = useState("");
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [open, setOpen] = useState(false);
  const [number, setNumber] = useState("");
  const [customer, setCustomer] = useState("");
  const [issueDate, setIssueDate] = useState<string>(new Date().toISOString().slice(0,10));
  const [items, setItems] = useState<InvoiceItem[]>([{ description: "", quantity: 1, unit_price: 0 }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const [uploads, setUploads] = useState<{ name: string; url: string }[]>([]);

  function pushToast(kind: ToastItem["kind"], message: string) {
    const id = Date.now() + Math.random();
    setToasts((t) => [...t, { id, kind, message }]);
    setTimeout(() => setToasts((t) => t.filter(x => x.id !== id)), 4000);
  }

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
    if (data.access_token) {
      setToken(data.access_token);
      try { localStorage.setItem("token", data.access_token); } catch {}
    }
    else setError("Login failed");
  }

  async function loadInvoices() {
    if (!token) return;
    setLoading(true);
    setError(null);
    const res = await fetch(`${API_BASE}/accounting/invoices`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      setError("Failed to fetch invoices");
      setLoading(false);
      return;
    }
    const data = await res.json();
    setInvoices(data);
    setLoading(false);
  }

  async function createInvoice() {
    setError(null);
    const payload = {
      number,
      customer_name: customer,
      issue_date: issueDate,
      currency: "USD",
      items: items.map(i => ({ description: i.description, quantity: i.quantity, unit_price: i.unit_price }))
    };
    // optimistic local insertion
    const tempId = -Math.floor(Math.random()*1000000);
    const optimistic: Invoice = { id: tempId, number, customer_name: customer, issue_date: issueDate, due_date: null, currency: "USD", status: "draft", total: totalNew, items: items, files: uploads };
    setInvoices(prev => [optimistic, ...prev]);
    const res = await fetch(`${API_BASE}/accounting/invoices`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const t = await res.text();
      setError(`Create failed: ${t}`);
      // rollback optimistic
      setInvoices(prev => prev.filter(x => x.id !== tempId));
      pushToast("error", "Failed to create invoice");
      return;
    }
    pushToast("success", "Invoice created");
    setOpen(false);
    setNumber("");
    setCustomer("");
    setItems([{ description: "", quantity: 1, unit_price: 0 }]);
    setUploads([]);
    loadInvoices();
  }

  async function recordPayment(id: number, amount: number) {
    setError(null);
    // optimistic: mark as paid in UI
    const before = invoices;
    setInvoices(prev => prev.map(x => x.id === id ? { ...x, status: "paid" } : x));
    const res = await fetch(`${API_BASE}/accounting/invoices/${id}/payments`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ amount }),
    });
    if (!res.ok) {
      const t = await res.text();
      setError(`Payment failed: ${t}`);
      setInvoices(before);
      pushToast("error", "Payment failed");
      return;
    }
    pushToast("success", "Payment recorded");
    loadInvoices();
  }

  useEffect(() => { if (token) loadInvoices(); }, [token]);

  const totalNew = useMemo(() => items.reduce((sum, it) => sum + (it.quantity || 0) * (it.unit_price || 0), 0), [items]);

  return (
    <main style={{ padding: 24, maxWidth: 1000, margin: "0 auto" }}>
      <h1>Invoices</h1>
      {!token ? (
        <button onClick={login}>Login</button>
      ) : (
        <>
          <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12 }}>
            <button onClick={() => setOpen(true)}>Create Invoice</button>
            <button onClick={loadInvoices} disabled={loading}>{loading ? "Loading..." : "Refresh"}</button>
            {error && <span style={{ color: "crimson" }}>{error}</span>}
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th align="left">Number</th>
                <th align="left">Customer</th>
                <th align="right">Total</th>
                <th align="left">Status</th>
                <th align="left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv) => (
                <React.Fragment key={inv.id}>
                  <tr style={{ borderTop: "1px solid #eee" }}>
                    <td>{inv.number}</td>
                    <td>{inv.customer_name}</td>
                    <td align="right">{inv.total.toFixed(2)} {inv.currency}</td>
                    <td>{inv.status}</td>
                    <td>
                      <button onClick={() => recordPayment(inv.id, inv.total)}>Pay</button>
                    </td>
                  </tr>
                  {inv.files && inv.files.length > 0 && (
                    <tr>
                      <td colSpan={5}>
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                          {inv.files.map((f: { name: string; url: string }) => (
                            <a key={f.url} href={f.url} target="_blank" rel="noreferrer">{f.name}</a>
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
              {invoices.length === 0 && (
                <tr><td colSpan={5}>No invoices</td></tr>
              )}
            </tbody>
          </table>

          {open && (
            <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)" }} onClick={() => setOpen(false)}>
              <div onClick={e => e.stopPropagation()} style={{ position: "absolute", right: 0, top: 0, width: 420, height: "100%", background: "#fff", padding: 16, overflow: "auto" }}>
                <h3>Create Invoice</h3>
                <label>Number<br /><input value={number} onChange={e => setNumber(e.target.value)} placeholder="INV-1003" /></label>
                <br />
                <label>Customer<br /><input value={customer} onChange={e => setCustomer(e.target.value)} placeholder="Acme Co" /></label>
                <br />
                <label>Issue Date<br /><input type="date" value={issueDate} onChange={e => setIssueDate(e.target.value)} /></label>
                <br />
                <h4>Items</h4>
                {items.map((it, idx) => (
                  <div key={idx} style={{ display: "grid", gridTemplateColumns: "1fr 100px 120px", gap: 8, marginBottom: 8 }}>
                    <input placeholder="Description" value={it.description} onChange={e => {
                      const arr = [...items]; arr[idx].description = e.target.value; setItems(arr);
                    }} />
                    <input type="number" step="0.01" placeholder="Qty" value={it.quantity} onChange={e => {
                      const arr = [...items]; arr[idx].quantity = parseFloat(e.target.value || "0"); setItems(arr);
                    }} />
                    <input type="number" step="0.01" placeholder="Unit $" value={it.unit_price} onChange={e => {
                      const arr = [...items]; arr[idx].unit_price = parseFloat(e.target.value || "0"); setItems(arr);
                    }} />
                  </div>
                ))}
                <button onClick={() => setItems([...items, { description: "", quantity: 1, unit_price: 0 }])}>+ Add item</button>
                <h4 style={{ marginTop: 12 }}>Attachments</h4>
                <input type="file" onChange={async (e) => {
                  const f = e.target.files?.[0];
                  if (!f) return;
                  try {
                    const form = new FormData();
                    form.append("file", f);
                    const res = await fetch(`${API_BASE}/files`, {
                      method: "POST",
                      headers: { Authorization: `Bearer ${token}` },
                      body: form,
                    });
                    if (!res.ok) throw new Error(await res.text());
                    const data = await res.json();
                    setUploads(prev => [...prev, { name: data.name, url: data.url }]);
                    pushToast("success", `Uploaded ${data.name}`);
                  } catch (err) {
                    pushToast("error", "Upload failed");
                  }
                }} />
                <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }}>
                  {uploads.map(u => (
                    <a key={u.url} href={u.url} target="_blank" rel="noreferrer">{u.name}</a>
                  ))}
                </div>
                <div style={{ marginTop: 12 }}>Total: {totalNew.toFixed(2)} USD</div>
                <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
                  <button onClick={createInvoice}>Create</button>
                  <button onClick={() => setOpen(false)}>Cancel</button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
      <Toasts items={toasts} onClose={(id: number) => setToasts(t => t.filter(x => x.id !== id))} />
    </main>
  );
}
