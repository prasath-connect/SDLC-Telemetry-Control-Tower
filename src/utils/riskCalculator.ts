export interface RequirementsData {
  unresolvedDependencies: number;
  missingAcceptanceCriteria: number;
  ageWithoutApproval: number;
}

export interface DesignData {
  lackSecuritySignoffs: boolean;
  stalledHSITickets: number;
}

export interface DevelopmentData {
  velocityDrop: number;
  prChurn: number;
}

export interface IntegrationData {
  ciCdFailureRate: number;
  unresolvedMergeConflicts: number;
  delayedSupplierDrops: number;
}

export interface TestData {
  defectEscapeRate: number;
  unresolvedCriticalBugs: number;
  failedTestCoverage: number;
}

export interface PlatformData {
  platform: string;
  requirements: RequirementsData;
  design: DesignData;
  development: DevelopmentData;
  integration: IntegrationData;
  test: TestData;
  activeSprints: { velocity: number }[];
  blockedDependencies: { age: number }[];
  ciCdFailures: { rate: number }[];
  openDefects: { severity: string; age: number }[];
  riskHistory: { date: string; req: number; design: number; dev: number; integration: number; test: number }[];
}

export function calculateReqRisk(req: RequirementsData): number {
  let risk = 0;
  risk += req.unresolvedDependencies * 15;
  risk += req.missingAcceptanceCriteria * 20;
  if (req.ageWithoutApproval > 14) {
    risk += (req.ageWithoutApproval - 14) * 3;
  }
  return Math.min(risk, 100);
}

export function calculateDesignRisk(design: DesignData): number {
  let risk = 0;
  if (design.lackSecuritySignoffs) risk += 40;
  risk += design.stalledHSITickets * 10;
  return Math.min(risk, 100);
}

export function calculateDevRisk(dev: DevelopmentData): number {
  let risk = 0;
  if (dev.velocityDrop > 15) {
    risk += dev.velocityDrop;
  }
  if (dev.prChurn > 10) {
    risk += (dev.prChurn - 10) * 2;
  }
  return Math.min(risk, 100);
}

export function calculateIntegrationRisk(integration: IntegrationData): number {
  let risk = integration.ciCdFailureRate;
  risk += integration.unresolvedMergeConflicts * 5;
  risk += integration.delayedSupplierDrops * 10;
  return Math.min(risk, 100);
}

export function calculateTestRisk(test: TestData): number {
  let risk = test.defectEscapeRate;
  risk += test.unresolvedCriticalBugs * 5;
  risk += test.failedTestCoverage;
  return Math.min(risk, 100);
}

export function calculatePhaseRisks(data: PlatformData) {
  return {
    req: calculateReqRisk(data.requirements),
    design: calculateDesignRisk(data.design),
    dev: calculateDevRisk(data.development),
    integration: calculateIntegrationRisk(data.integration),
    test: calculateTestRisk(data.test),
  };
}

export function getLeadingIndicator(phase: string, data: PlatformData[]): string {
  if (phase === 'req') {
    const totalUnresolved = data.reduce((sum, p) => sum + p.requirements.unresolvedDependencies, 0);
    const totalMissing = data.reduce((sum, p) => sum + p.requirements.missingAcceptanceCriteria, 0);
    const maxAge = Math.max(...data.map(p => p.requirements.ageWithoutApproval));
    if (totalUnresolved > totalMissing) return `Unresolved dependencies: ${totalUnresolved}`;
    if (maxAge > 14) return `Epics aged ${maxAge} days without approval`;
    return `Missing acceptance criteria: ${totalMissing}`;
  }
  if (phase === 'design') {
    const lackCount = data.filter(p => p.design.lackSecuritySignoffs).length;
    const totalStalled = data.reduce((sum, p) => sum + p.design.stalledHSITickets, 0);
    if (lackCount > 0) return `Lack of security sign-offs in ${lackCount} platforms`;
    return `Stalled HSI tickets: ${totalStalled}`;
  }
  if (phase === 'dev') {
    const maxDrop = Math.max(...data.map(p => p.development.velocityDrop));
    const maxChurn = Math.max(...data.map(p => p.development.prChurn));
    if (maxDrop > 15) return `Velocity dropped ${maxDrop}%`;
    return `High PR churn: ${maxChurn}`;
  }
  if (phase === 'integration') {
    const maxFailure = Math.max(...data.map(p => p.integration.ciCdFailureRate));
    const totalConflicts = data.reduce((sum, p) => sum + p.integration.unresolvedMergeConflicts, 0);
    const totalDelays = data.reduce((sum, p) => sum + p.integration.delayedSupplierDrops, 0);
    if (totalDelays > 0) return `Delayed supplier drops: ${totalDelays}`;
    if (totalConflicts > 0) return `Unresolved merge conflicts: ${totalConflicts}`;
    return `CI/CD failure rate: ${maxFailure}%`;
  }
  if (phase === 'test') {
    const maxEscape = Math.max(...data.map(p => p.test.defectEscapeRate));
    const totalCritical = data.reduce((sum, p) => sum + p.test.unresolvedCriticalBugs, 0);
    const maxCoverage = Math.max(...data.map(p => p.test.failedTestCoverage));
    if (totalCritical > 0) return `Unresolved critical bugs: ${totalCritical}`;
    if (maxCoverage > 20) return `Failed test coverage: ${maxCoverage}%`;
    return `Defect escape rate: ${maxEscape}%`;
  }
  return '';
}

