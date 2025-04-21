<script setup lang="ts">
type Message = {
  id: number;
  type: string;
  author: {
    id: number;
    username: string;
  };
  content: string;
  created_at: string;
};

const config = useRuntimeConfig();
const route = useRoute();
const { accessToken, user } = useAuth();
const { scrollContainer, scrollToBottom } = useScrollElement();

const roomId = computed(() => route.params?.id);
const token = ref(accessToken.value);
const newMessages = ref<Message[]>([]);
const newMessage = ref('');
const onlineMembers = ref<string[]>([]);

const { data: oldMessages } = await useFetch<Message[]>(
  `${config.public.apiUrl}/api/rooms/${roomId.value}/messages`,
  {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  }
);

const { send } = useWebSocket(
  `${config.public.apiUrl.replace('http', 'ws')}/ws/rooms/${
    route.params?.id
  }/?token=${token.value}`,
  {
    autoReconnect: {
      retries: 5,
      delay: 5000,
      onFailed() {
        console.error('Failed to connect WebSocket after retries');
      },
    },
    onMessage(ws, event) {
      const data = JSON.parse(event.data);

      if (data.type === 'user_not_member') {
        navigateTo('/');
      } else if (data.type === 'chat_message') {
        newMessages.value.push(data as Message);
        scrollToBottom();
      } else if (data.type === 'update_members') {
        onlineMembers.value = data.members;
      }
    },
  }
);

const sendMessage = () => {
  if (newMessage.value.trim() === '') return;

  const data = {
    message: newMessage.value,
  };

  send(JSON.stringify(data));
  newMessage.value = '';
};
</script>

<template>
  <div class="relative h-dvh bg-gray-50">
    <div
      ref="scrollContainer"
      class="absolute inset-x-0 h-full p-4 pb-28 overflow-y-auto space-y-4"
    >
      <div
        v-for="message in [...(oldMessages || []), ...newMessages]"
        :key="message.id"
        :class="`w-full max-w-lg mx-auto`"
      >
        <div
          :class="`px-4 py-2 rounded-lg ${
            message?.author?.id === user?.id
              ? 'bg-blue-100 ml-40'
              : 'bg-gray-100 mr-40'
          }`"
        >
          <p>
            <strong>{{ message.author?.username }}</strong>
          </p>
          <p>{{ message.content }}</p>
          <p class="text-sm text-gray-500">
            {{ new Date(message.created_at).toLocaleString() }}
          </p>
        </div>
      </div>
    </div>

    <div class="absolute bottom-0 left-0 right-0 p-2 bg-gray-50">
      <div
        class="w-full max-w-xl mx-auto bg-white p-4 pb-2 space-y-2 rounded-xl shadow-md"
      >
        <form class="flex gap-2" @submit.prevent="sendMessage">
          <input
            type="text"
            placeholder="Digite sua mensagem..."
            class="border border-gray-300 rounded-lg p-2 w-full"
            v-model="newMessage"
          />
          <button
            type="submit"
            class="bg-blue-500 text-white rounded-lg p-2 disabled:opacity-50"
            :disabled="!newMessage"
          >
            Enviar
          </button>
        </form>

        <div>
          <button
            class="block text-sm font-semibold text-green-500 text-center mx-auto p-0.5 focus:outline-hidden"
            aria-haspopup="dialog"
            aria-expanded="false"
            aria-controls="hs-members-modal"
            data-hs-overlay="#hs-members-modal"
          >
            {{ onlineMembers.length }} membro(s) online
          </button>

          <div
            id="hs-members-modal"
            class="hs-overlay hidden size-full fixed top-0 start-0 z-80 overflow-x-hidden overflow-y-auto pointer-events-none"
            role="dialog"
            tabindex="-1"
            aria-labelledby="hs-members-modal-label"
          >
            <div
              class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 h-[calc(100%-56px)] sm:mx-auto"
            >
              <div
                class="max-h-full overflow-hidden flex flex-col bg-white border border-gray-200 shadow-2xs rounded-xl pointer-events-auto"
              >
                <div
                  class="flex justify-between items-center py-3 px-4 border-b border-gray-200"
                >
                  <h3 class="font-bold text-gray-800">
                    {{ onlineMembers.length }} membro(s) online
                  </h3>
                  <button
                    type="button"
                    class="size-8 inline-flex justify-center items-center gap-x-2 rounded-full border border-transparent bg-gray-100 text-gray-800 hover:bg-gray-200 focus:outline-hidden focus:bg-gray-200 disabled:opacity-50 disabled:pointer-events-none"
                    aria-label="Close"
                    data-hs-overlay="#hs-members-modal"
                  >
                    <span class="sr-only">Close</span>
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
                      <path d="M18 6 6 18"></path>
                      <path d="m6 6 12 12"></path>
                    </svg>
                  </button>
                </div>

                <div class="p-4 overflow-y-auto">
                  <div class="space-y-4">
                    <ul
                      v-if="onlineMembers.length > 0"
                      class="divide-y divide-gray-200"
                    >
                      <li
                        v-for="member in onlineMembers"
                        :key="member"
                        class="flex items-center justify-between py-2"
                      >
                        <span class="text-gray-800 font-semibold">
                          {{ member }}
                        </span>
                      </li>
                    </ul>

                    <p
                      v-if="onlineMembers.length === 0"
                      class="text-center text-gray-500"
                    >
                      Nenhum membro online
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
