export type Founder = {
  name: string;
  role: string;
  faculty: string;
  institution: string;
  location: string;
  shortInstitution: string;
  email: string;
};

// Public contact details explicitly approved in the V3 specification.
export const founders = [
  {
    name: "Muzzammil Sajid",
    role: "Co-founder — Research & Assurance",
    faculty: "Faculty of Mechanical Engineering",
    institution:
      "Ghulam Ishaq Khan Institute of Engineering Sciences and Technology",
    location: "Topi, Pakistan",
    shortInstitution: "GIKI / FME",
    email: "muzzammilsajid1@gmail.com",
  },
  {
    name: "Simra Imran",
    role: "Co-founder — Product & Integration",
    faculty: "School of Electrical Engineering and Computer Science",
    institution: "National University of Sciences and Technology",
    location: "Islamabad, Pakistan",
    shortInstitution: "NUST / SEECS",
    email: "simraimran158@gmail.com",
  },
] as const satisfies readonly Founder[];

// Historical implementation verification; never a live reliability or safety metric.
export const submissionVerification = {
  testsPassed: 137,
  testsSkipped: 0,
  ruff: "PASS",
  diffCheck: "PASS",
} as const;

export const siteConfig = {
  canonicalUrl: "https://mehwar-deftech.vercel.app",
  evidenceArchiveUrl: "",
  publicEmail: "",
  founderContacts: founders,
  demoVideo: "",
  demoCaptions: "",
  demoTranscript: "",
};

export const referenceLabel =
  "deterministic A* reliability reference under the shared grid contract";

export const workflow = [
  [
    "Controller",
    "Evaluate the verified MaskablePPO adapter in the current MVP.",
    "Verified adapter",
  ],
  [
    "Scenario runner",
    "Run a selected structured C4 scenario under the shared movement contract.",
    "Selected C4 scenario",
  ],
  [
    "Trajectory recorder",
    "Preserve the visited states and record invalid actions separately.",
    "Trajectory + diagnostics",
  ],
  [
    "Failure intelligence",
    "Record the outcome under the frozen, versioned failure semantics.",
    "c4_c5_recurrence_v1",
  ],
  [
    "Deterministic reference",
    "Provide A* task-feasibility context under the same grid contract.",
    "Reference context",
  ],
  [
    "Evidence profile",
    "Tie the observation to its controller, scenario and explicit limitations.",
    "Provenance + boundaries",
  ],
  [
    "Dashboard + report",
    "Inspect the trajectory and retain JSON and human-readable reports.",
    "Inspectable outputs",
  ],
] as const;

export const roadmap = [
  [
    "Technical-user discovery",
    "Which evidence helps an autonomy engineer make a decision?",
  ],
  [
    "External controller / autonomy-stack integration",
    "Can the workflow fit an external evaluation stack?",
  ],
  [
    "Broader structured scenario coverage",
    "Where else do the current diagnostic boundaries appear?",
  ],
  [
    "Higher-fidelity simulation / SIL",
    "Does the evidence remain useful beyond the grid abstraction?",
  ],
  [
    "Cross-fidelity evidence study",
    "Which observations transfer between controlled environments?",
  ],
  [
    "Controlled lab / HIL-style validation",
    "What can be tested under lab constraints, where feasible?",
  ],
  [
    "Pilot / design-partner specification",
    "What would a useful, bounded technical pilot need to demonstrate?",
  ],
] as const;
