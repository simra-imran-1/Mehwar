"use client";
import { useState } from "react";
export function CopyHash({ label, value }: { label: string; value: string }) {
  const [feedback, setFeedback] = useState("");
  return (
    <div className="hash-record">
      <span>{label}</span>
      <div className="hash-actions">
        <details>
          <summary>
            <code>
              {value.slice(0, 12)}…{value.slice(-6)}
            </code>
            <span className="sr-only"> — expand full {label}</span>
            <svg aria-hidden="true" width="12" height="12" viewBox="0 0 12 12">
              <path d="M1 6h10M6 1v10" fill="none" stroke="currentColor" />
            </svg>
          </summary>
          <code className="full-hash">{value}</code>
        </details>
        <button
          type="button"
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(value);
              setFeedback("Copied");
            } catch {
              setFeedback("Expand to copy manually");
            }
          }}
        >
          Copy<span className="sr-only"> full {label}</span>
          <svg aria-hidden="true" width="12" height="12" viewBox="0 0 12 12">
            <path d="M4 2h6v7H4zM2 4v7h6" fill="none" stroke="currentColor" />
          </svg>
        </button>
      </div>
      <span className="copy-feedback" role="status">
        {feedback}
      </span>
    </div>
  );
}
