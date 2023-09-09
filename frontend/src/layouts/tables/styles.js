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
import { makeStyles } from "@mui/styles";

export default makeStyles( ({ palette, boxShadows, borders, functions, transitions, breakpoints }) => {
  const { borderWidth, borderColor } = borders;
  const { borderRadius } = borders;
  const { pxToRem } = functions;
  
  return {
    tables_table: {
      "& .MuiTableRow-root:not(:last-child)": {
        "& td": {
          borderBottom: `${borderWidth[1]} solid ${borderColor}`,
        },
      },
    },
    
    card: {
      minWidth: "auto",
      backgroundPosition: "50%",
      backgroundSize: "cover",
      borderRadius: borderRadius.xl,
      boxShadow: "none",

      [breakpoints.up("xl")]: {
        maxHeight: ({ miniSidenav }) => (miniSidenav ? pxToRem(64) : pxToRem(250)),
        transition: transitions.create("max-height", {
          easing: transitions.easing.easeInOut,
          duration: transitions.duration.standard,
        }),
      },
    },

  };
});
