export function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <span className="wordmark">
      <svg aria-hidden="true" viewBox="0 0 32 32" width="32" height="32">
        <path
          d="M4 25V7l12 13L28 7v18"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.6"
          strokeLinejoin="round"
        />
        <circle cx="4" cy="25" r="2.8" fill="currentColor" />
        <circle cx="28" cy="25" r="2.8" fill="currentColor" />
      </svg>
      {!compact && "MEHWAR"}
    </span>
  );
}
