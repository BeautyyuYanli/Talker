<script setup>
import { ref } from 'vue'
import OutputBoxs from './components/OutputBoxs.vue'
import InputBottom from './components/InputBottom.vue'
let status = ref('stopped')
let msg_list = ref([])
let headers = {
  'Content-Type': 'text/plain',
  Accept: 'text/plain'
}
const model = new URLSearchParams(window.location.search).get('model')
const send_msg = (msg) => {
  msg_list.value.push('> ' + msg)
  status.value = 'sending'
  // eslint-disable-next-line no-undef
  axios
    .request({
      // baseURL: 'http://localhost:5000',
      method: 'post',
      url: '/gen_msg?model=' + model,
      headers: headers,
      data: msg
    })
    .then((res) => {
      msg_list.value.push(res.data)
      status.value = 'stopped'
    })
    .catch((err) => {
      msg_list.value.push('error: ' + String(err))
      status.value = 'stopped'
    })
}
</script>
<template>
  <OutputBoxs id="top" :value="msg_list" ref="chat" />
  <InputBottom id="bottom" @send_msg="send_msg" :status="status" />
</template>

<style scoped>
#top {
  position: absolute;
  left: 10%;
  width: 80%;
  bottom: 10%;
}

#bottom {
  position: absolute;
  width: 80%;
  left: 10%;
  bottom: 0;
}
</style>
