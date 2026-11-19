export type ProvisionStatus = 'pending' | 'running' | 'success' | 'failed';

export type PolicyItem = {
  locations: string[];
  environments: string[];
  resource_name_pattern: string;
};

export type TemplateItem = {
  id: string;
  slug: string;
  name: string;
  params_schema: Record<string, unknown>;
  azure_sku: string;
};

export type ProvisionRequestCreate = {
  template_id: string;
  resource_name: string;
  environment: string;
  location: string;
};

export type ProvisionRequestRead = {
  id: string;
  user_id: string;
  template_id: string;
  status: ProvisionStatus;
  request_data: ProvisionRequestCreate;
  error_message: string | null;
  created_at: string;
  execution_time: string | null;
};

export type CostRecordItem = {
  id: string;
  subscription_id: string;
  cost: number;
  date: string;
  resource_type: string;
  tags: Record<string, string>;
};

export type CostSeriesDay = {
  date: string;
  total_cost: number;
  by_service: Record<string, number>;
};

export type CloudWiseDashboardResponse = {
  granularity: 'day' | 'week' | 'month';
  series: CostSeriesDay[];
  summary: {
    total_cost: number;
    top_service: string;
    subscription_count: number;
  };
};

export type FriendlyError = {
  title: string;
  detail: string | string[];
  status: number;
};
