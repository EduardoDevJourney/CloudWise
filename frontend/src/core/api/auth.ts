import { defineApiRoute, defineApiRouteFn, httpResource } from '@core/http-resource';
import type { MeItem, UserItem, UserUpdate } from '@core/types/api';

const ME_ROUTE = defineApiRoute('/api/v1/me');
const USERS_ROUTE = defineApiRoute('/api/v1/users');
const userRoute = defineApiRouteFn('/api/v1/users/:id');

export function fetchMe() {
  return httpResource<MeItem>(ME_ROUTE);
}

export function fetchUsers() {
  return httpResource<UserItem[]>(USERS_ROUTE);
}

export function updateUser(id: string, payload: UserUpdate) {
  return httpResource<UserItem>(userRoute(id), {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}
