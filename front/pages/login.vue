<script setup lang="ts">
definePageMeta({
  layout: false,
});

const { isLoggedIn, login } = useAuth();

if (isLoggedIn.value) {
  navigateTo('/');
}

const username = ref('');
const password = ref('');

const handleSubmit = async (e: Event) => {
  e.preventDefault();

  const loginSuccess = await login({
    username: username.value,
    password: password.value,
  });

  if (loginSuccess) {
    navigateTo('/');
  } else {
    alert('Erro ao fazer login. Verifique suas credenciais.');
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 p-4">
    <div
      class="bg-white border border-gray-200 rounded-xl shadow-2xs w-full md:max-w-md"
    >
      <div class="p-4 sm:p-7">
        <div class="text-center">
          <h1 class="block text-2xl font-bold text-gray-800">Entrar</h1>
          <p class="mt-2 text-sm text-gray-600">
            Informe suas credenciais para acessar sua conta.
          </p>
        </div>

        <div class="mt-5">
          <!-- Form -->
          <form class="space-y-4" @submit="handleSubmit">
            <div class="grid gap-y-4">
              <!-- Form Group -->
              <div>
                <label for="username" class="block text-sm mb-1">
                  Nome de usuário
                </label>
                <div class="relative">
                  <input
                    type="text"
                    id="username"
                    name="username"
                    class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                    required
                    aria-describedby="email-error"
                    v-model="username"
                  />
                </div>
              </div>
              <!-- End Form Group -->

              <!-- Form Group -->
              <div>
                <label for="password" class="block text-sm mb-1"> Senha </label>
                <div class="relative">
                  <input
                    type="password"
                    id="password"
                    name="password"
                    class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                    required
                    aria-describedby="email-error"
                    v-model="password"
                  />
                </div>
              </div>
              <!-- End Form Group -->

              <button
                type="submit"
                class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-hidden focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
              >
                Entrar
              </button>
            </div>
          </form>
          <!-- End Form -->
        </div>
      </div>
    </div>
  </div>
</template>
