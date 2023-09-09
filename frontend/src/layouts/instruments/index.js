/**
=========================================================
* Soft UI Dashboard React - v2.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-material-ui
* Copyright 2021 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";

// Soft UI Dashboard React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";

// Custom styles for the Tables
import styles from "layouts/instruments/styles";

import SuiButton from "components/SuiButton";
import { useState, useEffect } from 'react';
import ImportPopup from "./components/ImportPopup";
import FilterSortTable from "../../components/FilterSortTable"
import Table from "./components/Table";

function Instruments() {
  const classes = styles();
  const [open, setOpen] = useState(false);
  const [insertedRows, setInsertedRows] = useState([]);
  const [data, setData] = useState([]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  useEffect(() => {
    fetchMessages();
  }, []);

  function fetchMessages() {
    fetch('http://0.0.0.0:9000/instruments/')
      .then(response => response.json())
      .then(data => {
        setData(data);
        console.log(data);
      })
      .catch(error => console.error('Error fetching messages:', error));
  }

  function getColumns() {
    if (insertedRows.length === 0 || !insertedRows[0]) return [];
    else return Object.keys(insertedRows[0])
      .filter(columnName => columnName !== "_id")
      .map((columnName) => {
        return { id: columnName, label: columnName }
      });
  }

  //CHECK how to pass data to table
  return (
    <DashboardLayout>
      <DashboardNavbar />
      <Table data={data}></Table>
    </DashboardLayout>
  );
}

export default Instruments;
