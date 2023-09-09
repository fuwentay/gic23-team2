import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Grid } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import Message from '../Messages'

function ChatUI() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);


  useEffect(() => {
    fetchMessages();
  }, []);

  function fetchMessages() {
    fetch('http://0.0.0.0:9000/chatbot/getAllMessages')
      .then(response => response.json())
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching messages:', error));
  }

  function handleSend() {
    if (input.trim() !== '') {
      console.log(input);
      const newMessage = {
        text: input,
        sender: 'user',
      };

      fetch('http://0.0.0.0:9000/chatbot/insertMessages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newMessage),
      })
        .then(response => response.json())
        .then(data => {
          fetchMessages();
          setInput('');
        })
        .catch(error => console.error('Error sending message:', error));
    }
  }

  function handleInputChange(event) {
    setInput(event.target.value);
  }
  

  return (
    <Box
      sx={{
        height: '50vh',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'grey.200',
      }}
    >
      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
      </Box>
      <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
        <Grid container spacing={2}>
          <Grid item xs={10}>
            <TextField
              size="medium"
              fullWidth
              placeholder="Type a message"
              variant="outlined"
              value={input}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={2}>
            <Button
              fullWidth
              color="primary"
              variant="contained"
              endIcon={<SendIcon />}
              onClick={handleSend}
            >
              Send
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}

export default ChatUI;
