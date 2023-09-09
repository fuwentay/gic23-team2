// @mui material components
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import { Button } from '@mui/material';
import SuiAvatar from "components/SuiAvatar";
import chatbot from "assets/images/chatbot-logo.png";
import React, { useState } from 'react';
import ChatUI from "../../chatbot/components/ChatUI";

function ChatbotButton() {
    const [isCardOpen, setCardOpen] = useState(false);

    const handleChatbotClick = () => {
        setCardOpen(prevState => !prevState);
    };
    return (
        <div>
            <SuiBox sx={{ display: 'flex', justifyContent: 'flex-end' }} >
                <Button
                    startIcon={
                        <SuiAvatar src={chatbot}
                            alt="profile-image"
                            customClass="shadow-sm sui-avatar"
                        />}
                    onClick={handleChatbotClick}
                >
                </Button>
            </SuiBox>
            {isCardOpen && (
                <SuiBox>
                    <ChatUI></ChatUI>               
                </SuiBox>
            )}
        </div>
    );
}

export default ChatbotButton;