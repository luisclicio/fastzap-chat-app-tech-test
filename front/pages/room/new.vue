<script setup lang="ts">
import { ref } from 'vue';

type Room = {
  id: number;
  name: string;
  description: string;
  is_private: boolean;
};

const config = useRuntimeConfig();
const { accessToken } = useAuth();

const name = ref('');
const description = ref('');
const isPrivate = ref(true);

const handleSubmit = async (event: Event) => {
  event.preventDefault();

  if (name.value.trim().length < 3 || name.value.trim().length > 50) {
    alert('O nome deve ter entre 3 e 50 caracteres.');
    return;
  }

  const formData = {
    name: name.value,
    description: description.value,
    is_private: isPrivate.value,
  };

  console.log('Form Data:', formData);

  try {
    const newRoom = await $fetch<Room>(`${config.public.apiUrl}/api/rooms/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
        'Content-Type': 'application/json',
      },
      body: formData,
    });

    await navigateTo(`/room/${newRoom.id}`);
  } catch (error) {
    console.error('Error creating room:', error);
    alert('Erro ao criar sala. Tente novamente.');
  }
};
</script>

<template>
  <div>
    <div class="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
      <div class="mx-auto max-w-2xl">
        <div class="text-center">
          <h2 class="text-xl text-gray-800 font-bold sm:text-3xl">
            Criar nova sala
          </h2>
        </div>

        <div
          class="mt-5 p-4 relative z-10 bg-white border border-gray-200 rounded-xl sm:mt-10 md:p-6"
        >
          <form class="space-y-4" @submit="handleSubmit">
            <div>
              <label for="name" class="block mb-1 text-sm font-medium">
                Nome
              </label>
              <input
                type="text"
                id="name"
                name="name"
                class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                placeholder="Digite o nome da sala"
                required
                minlength="3"
                maxlength="50"
                v-model="name"
              />
            </div>

            <div>
              <label for="description" class="block mb-1 text-sm font-medium">
                Descrição
              </label>
              <div class="mt-1">
                <textarea
                  id="description"
                  name="description"
                  rows="3"
                  class="py-2.5 sm:py-3 px-4 block w-full border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none"
                  placeholder="Escreva uma descrição para a sala"
                  v-model="description"
                ></textarea>
              </div>
            </div>

            <div class="flex items-center gap-x-3">
              <label
                for="isPrivate"
                class="relative inline-block w-11 h-6 cursor-pointer"
              >
                <input
                  id="isPrivate"
                  name="isPrivate"
                  type="checkbox"
                  class="peer sr-only"
                  v-model="isPrivate"
                />
                <span
                  class="absolute inset-0 bg-gray-200 rounded-full transition-colors duration-200 ease-in-out peer-checked:bg-blue-600 peer-disabled:opacity-50 peer-disabled:pointer-events-none"
                ></span>
                <span
                  class="absolute top-1/2 start-0.5 -translate-y-1/2 size-5 bg-white rounded-full shadow-xs transition-transform duration-200 ease-in-out peer-checked:translate-x-full"
                ></span>
              </label>
              <label for="isPrivate" class="text-sm font-medium">
                Sala privada?
              </label>
            </div>

            <div class="grid">
              <button
                type="submit"
                class="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 focus:outline-hidden focus:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
              >
                Criar sala
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
