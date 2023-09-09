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

import React, { useRef } from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo';
import dayjs from 'dayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';

import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function Analytics() {
  const classes = styles();
  const { columns: prCols, rows: prRows } = instrumentTable;
  const [value, setValue] = React.useState(dayjs('year-month-day'));
  const [instrument, setInstrument] = React.useState('');
  const [country, setCountry] = React.useState('');
  const [sector, setSector] = React.useState('');

  const handleChangeInstrument = (event) => {
    setInstrument(event.target.value);
  };

  const handleChangeCountry = (event) => {
    setCountry(event.target.value);
  };

  const handleChangeSector = (event) => {
    setSector(event.target.value);
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <SuiBox py={3}>
        <SuiBox mb={3}>
          <Card>

            <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
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
              <Box sx={{ minWidth: 120 }}>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                  <DemoItem label="Instruments" style={{ marginBottom: '16px' }}></DemoItem>
                  <Select
                    labelId="demo-simple-select-standard-label"
                    id="demo-simple-select-standard"
                    value={instrument}
                    onChange={handleChangeInstrument}
                    label="Instruments"
                  >
                    <MenuItem value="">
                      <em>None</em>
                    </MenuItem>
                    <MenuItem value={10}>Ten</MenuItem>
                    <MenuItem value={20}>Twenty</MenuItem>
                    <MenuItem value={30}>Thirty</MenuItem>
                  </Select>
                </FormControl>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                  <DemoItem label="Country"></DemoItem>
                  <Select
                    labelId="demo-simple-select-standard-label"
                    id="demo-simple-select-standard"
                    value={country}
                    onChange={handleChangeCountry}
                    label="Country"
                  >
                    <MenuItem value={"test1"}>test</MenuItem>
                    <MenuItem value={"test2"}>test1</MenuItem>
                    <MenuItem value={"test3"}>test2</MenuItem>
                  </Select>
                </FormControl>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                  <DemoItem label="Sector"></DemoItem>
                  <Select
                    labelId="demo-simple-select-standard-label"
                    id="demo-simple-select-standard"
                    value={sector}
                    onChange={handleChangeSector}
                    label="Sector"
                  >
                    <MenuItem value={"sector1"}>test</MenuItem>
                    <MenuItem value={"sector2"}>test1</MenuItem>
                    <MenuItem value={"sector3"}>test2</MenuItem>
                  </Select>
                </FormControl>

              </Box>
            </SuiBox>

            <SuiBox mb={3}>
              <Grid container spacing={3}>
                <Grid item xs={8}>
                  <Card className="h-100" style={{ paddingLeft: '10px' }}>
                    <SuiBox p={2}>
                      <SuiBox display="flex" flexDirection="column" height="100%">
                        <SuiTypography variant="h5" fontWeight="bold">
                          Time Series Forecasting
                        </SuiTypography>
                        <SuiBox mb={6}>
                          <SuiTypography variant="body2" textColor="text">
                            Insights about instrument performance
                          </SuiTypography>
                        </SuiBox>
                        <SuiTypography
                          component="a"
                          href="#"
                          variant="button"
                          textColor="text"
                          fontWeight="medium"
                          customClass={classes.buildByDevelopers_button}
                        >
                          Read More
                        </SuiTypography>
                      </SuiBox>
                    </SuiBox>
                  </Card>
                </Grid>

                <Grid item xs={4}>
                  <Card className="h-100" style={{ paddingTop: "15px", paddingLeft: '15px', paddingBottom: "10px" }}>
                    <SuiTypography variant="h5" fontWeight="bold">
                      Details
                    </SuiTypography>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Country:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Currency:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Sector:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Instrument Type:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Created At:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Modified At:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                    <SuiBox>
                      <SuiTypography variant="button" fontWeight="bold" textTransform="capitalize">
                        Remarks:
                      </SuiTypography>
                      <SuiTypography variant="button" fontWeight="regular" textColor="text" padding="10px">
                        test
                      </SuiTypography>
                    </SuiBox>
                  </Card>
                </Grid>

              </Grid>
            </SuiBox>
          </Card>
        </SuiBox>

        <Card>
          <SuiBox display="flex" justifyContent="space-between" alignItems="center" p={3}>
            <SuiTypography variant="h5" fontWeight="bold">
              Instrument Peformance
            </SuiTypography>
          </SuiBox>
          <SuiBox customClass={classes.tables_table}>
            <Table columns={prCols} rows={prRows} />
          </SuiBox>
        </Card>
      </SuiBox>
    </DashboardLayout>
  );
}

export default Analytics;
