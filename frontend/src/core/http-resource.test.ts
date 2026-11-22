import { http, HttpResponse } from 'msw';
import { beforeEach, describe, expect, it } from 'vitest';

import { setDevUser } from '@core/dev-users';
import { httpResource } from '@core/http-resource';
import { server } from '@mocks/server';

describe('httpResource', () => {
  beforeEach(() => localStorage.clear());

  it('sends the headers of the selected dev user', async () => {
    let headers: Headers | undefined;
    server.use(
      http.get('/api/v1/ping', ({ request }) => {
        headers = request.headers;
        return HttpResponse.json({});
      }),
    );
    setDevUser('dev-provisioner');

    await httpResource('/api/v1/ping');

    expect(headers?.get('X-Dev-User-Id')).toBe('dev-provisioner');
    expect(headers?.get('X-Dev-User-Email')).toBe('provisioner@dev.local');
  });
});
