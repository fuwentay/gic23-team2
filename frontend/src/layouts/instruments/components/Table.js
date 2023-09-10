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

// Custom styles for the Tables
import styles from "layouts/instruments/styles";

import { useState, useEffect } from 'react';
import ImportPopup from "./ImportPopup";
import FilterSortTable from "../../../components/FilterSortTable"

function Table({ data = [] }) {
    const classes = styles();
    const [open, setOpen] = useState(false);
    const [insertedRows, setInsertedRows] = useState([]);

    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    function getColumns() {
        if (!data || data.length === 0) return [];
        else {
            const firstObject = data[0];
            return Object.keys(firstObject)
                .filter(columnName => columnName !== "_id")
                .map((columnName) => {
                    return { id: columnName, label: columnName };
                });
        }
    }

    function getRows(data) {
        if (!Array.isArray(data)) {
            return [];
        }

        const rows = data.map(item => {
            const { _id, ...rowData } = item;

            if (_id && _id.$oid) {
                rowData._id = _id.$oid;
            }

            if (item.createdAt && item.createdAt.$date) {
                rowData.createdAt = item.createdAt.$date;
            }
            if (item.modifiedAt && item.modifiedAt.$date) {
                rowData.modifiedAt = item.modifiedAt.$date;
            }

            return rowData;
        });

        return rows;
    }

    useEffect(() => {
        setInsertedRows(getRows(data));
    }, [data]);

    return (
        <div>
            <SuiBox display="flex">
                {/* <SuiButton
          component="a"
          target="_blank"
          rel="noreferrer"
          variant="gradient"
          buttonColor="info"
          style={{ marginRight: '1.4rem' }}
          onClick={handleOpen}>
          Upload Data
        </SuiButton> */}

            </SuiBox>
            <SuiBox>
                <SuiBox mb={0}>
                    <Card>
                        <SuiBox customClass={classes.tables_table}>
                            <FilterSortTable
                                title="Inserted Rows"
                                headers={getColumns()}
                                rows={insertedRows} />
                        </SuiBox>
                    </Card>
                </SuiBox>
            </SuiBox>
        </div>
    );
}

export default Table;
