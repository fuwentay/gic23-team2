/* eslint-disable */
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

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

// @mui material components
import Link from "@mui/material/Link";
import Icon from "@mui/material/Icon";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";

// Soft UI Dashboard React base styles
import typography from "assets/theme/base/typography";

// Custom styles for the Footer
import styles from "examples/Footer/styles";

function Footer({ company, links }) {
  const { href, name } = company;
  const { size } = typography;
  const classes = styles();

  const renderLinks = () =>
    links.map((link) => (
      <SuiBox key={link.name} component="li" px={2}>
        <Link href={link.href} target="_blank">
          <SuiTypography variant="button" fontWeight="regular" textColor="text">
            {link.name}
          </SuiTypography>
        </Link>
      </SuiBox>
    ));

  return (
    <SuiBox
      width="100%"
      display="flex"
      flexDirection={{ xs: "column", lg: "row" }}
      justifyContent="space-between"
      alignItems="center"
      px={1.5}
    >
      <SuiBox
        display="flex"
        justifyContent="center"
        alignItems="center"
        flexWrap="wrap"
        color="text"
        fontSize={size.sm}
        px={1.5}
      >
        &copy; {new Date().getFullYear()}, made with
        <SuiBox fontSize={size.regular} color="text" mb={-0.5} mx={0.25}>
          <Icon color="inherit" fontSize="inherit">
            favorite
          </Icon>
        </SuiBox>
        by
        <Link href={href} target="_blank">
          <SuiTypography variant="button" fontWeight="medium">
            &nbsp;{name}&nbsp;
          </SuiTypography>
        </Link>
        for a better web.
      </SuiBox>
      <SuiBox component="ul" customClass={classes.footer_list}>
        {renderLinks()}
      </SuiBox>
    </SuiBox>
  );
}

// Setting default values for the props of Footer
Footer.defaultProps = {
  company: { href: "https://www.creative-tim.com/", name: "Creative Tim" },
  links: [
    { href: "https://www.creative-tim.com/", name: "Creative Tim" },
    { href: "https://www.creative-tim.com/presentation", name: "About Us" },
    { href: "https://www.creative-tim.com/blog", name: "Blog" },
    { href: "https://www.creative-tim.com/license", name: "License" },
  ],
};

// Typechecking props for the Footer
Footer.propTypes = {
  company: PropTypes.objectOf(PropTypes.string),
  links: PropTypes.arrayOf(PropTypes.object),
};

export default Footer;
