<template>
  <div>
    <p>Message is: {{ response }}</p> <!-- 显示POST请求的响应 -->
    <input v-model="formData.message" placeholder="Type your message here" /> <!-- 绑定到formData对象的message属性 -->
    <button @click="submitMessage">Send Message</button> <!-- 点击时调用submitMessage方法 -->
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';


const formData = ref({
  message: ''
});

const response = ref(''); 

function submitMessage() {
  axios.post('http://127.0.0.1:8000/q', {query: formData.value.message},{headers:{'Content-Type': 'application/x-www-form-urlencoded'}}) // 替换YOUR_ENDPOINT_HERE为你的API端点
    .then(res => {

      response.value = res.data; 
    })
    .catch(error => {
      console.error('There was an error!', error);
      response.value = 'Error: ' + error.message; 
    });
}
</script>

<style scoped>
</style>