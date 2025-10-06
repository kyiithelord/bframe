"use client";
import React from "react";

export type ToastItem = { id: number; kind: "success" | "error" | "info"; message: string };

export function Toasts({ items, onClose }: { items: ToastItem[]; onClose: (id: number) => void }) {
  return (
    <div style={{ position: "fixed", right: 16, bottom: 16, display: "grid", gap: 8, zIndex: 1000 }}>
      {items.map(t => (
        <div key={t.id} style={{ minWidth: 280, color: "#111827", background: t.kind === "error" ? "#fecaca" : t.kind === "success" ? "#bbf7d0" : "#e5e7eb", border: "1px solid #e5e7eb", borderRadius: 8, padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong style={{ textTransform: "capitalize" }}>{t.kind}</strong>
            <button onClick={() => onClose(t.id)} style={{ background: "transparent", border: 0, cursor: "pointer" }}>×</button>
          </div>
          <div>{t.message}</div>
        </div>
      ))}
    </div>
  );
}
