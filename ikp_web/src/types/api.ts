export interface ValidationMessage {
  severity: 'Error' | 'Warning' | 'Info' | 'Recommendation';
  code?: string;
  message: string;
  affected_object?: string;
  recommended_action?: string;
}

export interface RuleEvaluation {
  title: string;
  status: 'PASS' | 'FAIL' | 'UNKNOWN';
  message?: string;
  remediations?: string[];
}

export interface BOQValidationResponse {
  is_valid: boolean;
  solution_id: string;
  fuzzy_matches: ValidationMessage[];
  invalid_skus: ValidationMessage[];
  messages: ValidationMessage[];
  rule_evaluations?: RuleEvaluation[];
}

export interface ReviewQueueItem {
  id: string;
  title: string;
  type: string;
  confidence: string;
  description: string;
  evidence: any[];
}

export interface ReviewQueueResponse {
  queue: ReviewQueueItem[];
}

export interface StatusResponse {
  total_objects: number;
  total_relationships: number;
  total_rules: number;
  platforms: Record<string, {
    title: string;
    skus: number;
    categories: number;
    rules: number;
  }>;
}

export interface IntegrationStatus {
  status: string;
  name: string;
}

export interface IntegrationsResponse {
  integrations: {
    llm: IntegrationStatus;
    vector_index: IntegrationStatus;
    mcp: IntegrationStatus;
}
}

export interface SearchResult {
  id: string;
  type?: string;
  title?: string;
  score: number;
  text: string;
}

export interface SolutionCandidate {
  solution_id: string;
  request_id: string;
  profile: string;
  components: string[];
  reasoning_chain: string[];
  requirements_satisfied: string[];
  rules_applied: string[];
  constraints_evaluated: string[];
  dependencies_resolved: string[];
  trade_offs: string[];
  estimated_risks: string[];
  confidence: string;
}
