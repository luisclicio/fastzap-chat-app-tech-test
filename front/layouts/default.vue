<script setup lang="ts">
type Room = {
  id: number;
  name: string;
};

const { user, isLoggedIn, accessToken, logout } = useAuth();

if (!isLoggedIn.value) {
  navigateTo('/login');
}

const config = useRuntimeConfig();
const route = useRoute();

const roomId = computed(() => parseInt(String(route.params?.id)));
const routePath = computed(() => route.path);
const userIsAdmin = computed(() => user.value?.is_staff);

const { data } = await useFetch<Room[]>(`${config.public.apiUrl}/api/rooms/`, {
  headers: {
    Authorization: `Bearer ${accessToken.value}`,
  },
  watch: [routePath],
});
</script>

<template>
  <div>
    <!-- Top Bar -->
    <div class="fixed top-0 inset-x-0 z-20 px-4 lg:hidden">
      <div class="flex items-center gap-3 py-2">
        <!-- Navigation Toggle -->
        <button
          type="button"
          class="size-8 flex justify-center items-center gap-x-2 border bg-white border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-hidden focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none"
          aria-haspopup="dialog"
          aria-expanded="false"
          aria-controls="hs-application-sidebar"
          aria-label="Toggle navigation"
          data-hs-overlay="#hs-application-sidebar"
        >
          <span class="sr-only">Toggle Navigation</span>
          <svg
            class="shrink-0 size-4"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect width="18" height="18" x="3" y="3" rx="2" />
            <path d="M15 3v18" />
            <path d="m8 9 3 3-3 3" />
          </svg>
        </button>
        <!-- End Navigation Toggle -->
      </div>
    </div>
    <!-- End Top Bar -->

    <!-- Sidebar -->
    <div
      id="hs-application-sidebar"
      class="hs-overlay [--auto-close:lg] hs-overlay-open:translate-x-0 -translate-x-full transition-all duration-300 transform w-65 h-full hidden fixed inset-y-0 start-0 z-60 bg-white border-e border-gray-200 lg:block lg:translate-x-0 lg:end-auto lg:bottom-0"
      role="dialog"
      tabindex="-1"
      aria-label="Sidebar"
    >
      <div class="relative flex flex-col h-full max-h-full">
        <div class="px-4 pt-4 flex items-center justify-between">
          <div class="space-y-0.5">
            <!-- Logo -->
            <NextLink
              to="/"
              class="flex-none rounded-xl text-xl inline-block font-semibold focus:outline-hidden focus:opacity-80"
            >
              FastChat
            </NextLink>
            <!-- End Logo -->
            <p class="text-gray-500 text-sm">Olá, {{ user?.username }}!</p>
          </div>

          <div class="flex items-center gap-x-2">
            <!-- Logout button -->
            <button
              type="button"
              class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-red-500 rounded-lg focus:outline-hidden focus:text-red-500 disabled:opacity-50 disabled:pointer-events-none"
              @click="logout"
            >
              <span class="sr-only">Logout</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="shrink-0 size-4"
              >
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" x2="9" y1="12" y2="12" />
              </svg>
            </button>
            <!-- End Logout button -->

            <!-- New Room -->
            <NuxtLink
              v-if="userIsAdmin"
              to="/room/new"
              class="size-8 flex justify-center items-center gap-x-2 border border-gray-200 text-gray-800 hover:text-gray-500 rounded-lg focus:outline-hidden focus:text-gray-500 disabled:opacity-50 disabled:pointer-events-none"
            >
              <span class="sr-only">Toggle new room</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="shrink-0 size-4"
              >
                <path d="M5 12h14" />
                <path d="M12 5v14" />
              </svg>
            </NuxtLink>
            <!-- End New Room -->
          </div>
        </div>

        <!-- Content -->
        <div
          class="h-full overflow-y-auto [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:bg-gray-300"
        >
          <nav
            class="hs-accordion-group p-3 w-full flex flex-col flex-wrap"
            data-hs-accordion-always-open
          >
            <ul class="flex flex-col space-y-1">
              <li v-for="room in data" :key="room.id">
                <NuxtLink
                  :to="`/room/${room.id}`"
                  :class="`flex items-center gap-x-3.5 py-2 px-2.5 text-sm text-gray-800 rounded-lg hover:bg-gray-100 focus:outline-hidden focus:bg-gray-100 ${
                    room.id === roomId ? 'bg-gray-100' : ''
                  }`"
                >
                  {{ room.name }}
                </NuxtLink>
              </li>
            </ul>
          </nav>
        </div>
        <!-- End Content -->
      </div>
    </div>
    <!-- End Sidebar -->

    <div class="w-full lg:pl-65">
      <slot />
    </div>
  </div>
</template>
