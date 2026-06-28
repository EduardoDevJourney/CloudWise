import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

type SessionState = {
  locale: string;
  setLocale: (locale: string) => void;
};

export const useSessionStore = create<SessionState>()(
  persist(
    (set) => ({
      locale: 'pt-BR',
      setLocale: (locale) => set({ locale }),
    }),
    {
      name: 'cloud-wise-session',
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
