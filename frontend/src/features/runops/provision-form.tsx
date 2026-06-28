import { useForm } from '@tanstack/react-form';
import { useState } from 'react';
import * as v from 'valibot';

import { Button } from '@ui/button';
import { Input } from '@ui/input';
import { useCreateProvision } from '@features/runops/hooks';
import { provisionFormSchema, type ProvisionFormValues } from '@features/runops/schemas';

const defaultValues: ProvisionFormValues = {
  template_id: 'rg-storage',
  resource_name: '',
  environment: 'dev',
  location: 'eastus',
};

export function ProvisionForm() {
  const mutation = useCreateProvision();
  const [lastId, setLastId] = useState<string | null>(null);

  const form = useForm({
    defaultValues,
    onSubmit: async ({ value }) => {
      const parsed = v.parse(provisionFormSchema, value);
      const result = await mutation.mutateAsync(parsed);
      setLastId(result.id);
    },
  });

  return (
    <form
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
      onSubmit={(e) => {
        e.preventDefault();
        void form.handleSubmit();
      }}
    >
      <h2 className="text-lg font-semibold text-slate-900">Novo provisionamento</h2>

      <form.Field name="template_id">
        {(field) => (
          <label className="block space-y-1 text-sm">
            <span>Template</span>
            <Input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />
          </label>
        )}
      </form.Field>

      <form.Field name="resource_name">
        {(field) => (
          <label className="block space-y-1 text-sm">
            <span>Nome do recurso</span>
            <Input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />
          </label>
        )}
      </form.Field>

      <form.Field name="environment">
        {(field) => (
          <label className="block space-y-1 text-sm">
            <span>Ambiente</span>
            <Input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />
          </label>
        )}
      </form.Field>

      <form.Field name="location">
        {(field) => (
          <label className="block space-y-1 text-sm">
            <span>Região</span>
            <Input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />
          </label>
        )}
      </form.Field>

      <Button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Provisionando...' : 'Provisionar'}
      </Button>

      {lastId ? <p className="text-sm text-slate-600">Solicitação criada: {lastId}</p> : null}
      {mutation.isError ? (
        <p className="text-sm text-red-600">{(mutation.error as Error).message}</p>
      ) : null}
    </form>
  );
}
