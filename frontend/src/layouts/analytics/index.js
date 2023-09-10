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
import styles from "layouts/instruments/styles";

// Data
import instrumentTable from "layouts/analytics/data/instrumentTable";

import React, { useState } from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import dayjs from 'dayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';

import Box from '@mui/material/Box';


import TableComponent from "../instruments/components/Table";

import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import ChatbotButton from "./components/ChatbotButton";
import DetailsCard from "./components/detailsCard";
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import BarChart from "./components/BarChart";
import PieChart from "./components/PieChart";

function Analytics() {
  const classes = styles();
  const { columns: prCols, rows: prRows } = instrumentTable;
  const [value, setValue] = React.useState(dayjs('year-month-day'));
  const [fundId, setFundId] = React.useState(1);
  const [instrument, setInstrument] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [sector, setSector] = React.useState('');
  const [isCardOpen, setCardOpen] = useState(false);
  const [topn, setTopn] = React.useState('10');
  const [isCheckedInstruform, setIsCheckedInstruform] = useState(false);
  const [isCheckedCountryform, setIsCheckedCountryform] = useState(false);
  const [isCheckedSectorform, setIsCheckedSectorform] = useState(false);


  const [isInstrumentOpen, setInstrumentOpen] = useState(true);
  const [isCountryOpen, setCountryOpen] = useState(true);
  const [isSectorOpen, setSectorOpen] = useState(true);

  const handleChange = (event) => {
    setTopn(event.target.value);
  };


  const handleInstrumentsOpen = () => {
    setInstrumentOpen((prev) => !prev);
  };

  const handleCountryOpen = () => {
    setCountryOpen((prev) => !prev);
  };

  const handleSectorOpen = () => {
    setSectorOpen((prev) => !prev);
  };


  const handleChatbotClick = () => {
    setCardOpen(prevState => !prevState);
  };

  const handleInstumentsOpen = () => {
    setInstrumentOpen(prevState => !prevState);
  };


  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SuiBox py={3}>
        <SuiBox mb={3}>
          <Card>
            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <Box>
                <SuiTypography variant="h5" fontWeight="bold" >
                  Aggregated View
                </SuiTypography>
                <Box sx={{ minWidth: 100, display: 'flex', flexDirection: 'row' }}>
          <FormControlLabel control={<Checkbox defaultChecked />} label="Instruments" onClick={handleInstrumentsOpen} />
          <FormControlLabel control={<Checkbox defaultChecked />} label="Country" onClick={handleCountryOpen} />
          <FormControlLabel control={<Checkbox defaultChecked />} label="Sector" onClick={handleSectorOpen} />
        </Box>
              </Box>
              <FormControl width='40px'>
                <DemoItem label="Fund ID"></DemoItem>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={topn}
                  label="Top N"
                  onChange={handleChangeId}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={20}>20</MenuItem>
                  <MenuItem value={30}>30</MenuItem>
                </Select>
              </FormControl>
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
            </SuiBox>

            <SuiBox>
            <Box>
                <Card style={{ borderRadius: 0 }}>
                  {isInstrumentOpen && (
                    <>
                      <TableComponent></TableComponent>
                      <ChatbotButton></ChatbotButton>
                    </>
                  )}
                  <SuiBox sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: "0px" }} >
                  </SuiBox>
                </Card>
              </Box>
           

            </SuiBox>
            <SuiBox>
        <Box>
          <Card style={{ borderRadius: 0 }}>
            {isCountryOpen && (
              <>
                <TableComponent></TableComponent>
                <ChatbotButton></ChatbotButton>
              </>
            )}
            <SuiBox sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: "0px" }} />
          </Card>
        </Box>
      </SuiBox>


      <SuiBox>
        <Box>
          <Card style={{ borderRadius: 0 }}>
            {isSectorOpen && (
              <>
                <TableComponent></TableComponent>
                <ChatbotButton></ChatbotButton>
              </>
            )}
            <SuiBox sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: "0px" }} />
          </Card>
        </Box>
      </SuiBox>

          </Card>
        </SuiBox>
        <PieChart></PieChart>

        <SuiBox mb={3}>

          <Card>
            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <SuiTypography variant="h5" fontWeight="bold" >
                Monthly Overview
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
            </SuiBox>
            <SuiTypography >
              <BarChart></BarChart>
            </SuiTypography>
          </Card>
        </SuiBox>

        <SuiBox mb={3}>
          <Card>
            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <SuiTypography variant="h5" fontWeight="bold" >
                Ranking
              </SuiTypography>
              <Box sx={{ marginLeft: "10px", marginTop: "12px" }}>
                <FormControl fullWidth>
                  <DemoItem label="Top N"></DemoItem>
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={topn}
                    label="Top N"
                    onChange={handleChangeTopN}
                  >
                    <MenuItem value={10}>10</MenuItem>
                    <MenuItem value={20}>20</MenuItem>
                    <MenuItem value={30}>30</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </SuiBox>
            <SuiBox customClass={classes.tables_table}>
              <Table columns={prCols} rows={prRows} />
            </SuiBox>
            <ChatbotButton></ChatbotButton>
          </Card>
        </SuiBox>



        <DetailsCard></DetailsCard>
      </SuiBox >
    </DashboardLayout >
  );
}

export default Analytics;
