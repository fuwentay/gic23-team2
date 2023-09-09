// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";

// Soft UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Table from "examples/Table";

// Custom styles for the Tables
import styles from "layouts/tables/styles";

// Data
import instrumentTable from "layouts/analytics/data/instrumentTable";

import React, { useState } from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import dayjs from 'dayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';

import Box from '@mui/material/Box';


import TableComponent from "../tables/components/Table";
import detailsCard from "./components/detailsCard.js";
import ChatUI from "../chatbot/components/ChatUI";
import Button from '@mui/material';
import SuiButton from "components/SuiButton";

import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import SuiAvatar from "components/SuiAvatar";
import chatbot from "assets/images/chatbot-logo.png";


function Analytics() {
  const classes = styles();
  const { columns: prCols, rows: prRows } = instrumentTable;
  const [value, setValue] = React.useState(dayjs('year-month-day'));
  const [instrument, setInstrument] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [sector, setSector] = React.useState('');
  const [isCardOpen, setCardOpen] = useState(false);

  const handleChangeInstrument = (event) => {
    setInstrument(event.target.value);
  };

  const handleChangeCountry = (event) => {
    setCountry(event.target.value);
  };

  const handleChangeSector = (event) => {
    setSector(event.target.value);
  };

  const handleAvatarClick = () => {
    setCardOpen(prevState => !prevState);
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SuiBox py={3}>
        <SuiBox mb={3}>
          <Card>

            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <SuiTypography variant="h5" fontWeight="bold" >
                Aggregated View
              </SuiTypography>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={['DesktopDatePicker']}>
                  <DemoItem label="Start Date" sx={{ mb: "2px" }} >
                    <DesktopDatePicker defaultValue={dayjs()} />
                  </DemoItem>
                  <DemoItem label="End Date">
                    <DesktopDatePicker defaultValue={dayjs()} />
                  </DemoItem>
                </DemoContainer>
              </LocalizationProvider>
              <Box>
                <Box sx={{ minWidth: 120, display: 'flex', flexDirection: 'row' }}>
                  <FormControlLabel control={<Checkbox defaultChecked />} label="All" />
                  <FormControlLabel control={<Checkbox defaultChecked />} label="Instruments" />
                  <FormControlLabel control={<Checkbox defaultChecked />} label="Country" />
                  <FormControlLabel control={<Checkbox defaultChecked />} label="Sector" />
                </Box>
              </Box>
            </SuiBox>

            <SuiBox mb={3}>
              <TableComponent></TableComponent>
              <SuiAvatar src={chatbot}
                alt="profile-image"
                customClass="shadow-sm sui-avatar"
                floatBottomRight
                onClick={() => { handleAvatarClick }} // New onClick handler
              />
              {isCardOpen && (
                <Card>
                  <CardContent>
                    <Typography variant="body2" color="text.secondary">
                      This is the content of the new card.
                    </Typography>
                  </CardContent>
                </Card>
              )}
            </SuiBox>
            <SuiBox mb={3}>
              <TableComponent></TableComponent>
            </SuiBox>
            <SuiBox mb={3}>
              <TableComponent></TableComponent>
            </SuiBox>

            <SuiBox mb={3}>
              <Grid container spacing={3}>
                <Grid item xs={8}>
                  <Card className="h-100" style={{ paddingLeft: '10px' }}>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <detailsCard></detailsCard>
                </Grid>

              </Grid>

            </SuiBox>
          </Card>

        </SuiBox>


        <Card>
          <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
            <SuiTypography variant="h5" fontWeight="bold" >
              Instrument Peformance
            </SuiTypography>
          </SuiBox>
          <SuiBox customClass={classes.tables_table}>
            <Table columns={prCols} rows={prRows} />
          </SuiBox>
        </Card>

        <detailsCard></detailsCard>
        <ChatUI></ChatUI>
      </SuiBox>
    </DashboardLayout>
  );
}

export default Analytics;
