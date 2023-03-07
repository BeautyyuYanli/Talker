<script setup>
import { ref } from 'vue'
defineProps(['status'])
const emit = defineEmits(['send_msg'])
const text = ref(null)
const send = () => {
  if (text.value.value) {
    emit('send_msg', text.value.value)
    text.value.value = ''
  }
}
const keydown = (e) => {
  if (e.key === 'Enter') {
    send()
  }
}
</script>
<template>
  <div id="bottom">
    <div>
      <input class="input" ref="text" @keypress="keydown" v-if="status == 'stopped'" />
      <p class="input" v-if="status != 'stopped'">pending...</p>
      <button @click="send">Send</button>
    </div>
  </div>
</template>
<style scoped>
#bottom {
  width: 100%;
  margin: 1rem 0;
}

#bottom > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

#bottom > div > .input {
  width: 100%;
}

#bottom > div > p {
  text-align: center;
}
</style>