export function getRecommendedAction(phase: string, data: PlatformData[]): string {
  if (phase === 'req') return 'Review epics for dependencies and approvals';
  if (phase === 'design') return 'Conduct security and safety sign-off reviews';
  if (phase === 'dev') return 'Analyze sprint velocity trends and PR processes';
  if (phase === 'integration') return 'Resolve supplier dependencies and CI/CD issues';
  if (phase === 'test') return 'Address critical defects and improve test coverage';
  return '';
}

export function calculateOverallMetrics(data: PlatformData[]) {
  const allRisks = data.map(calculatePhaseRisks);
  const phaseRisks = {
    req: allRisks.reduce((sum, r) => sum + r.req, 0) / data.length,
    design: allRisks.reduce((sum, r) => sum + r.design, 0) / data.length,
    dev: allRisks.reduce((sum, r) => sum + r.dev, 0) / data.length,
    integration: allRisks.reduce((sum, r) => sum + r.integration, 0) / data.length,
    test: allRisks.reduce((sum, r) => sum + r.test, 0) / data.length,
  };
  const maxRisk = Math.max(...Object.values(phaseRisks));
  let health = 'Green';
  if (maxRisk > 75) health = 'Red';
  else if (maxRisk > 50) health = 'Amber';
  const budgetAtRisk = Math.round(maxRisk * 50000); // Mock calculation
  const scheduleSlip = Math.round(maxRisk / 10); // Mock days
  return { phaseRisks, health, budgetAtRisk, scheduleSlip };
}

export function generateExecutiveSummary(data: PlatformData[]) {
  const { phaseRisks, health, scheduleSlip } = calculateOverallMetrics(data);
  const criticalPhases = Object.entries(phaseRisks).filter(([_, risk]) => risk > 75).map(([phase]) => phase);
  if (criticalPhases.length === 0) return 'All phases are within acceptable risk levels.';
  const phaseNames = criticalPhases.map(p => p.charAt(0).toUpperCase() + p.slice(1));
  return `Critical risk in ${phaseNames.join(', ')}. ${scheduleSlip}-day schedule slip predicted.`;
}

export function getRiskOverTimeData(data: PlatformData[]) {
  // Aggregate risk history across platforms
  const historyMap = new Map<string, { req: number[]; design: number[]; dev: number[]; integration: number[]; test: number[] }>();
  data.forEach(platform => {
    platform.riskHistory.forEach(entry => {
      if (!historyMap.has(entry.date)) {
        historyMap.set(entry.date, { req: [], design: [], dev: [], integration: [], test: [] });
      }
      const hist = historyMap.get(entry.date)!;
      hist.req.push(entry.req);
      hist.design.push(entry.design);
      hist.dev.push(entry.dev);
      hist.integration.push(entry.integration);
      hist.test.push(entry.test);
    });
  });
  return Array.from(historyMap.entries()).map(([date, risks]) => ({
    date,
    req: risks.req.reduce((a, b) => a + b, 0) / risks.req.length,
    design: risks.design.reduce((a, b) => a + b, 0) / risks.design.length,
    dev: risks.dev.reduce((a, b) => a + b, 0) / risks.dev.length,
    integration: risks.integration.reduce((a, b) => a + b, 0) / risks.integration.length,
    test: risks.test.reduce((a, b) => a + b, 0) / risks.test.length,
  })).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
}