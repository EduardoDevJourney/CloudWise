import * as v from 'valibot';

export const provisionFormSchema = v.object({
  template_id: v.pipe(v.string(), v.minLength(1, 'Template é obrigatório')),
  resource_name: v.pipe(v.string(), v.minLength(1, 'Nome do recurso é obrigatório')),
  environment: v.pipe(v.string(), v.minLength(1, 'Ambiente é obrigatório')),
  location: v.pipe(v.string(), v.minLength(1, 'Região é obrigatória')),
});

export type ProvisionFormValues = v.InferOutput<typeof provisionFormSchema>;
