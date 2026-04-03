export const mockJiraTelemetry = [
  {
    platform: "Electric Vehicle Platform A",
    requirements: {
      unresolvedDependencies: 2,
      missingAcceptanceCriteria: 1,
      ageWithoutApproval: 16,
    },
    design: {
      lackSecuritySignoffs: true,
      stalledHSITickets: 3,
    },
    development: {
      velocityDrop: 20,
      prChurn: 15,
    },
    integration: {
      ciCdFailureRate: 25,
      unresolvedMergeConflicts: 4,
      delayedSupplierDrops: 2,
    },
    test: {
      defectEscapeRate: 30,
      unresolvedCriticalBugs: 5,
      failedTestCoverage: 20,
    },
    activeSprints: [
      { velocity: 80 },
      { velocity: 75 },
      { velocity: 60 },
    ],
    blockedDependencies: [
      { age: 16 },
      { age: 10 },
    ],
    ciCdFailures: [
      { rate: 25 },
    ],
    openDefects: [
      { severity: 'critical', age: 8 },
      { severity: 'blocker', age: 5 },
    ],
    riskHistory: [
      { date: '2024-03-15', req: 20, design: 30, dev: 25, integration: 35, test: 40 },
      { date: '2024-03-16', req: 22, design: 32, dev: 27, integration: 37, test: 42 },
      { date: '2024-03-17', req: 25, design: 35, dev: 30, integration: 40, test: 45 },
      { date: '2024-03-18', req: 28, design: 38, dev: 33, integration: 43, test: 48 },
      { date: '2024-03-19', req: 30, design: 40, dev: 35, integration: 45, test: 50 },
      { date: '2024-03-20', req: 32, design: 42, dev: 37, integration: 47, test: 52 },
      { date: '2024-03-21', req: 35, design: 45, dev: 40, integration: 50, test: 55 },
      { date: '2024-03-22', req: 38, design: 48, dev: 43, integration: 53, test: 58 },
      { date: '2024-03-23', req: 40, design: 50, dev: 45, integration: 55, test: 60 },
      { date: '2024-03-24', req: 42, design: 52, dev: 47, integration: 57, test: 62 },
    ],
  },
  {
    platform: "Autonomous Driving Platform B",
    requirements: {
      unresolvedDependencies: 0,
      missingAcceptanceCriteria: 0,
      ageWithoutApproval: 10,
    },
    design: {
      lackSecuritySignoffs: false,
      stalledHSITickets: 1,
    },
    development: {
      velocityDrop: 5,
      prChurn: 8,
    },
    integration: {
      ciCdFailureRate: 10,
      unresolvedMergeConflicts: 1,
      delayedSupplierDrops: 0,
    },
    test: {
      defectEscapeRate: 15,
      unresolvedCriticalBugs: 2,
      failedTestCoverage: 5,
    },
    activeSprints: [
      { velocity: 90 },
      { velocity: 85 },
      { velocity: 88 },
    ],
    blockedDependencies: [],
    ciCdFailures: [
      { rate: 10 },
    ],
    openDefects: [
      { severity: 'major', age: 3 },
    ],
    riskHistory: [
      { date: '2024-03-15', req: 5, design: 10, dev: 8, integration: 12, test: 15 },
      { date: '2024-03-16', req: 6, design: 11, dev: 9, integration: 13, test: 16 },
      { date: '2024-03-17', req: 7, design: 12, dev: 10, integration: 14, test: 17 },
      { date: '2024-03-18', req: 8, design: 13, dev: 11, integration: 15, test: 18 },
      { date: '2024-03-19', req: 9, design: 14, dev: 12, integration: 16, test: 19 },
      { date: '2024-03-20', req: 10, design: 15, dev: 13, integration: 17, test: 20 },
      { date: '2024-03-21', req: 11, design: 16, dev: 14, integration: 18, test: 21 },
      { date: '2024-03-22', req: 12, design: 17, dev: 15, integration: 19, test: 22 },
      { date: '2024-03-23', req: 13, design: 18, dev: 16, integration: 20, test: 23 },
      { date: '2024-03-24', req: 14, design: 19, dev: 17, integration: 21, test: 24 },
    ],
  },
  {
    platform: "Hybrid Platform C",
    requirements: {
      unresolvedDependencies: 3,
      missingAcceptanceCriteria: 2,
      ageWithoutApproval: 20,
    },
    design: {
      lackSecuritySignoffs: true,
      stalledHSITickets: 5,
    },
    development: {
      velocityDrop: 25,
      prChurn: 20,
    },
    integration: {
      ciCdFailureRate: 35,
      unresolvedMergeConflicts: 6,
      delayedSupplierDrops: 3,
    },
    test: {
      defectEscapeRate: 40,
      unresolvedCriticalBugs: 8,
      failedTestCoverage: 30,
    },
    activeSprints: [
      { velocity: 70 },
      { velocity: 65 },
      { velocity: 50 },
    ],
    blockedDependencies: [
      { age: 20 },
      { age: 15 },
      { age: 12 },
    ],
    ciCdFailures: [
      { rate: 35 },
    ],
    openDefects: [
      { severity: 'critical', age: 10 },
      { severity: 'blocker', age: 7 },
      { severity: 'critical', age: 6 },
    ],
    riskHistory: [
      { date: '2024-03-15', req: 45, design: 55, dev: 50, integration: 60, test: 65 },
      { date: '2024-03-16', req: 47, design: 57, dev: 52, integration: 62, test: 67 },
      { date: '2024-03-17', req: 49, design: 59, dev: 54, integration: 64, test: 69 },
      { date: '2024-03-18', req: 51, design: 61, dev: 56, integration: 66, test: 71 },
      { date: '2024-03-19', req: 53, design: 63, dev: 58, integration: 68, test: 73 },
      { date: '2024-03-20', req: 55, design: 65, dev: 60, integration: 70, test: 75 },
      { date: '2024-03-21', req: 57, design: 67, dev: 62, integration: 72, test: 77 },
      { date: '2024-03-22', req: 59, design: 69, dev: 64, integration: 74, test: 79 },
      { date: '2024-03-23', req: 61, design: 71, dev: 66, integration: 76, test: 81 },
      { date: '2024-03-24', req: 63, design: 73, dev: 68, integration: 78, test: 83 },
    ],
  },
  {
    platform: "Commercial Vehicle Platform D",
    requirements: {
      unresolvedDependencies: 1,
      missingAcceptanceCriteria: 0,
      ageWithoutApproval: 12,
    },
    design: {
      lackSecuritySignoffs: false,
      stalledHSITickets: 0,
    },
    development: {
      velocityDrop: 10,
      prChurn: 12,
    },
    integration: {
      ciCdFailureRate: 15,
      unresolvedMergeConflicts: 2,
      delayedSupplierDrops: 1,
    },
    test: {
      defectEscapeRate: 20,
      unresolvedCriticalBugs: 3,
      failedTestCoverage: 10,
    },
    activeSprints: [
      { velocity: 85 },
      { velocity: 80 },
      { velocity: 82 },
    ],
    blockedDependencies: [
      { age: 12 },
    ],
    ciCdFailures: [
      { rate: 15 },
    ],
    openDefects: [
      { severity: 'major', age: 4 },
      { severity: 'critical', age: 2 },
    ],
    riskHistory: [
      { date: '2024-03-15', req: 15, design: 20, dev: 18, integration: 22, test: 25 },
      { date: '2024-03-16', req: 16, design: 21, dev: 19, integration: 23, test: 26 },
      { date: '2024-03-17', req: 17, design: 22, dev: 20, integration: 24, test: 27 },
      { date: '2024-03-18', req: 18, design: 23, dev: 21, integration: 25, test: 28 },
      { date: '2024-03-19', req: 19, design: 24, dev: 22, integration: 26, test: 29 },
      { date: '2024-03-20', req: 20, design: 25, dev: 23, integration: 27, test: 30 },
      { date: '2024-03-21', req: 21, design: 26, dev: 24, integration: 28, test: 31 },
      { date: '2024-03-22', req: 22, design: 27, dev: 25, integration: 29, test: 32 },
      { date: '2024-03-23', req: 23, design: 28, dev: 26, integration: 30, test: 33 },
      { date: '2024-03-24', req: 24, design: 29, dev: 27, integration: 31, test: 34 },
    ],
  },
  {
    platform: "Luxury Sedan Platform E",
    requirements: {
      unresolvedDependencies: 4,
      missingAcceptanceCriteria: 3,
      ageWithoutApproval: 25,
    },
    design: {
      lackSecuritySignoffs: true,
      stalledHSITickets: 7,
    },
    development: {
      velocityDrop: 30,
      prChurn: 25,
    },
    integration: {
      ciCdFailureRate: 45,
      unresolvedMergeConflicts: 8,
      delayedSupplierDrops: 4,
    },
    test: {
      defectEscapeRate: 50,
      unresolvedCriticalBugs: 10,
      failedTestCoverage: 40,
    },
    activeSprints: [
      { velocity: 60 },
      { velocity: 55 },
      { velocity: 40 },
    ],
    blockedDependencies: [
      { age: 25 },
      { age: 18 },
      { age: 14 },
      { age: 16 },
    ],
    ciCdFailures: [
      { rate: 45 },
    ],
    openDefects: [
      { severity: 'critical', age: 12 },
      { severity: 'blocker', age: 9 },
      { severity: 'critical', age: 8 },
      { severity: 'blocker', age: 6 },
    ],
    riskHistory: [
      { date: '2024-03-15', req: 60, design: 70, dev: 65, integration: 75, test: 80 },
      { date: '2024-03-16', req: 62, design: 72, dev: 67, integration: 77, test: 82 },
      { date: '2024-03-17', req: 64, design: 74, dev: 69, integration: 79, test: 84 },
      { date: '2024-03-18', req: 66, design: 76, dev: 71, integration: 81, test: 86 },
      { date: '2024-03-19', req: 68, design: 78, dev: 73, integration: 83, test: 88 },
      { date: '2024-03-20', req: 70, design: 80, dev: 75, integration: 85, test: 90 },
      { date: '2024-03-21', req: 72, design: 82, dev: 77, integration: 87, test: 92 },
      { date: '2024-03-22', req: 74, design: 84, dev: 79, integration: 89, test: 94 },
      { date: '2024-03-23', req: 76, design: 86, dev: 81, integration: 91, test: 96 },
      { date: '2024-03-24', req: 78, design: 88, dev: 83, integration: 93, test: 98 },
    ],
  },
];