import { useIntervalFn, useStorage, StorageSerializers } from '@vueuse/core';

type User = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
};

export const useAuth = () => {
  const config = useRuntimeConfig();
  const accessToken = useStorage<string | null>(
    'accessToken',
    null,
    localStorage
  );
  const refreshToken = useStorage<string | null>(
    'refreshToken',
    null,
    localStorage
  );
  const user = useStorage<User | null>('user', null, localStorage, {
    serializer: StorageSerializers.object,
  });
  const isLoggedIn = computed(() => !!refreshToken.value);

  const fetchUser = async () => {
    if (!accessToken.value) {
      throw new Error('No access token available');
    }

    try {
      const userData = await $fetch<User>(
        `${config.public.apiUrl}/api/users/profile/`,
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );

      user.value = userData;
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      logout();
    }
  };

  const login = async (credentials: { username: string; password: string }) => {
    try {
      const { access, refresh } = await $fetch<{
        access: string;
        refresh: string;
      }>(`${config.public.apiUrl}/api/auth/token/`, {
        method: 'POST',
        body: credentials,
      });

      accessToken.value = access;
      refreshToken.value = refresh;
      await fetchUser();
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      logout();
      return false;
    }
  };

  const logout = () => {
    accessToken.value = null;
    refreshToken.value = null;
    navigateTo('/login');
  };

  const refresh = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available');
    }

    try {
      const { access } = await $fetch<{
        access: string;
      }>(`${config.public.apiUrl}/api/auth/token/refresh/`, {
        method: 'POST',
        body: { refresh: refreshToken.value },
      });
      accessToken.value = access;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
    }
  };

  useIntervalFn(
    () => {
      refresh().catch((error) => {
        console.error('Error during token refresh:', error);
      });
    },
    60000 * 5, // 5 minutes
    {
      immediateCallback: true,
    }
  );

  return {
    user,
    accessToken,
    refreshToken,
    isLoggedIn,
    login,
    logout,
    refresh,
  };
};
