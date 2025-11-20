export interface Vendor {
    id: number;
    name: string;
  }
  
  export interface Scenario {
    id: number;
    vendor_id: number;
    name: string;
    description: string;
  }
  
  export interface Param {
    id: number;
    scenario_id: number;
    key: string;
    label: string;
    type: string;
    required: boolean;
    default_value: string;
    options?: string | null;
  }
  
  export interface GenerateRequest {
    scenario_id: number;
    params: Record<string, string>;
  }