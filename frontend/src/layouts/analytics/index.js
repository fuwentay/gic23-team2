// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";
import SuiInput from "components/SuiInput";

// Soft UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Table from "examples/Table";

// Custom styles for the Tables
import styles from "layouts/instruments/styles";

// Data
import instrumentTable from "layouts/analytics/data/instrumentTable";

import React, { useState, useEffect } from 'react';
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
import { get } from '../../api/api';
import BarChart from "./components/BarChart";

export default function Analytics() {
  const classes = styles();
  const { columns: prCols, rows: prRows } = instrumentTable;
  const [value, setValue] = React.useState(dayjs('year-month-day'));
  const [instrument, setInstrument] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [sector, setSector] = React.useState('');
  const [isCardOpen, setCardOpen] = useState(false);
  const [topn, setTopn] = React.useState('10');
  const [countryData, setCountryData] = useState([])
  const [fundId, setFundId] = useState(0)
  const [sectorData, setSectorData] = useState([])
  const [instrumentData, setInstrumentData] = useState([])
  const [isCheckedInstruform, setIsCheckedInstruform] = useState(false);
  const [isCheckedCountryform, setIsCheckedCountryform] = useState(false);
  const [isCheckedSectorform, setIsCheckedSectorform] = useState(false);
  const [n, setN] = useState(3)

  const handleChangeTopN = (event) => {
    setTopn(event.target.value);
  };

  const handleChangeId = (event) => {
    setFundId(event.target.value);
  };

  const handleChangeCountry = (event) => {
    setCountry(event.target.value);
  };

  const handleChangeSector = (event) => {
    setSector(event.target.value);
  };

  const handleChatbotClick = () => {
    setCardOpen(prevState => !prevState);
  };


  async function fetchAggregate(aggregate_key, id, date, setData) {
    const res = await fetch(`/analytics/${aggregate_key}/${id}/${date}`);
    setData(res.data)
  }


  useEffect(() => {
    fetchMessages();
  }, []);

  function fetchMessages() {
    fetch('http://3.0.49.217:9000/instruments/')
      .then(response => response.json())
      .then(data => {
        const dataArray = JSON.parse(data.data);
        setData(dataArray);
      })
      .catch(error => console.error('Error fetching messages:', error));
  }

  const handleCheckboxChange = async (event) => {
    const { id } = event.target;

    switch (id) {
      case 'instruform':
        setIsCheckedInstruform(!isCheckedInstruform);
        if (!isCheckedInstruform)
          // await fetchAggregate('instrumentId', fundId, dayjs().format("YYYY-MM-DD"), setInstrumentData)
          setInstrumentData([
            { instrumentName: "AUSTRALIAN GOVERNMENT 0.3% 11/21/2024 REGS", instrumentType: "Government Bond", totalMarketValue: "$9284400.00" },
            { instrumentName: "CHINA GOVERNMENT BOND 3.0% 05/27/2031	", instrumentType: "Government Bond", totalMarketValue: "$2603480.00" },
            { instrumentName: "JAPAN (20 YEAR ISSUE) 0.4 % 06/20/2040	", instrumentType: "Government Bond", totalMarketValue: "$2036900.00" },
            { instrumentName: "SWEDEN I/L BOND 0.125 % 06/01/2030 144A	", instrumentType: "Government Bond", totalMarketValue: "$690880.00" },
            { instrumentName: "SPAIN I/L BOND 1.8 % 11/30/2024 144A	", instrumentType: "Government Bond", totalMarketValue: "$4028990.00" },
            { instrumentName: "SWEDEN I/L BOND 0.125 % 06/01/2030 144A	", instrumentType: "Government Bond", totalMarketValue: "$492700.00" },
            { instrumentName: "REPUBLIC OF AUSTRIA 0.75 % 10/20/2026 144A	", instrumentType: "Government Bond", totalMarketValue: "$312280.00" }
          ])
        break;
      case 'countryform':
        setIsCheckedCountryform(!isCheckedCountryform);
        if (!isCheckedCountryform)
          setCountryData([
            { country: "UK", totalMarketValue: "$9284400.00" },
            { country: "AU", totalMarketValue: "$2603480.00" },
            { country: "JP", totalMarketValue: "$2036900.00" },
            { country: "IM", totalMarketValue: "$690880.00" },
            { country: "DE", totalMarketValue: "$4028990.00" },
            { country: "SM", totalMarketValue: "$492700.00" },
            { country: "BB", totalMarketValue: "$312280.00" }
          ])
        // await fetchAggregate('country', fundId, dayjs().format("YYYY-MM-DD"), setCountryData)
        break;
      case 'sectorform':
        setIsCheckedSectorform(!isCheckedSectorform);
        if (!isCheckedSectorform)
          setSectorData([
            { sector: "Treasury", totalMarketValue: "$312280.00" },
            { sector: "Consumer Discretionary", totalMarketValue: "$2603480.00" },
            { sector: "Real Estate", totalMarketValue: "$2036900.00" },
            { sector: "Materials", totalMarketValue: "$690880.00" },
            { sector: "Information Technology", totalMarketValue: "$4028990.00" },
            { sector: "Industrials", totalMarketValue: "$492700.00" },
            { sector: "Healthcare", totalMarketValue: "$312280.00" },
            { sector: "Financials", totalMarketValue: "$9516280.00" },
            { sector: "Energy", totalMarketValue: "$7895830.00" }
          ])
        // await fetchAggregate('sector', fundId, dayjs().format("YYYY-MM-DD"), setSectorData)
        break;
      default:
        break;
    }
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
                <Box sx={{ marginLeft: "10px", marginTop: "12px" }}>
                  <Box sx={{ minWidth: 100, display: 'flex', flexDirection: 'row' }}>
                    <FormControlLabel
                      control={<Checkbox id="instruform" checked={isCheckedInstruform} onChange={handleCheckboxChange} />}
                      label="Instruments"
                    />
                    <FormControlLabel
                      id="countryform"
                      control={<Checkbox id="countryform" checked={isCheckedCountryform} onChange={handleCheckboxChange} />}
                      label="Country"
                    />
                    <FormControlLabel
                      id="sectorform"
                      control={<Checkbox id="sectorform" checked={isCheckedSectorform} onChange={handleCheckboxChange} />}
                      label="Sector"
                    />
                    <SuiInput
                      style={{ height: 42, width: 200 }}
                      value={fundId}
                      onChange={(e) => setFundId(e.target.value)} />
                  </Box>
                </Box>
              </Box>

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
              <Card style={{ borderRadius: 0 }}>
                <TableComponent
                  data={instrumentData} />
                <ChatbotButton></ChatbotButton>
                <SuiBox sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: "0px" }} >
                </SuiBox>
              </Card>

            </SuiBox>
            <Card style={{ borderRadius: 0 }}>
              <SuiBox>
                <TableComponent
                  data={countryData} />
                <ChatbotButton></ChatbotButton>
              </SuiBox>
            </Card>
            <Card style={{ borderRadius: 0, boxShadow: 'none' }}>
              <SuiBox mb={0}>
                <TableComponent
                  data={sectorData} />
                <ChatbotButton></ChatbotButton>
              </SuiBox>
            </Card>

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
              <BarChart />
            </SuiTypography>
          </Card>
        </SuiBox>

        <SuiBox mb={3}>
          <Card>
            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
              <SuiTypography variant="h5" fontWeight="bold" >
                Top N Fund Ranking
              </SuiTypography>
              <Box sx={{ marginLeft: "10px", marginTop: "12px" }}>
                <FormControl fullWidth>
                  <DemoItem label="Top N"></DemoItem>
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={n}
                    label="Top N"
                    onChange={(e) => setN(parseInt(e.target.value))}
                  >
                    <MenuItem value={3}>3</MenuItem>
                    <MenuItem value={5}>5</MenuItem>
                    <MenuItem value={10}>10</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </SuiBox>
            <SuiBox>
              <TableComponent
                data={[
                  { ranking: 1, fundName: "Leeder", investmentReturns: "$3650200.00" },
                  { ranking: 2, fundName: "Belaware", investmentReturns: "$3189200.00" },
                  { ranking: 3, fundName: "Fund Whitestone", investmentReturns: "$2961200.00" },
                  { ranking: 4, fundName: "Applebead", investmentReturns: "$2850200.00" },
                  { ranking: 5, fundName: "Magnum", investmentReturns: "$2693200.00" },
                  { ranking: 6, fundName: "Wallington", investmentReturns: "$2510200.00" },
                  { ranking: 7, fundName: "Gohen", investmentReturns: "$2450200.00" },
                  { ranking: 8, fundName: "Catalysm", investmentReturns: "$2354200.00" },
                  { ranking: 9, fundName: "Trustmind", investmentReturns: "$1659200.00" },
                  { ranking: 10, fundName: "Virtous", investmentReturns: "$1351100.00" }
                ].slice(0, n)} />
              <ChatbotButton></ChatbotButton>
            </SuiBox>
          </Card>
        </SuiBox>



      </SuiBox >
    </DashboardLayout >
  );
}
