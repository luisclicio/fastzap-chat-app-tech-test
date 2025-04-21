import { ref, nextTick, onMounted } from 'vue';

export function useScrollElement() {
  const scrollContainer = ref<HTMLElement | null>(null);

  const scrollToBottom = async () => {
    if (scrollContainer.value) {
      await nextTick();
      scrollContainer.value.scrollTo({
        top: scrollContainer.value.scrollHeight,
        behavior: 'smooth',
      });
    }
  };

  onMounted(() => {
    scrollToBottom();
  });

  return {
    scrollContainer,
    scrollToBottom,
  };
}
