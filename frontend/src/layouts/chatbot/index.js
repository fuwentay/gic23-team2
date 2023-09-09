import { useState } from "react";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import React from "react";
import ChatUI from "./components/ChatUI";
import SuiBox from "components/SuiBox";

function Chatbot() {
  return (
    <DashboardLayout>
      <SuiBox>
      <ChatUI/>
      </SuiBox>
    </DashboardLayout>
  );
}

export default Chatbot;
