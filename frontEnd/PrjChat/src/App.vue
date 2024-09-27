<template>
  <div class="chat-container">
    <div class="chat-messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message-bubble"
        :class="{ 'sent': msg.sent, 'received': !msg.sent }"
      >
        {{ msg.text }}
      </div>
    </div>
    <div class="chat-input">
      <input
        type="text"
        v-model="currentMessage"
        @keyup.enter="sendMessage"
        placeholder="Type your message here..."
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import qs from 'qs'; // 引入qs库来序列化表单数据

const currentMessage = ref(''); // 当前输入的消息
const messages = reactive([]); // 消息历史记录，包含发送和接收的消息

// 发送消息的函数
async function sendMessage() {
  if (currentMessage.value.trim() === '') return; // 如果消息为空，则不发送

  try {
    const formData = qs.stringify({
      message: currentMessage.value,
    });

    // 发送POST请求到服务器（这里仅为示例，具体URL和逻辑需根据实际情况调整）
    const response = await axios.post('http://127.0.0.1:8000/q', {query: formData}, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    // 假设服务器成功响应，并返回相同的消息内容
    const sentMessage = { text: currentMessage.value, sent: true }; // 用户发送的消息
    messages.push(sentMessage);

    // 模拟服务器返回的消息（实际应用中应根据服务器实际返回的数据进行处理）
    const receivedMessage = { text: response.data, sent: false }; // 从服务器接收的消息
    messages.push(receivedMessage);

    currentMessage.value = ''; // 清空输入框
  } catch (error) {
    // 错误处理，将错误信息作为接收到的消息显示（实际应用中可能需要更详细的错误处理）
    const errorMessage = { text: 'Error sending message: ' + error.message, sent: false };
    messages.push(errorMessage);
  }
}
</script>

<style scoped>
.chat-container {
  width: 1080px; /* 根据需要调整宽度 */
  border: 1px solid #ccc;
  padding: 10px;
  margin: 0 auto; /* 水平居中 */
  font-family: Arial, sans-serif;
}

.chat-messages {
  height: 500px; /* 根据需要调整高度 */
  overflow-y: auto; /* 滚动条 */
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #eee;
}

.message-bubble {
  padding: 8px;
  border-radius: 8px;
  margin-bottom: 10px;
  max-width: 70%; /* 限制消息气泡的最大宽度 */
}

.sent {
  background-color: #e0e0e0; /* 用户发送的消息气泡背景色 */
  margin-left: auto; /* 右对齐 */
  text-align: right; /* 文本右对齐 */
}

.received {
  background-color: #90ee90; /* 从服务器接收的消息气泡背景色 */
  margin-right: auto; /* 左对齐 */
}

.chat-input {
  display: flex;
}

.chat-input input {
  flex: 1; /* 占据所有可用空间 */
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px; /* 与按钮之间的间距 */
}

.chat-input button {
  padding: 5px 10px;
  background-color: #0975e9;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>