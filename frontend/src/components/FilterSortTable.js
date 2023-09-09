import * as React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import SuiButton from "components/SuiButton";
import SuiInput from "components/SuiInput";
import { visuallyHidden } from '@mui/utils';
import styles from "layouts/instruments/styles";
import { CSVLink } from "react-csv";

function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}

function getComparator(order, orderBy) {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}

// Since 2020 all major browsers ensure sort stability with Array.prototype.sort().
// stableSort() brings sort stability to non-modern browsers (notably IE11). If you
// only support modern browsers you can replace stableSort(exampleArray, exampleComparator)
// with exampleArray.slice().sort(exampleComparator)
function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) {
            return order;
        }
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}

function EnhancedTableHead(props) {
    const { order, orderBy, onRequestSort, headers } = props;
    const createSortHandler = (property) => (event) => {
        onRequestSort(event, property);
    };

    return (
        <TableRow>
            {headers.map((headCell) => (
                <TableCell
                    key={headCell.id}
                    align={'right'}
                    padding={headCell.disablePadding ? 'none' : 'normal'}
                    sortDirection={orderBy === headCell.id ? order : false}
                >
                    <TableSortLabel
                        active={orderBy === headCell.id}
                        direction={orderBy === headCell.id ? order : 'asc'}
                        onClick={createSortHandler(headCell.id)}
                    >
                        {headCell.label}
                        {orderBy === headCell.id ? (
                            <Box component="span" sx={visuallyHidden}>
                                {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                            </Box>
                        ) : null}
                    </TableSortLabel>
                </TableCell>
            ))}
        </TableRow>
    );
}

EnhancedTableHead.propTypes = {
    onRequestSort: PropTypes.func.isRequired,
    onSelectAllClick: PropTypes.func.isRequired,
    order: PropTypes.oneOf(['asc', 'desc']).isRequired,
    orderBy: PropTypes.string.isRequired,
    rowCount: PropTypes.number.isRequired,
};

function EnhancedTableToolbar(props) {
    const classes = styles();
    const { title, rows, filter, setFilter } = props;

    return (
        <Toolbar
            sx={{
                pl: { sm: 2 },
                pr: { xs: 1, sm: 1 }
            }}
        >

            <Typography
                sx={{ flex: '1 1 100%' }}
                variant="h6"
                id="tableTitle"
                component="div"
            >
                {title}
            </Typography>

            {rows.length > 0 &&
                <div style={{ display: "flex", flexDirection: "row" }}>
                    <SuiInput
                        placeholder="Filter"
                        customClass={classes.navbar_input}
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)} />
                    <SuiButton
                        component="a"
                        target="_blank"
                        rel="noreferrer"
                        variant="gradient"
                        buttonColor="info"
                        style={{ width: 300, marginLeft: 20 }}>
                        <CSVLink
                            style={{ color: "white" }}
                            filename="inserted_rows.csv"
                            data={rows.map(row => { return { ...row, _id: row._id.$oid } })}>
                            Export to CSV
                        </CSVLink>
                    </SuiButton>
                </div>
            }
        </Toolbar >
    );
}

export default function EnhancedTable(props) {
    const { title, headers, rows } = props;
    const [order, setOrder] = React.useState('asc');
    const [orderBy, setOrderBy] = React.useState('calories');
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(25);
    const [filter, setFilter] = React.useState("");

    const handleRequestSort = (event, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    // Avoid a layout jump when reaching the last page with empty rows.
    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

    const filteredRows = React.useMemo(
        () =>
        stableSort(rows, getComparator(order, orderBy))
            .filter(row => filter.length === 0 || toInclude(row, filter)),
        [rows, order, orderBy, filter]
    )

    const visibleRows = React.useMemo(
        () =>
            filteredRows
                .slice(
                    page * rowsPerPage,
                    page * rowsPerPage + rowsPerPage,
                ),
        [filteredRows, page, rowsPerPage],
    );

    function toInclude(row, filter) {
        const smallCaseFilter = filter.toLowerCase();
        const rowValues = Object.values(row);
        for (let i = 0; i < rowValues.length; i++) {
            if (typeof rowValues[i] === "string" && rowValues[i].toLowerCase().includes(smallCaseFilter)) return true;
            else if (typeof rowValues[i] === "number" && rowValues[i] === parseInt(filter)) return true;
        }
        return false;
    }

    return (
        <Box sx={{ width: '100%' }}>
            <EnhancedTableToolbar
                title={title}
                filter={filter}
                setFilter={setFilter}
                rows={rows} />
            <TableContainer>
                <Table
                    sx={{ minWidth: 750 }}
                    aria-labelledby="tableTitle"
                    size='medium'
                >
                    <EnhancedTableHead
                        headers={headers}
                        order={order}
                        orderBy={orderBy}
                        onRequestSort={handleRequestSort}
                        rowCount={rows.length}
                    />
                    <TableBody>
                        {rows.length === 0
                            ? <TableCell colSpan={6} >
                                No data to display
                            </TableCell>
                            : visibleRows.map((row, index) => {
                                return (
                                    <TableRow
                                        hover
                                        tabIndex={-1}
                                        key={row.name}>
                                        {headers.map((column) => {
                                            return (
                                                <TableCell align="right">{row[column.id]}</TableCell>
                                            )
                                        })}
                                    </TableRow>
                                );
                            })}
                        {emptyRows > 0 && (
                            <TableRow
                                style={{
                                    height: 53 * emptyRows,
                                }}
                            >
                                <TableCell colSpan={6} />
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                SelectProps={{ sx: { width: "80px!important" } }}
                rowsPerPageOptions={[25, 50, 100]}
                component="div"
                count={filteredRows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </Box>
    );
}
