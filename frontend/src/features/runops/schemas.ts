import * as v from 'valibot';

export const provisionFormSchema = v.object({
  template_id: v.pipe(v.string(), v.minLength(1, 'Template is required')),
  resource_name: v.pipe(v.string(), v.minLength(1, 'Resource name is required')),
  environment: v.pipe(v.string(), v.minLength(1, 'Environment is required')),
  location: v.pipe(v.string(), v.minLength(1, 'Location is required')),
});

export type ProvisionFormValues = v.InferOutput<typeof provisionFormSchema>;
