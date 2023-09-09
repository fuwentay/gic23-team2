import * as React from "react";
import { useState } from "react";
import {
    Box,
    Typography,
    Avatar,
    Paper,
} from "@mui/material";
import SuiAvatar from "components/SuiAvatar";
import chatbot from "assets/images/chatbot-logo.png";
import user from "assets/images/user.png";

function Message({ message }) {
    const isBot = message.sender === "bot";

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: isBot ? "flex-start" : "flex-end",
                mb: 2,
            }}
        >
            <Box
                sx={{
                    display: "flex",
                    flexDirection: isBot ? "row" : "row-reverse",
                    alignItems: "center",
                }}
            >
                <Avatar>
                    {isBot ?             
                    <SuiAvatar
                    src={chatbot}
                    alt="profile-image"
                    customClass="shadow-sm"
                    /> : 
                    <SuiAvatar
                    src={user}
                    alt="profile-image"
                    customClass="shadow-sm"
                    />}
                </Avatar>
                <Paper
                    sx={{
                        p: 2,
                        ml: isBot ? 1 : 0,
                        mr: isBot ? 0 : 1,
                        backgroundColor: isBot ? "#9dd6fc" : "#ffffff",
                        borderRadius: isBot ? "20px 20px 20px 5px" : "20px 20px 5px 20px",
                    }}
                >
                    <Typography variant="body2">{message.text}</Typography>
                </Paper>
            </Box>
        </Box>
    )

}
export default Message;