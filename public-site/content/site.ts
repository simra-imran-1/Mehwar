// Historical snapshot: keep immutable when a future validated build is added.
export const submissionSnapshot = {
  title: "DEFTECH 2026 Submission Snapshot",
  date: "September 2026",
  branch: "feat/integration-demo",
  sha: "1586eebf9daa8a8e690bc6f62cc377ce540214ee",
  checkpointSha256:
    "c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf",
  verification: [
    "137 tests passed",
    "0 skipped",
    "Ruff PASS",
    "git diff --check PASS",
  ],
} as const;

export const siteConfig: {
  snapshotUrl: string;
  contactMailto: string;
  demoVideo: string;
  latestValidatedBuild: null;
} = {
  snapshotUrl: "", // Approved public Drive URL; empty falls back to #snapshot.
  contactMailto: "", // Set to mailto:TEAM_APPROVED_PUBLIC_EMAIL once approved.
  demoVideo: "", // Set to a public local asset such as /mehwar-demo.mp4 to enable.
  latestValidatedBuild: null, // Future content stays separate from submissionSnapshot.
};

export const referenceLabel =
  "deterministic A* reliability reference under the shared grid contract";
