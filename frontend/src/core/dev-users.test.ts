import { beforeEach, describe, expect, it } from 'vitest';

import { DEV_USERS, getDevUser, setDevUser } from '@core/dev-users';

describe('dev-users', () => {
  beforeEach(() => localStorage.clear());

  it('starts as the admin user', () => {
    expect(getDevUser().id).toBe('dev-user');
  });

  it('remembers the chosen user', () => {
    setDevUser('dev-viewer');
    expect(getDevUser()).toEqual(DEV_USERS[0]);
  });

  it('falls back to the admin when the stored id is unknown', () => {
    localStorage.setItem('cloud-wise-dev-user', 'nobody');
    expect(getDevUser().id).toBe('dev-user');
  });
});
