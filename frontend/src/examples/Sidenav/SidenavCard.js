// @mui material components
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Icon from "@mui/material/Icon";
import Link from "@mui/material/Link";

// Soft UI Dashboard PRO Material-UI components
import SuiButton from "components/SuiButton";
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";

// Custom styles for the SidenavCard
import styles from "examples/Sidenav/styles/sidenavCard";

// Soft UI Dashboard PRO Material-UI context
import { useSoftUIController } from "context";

function SidenavCard() {
  const [controller] = useSoftUIController();
  const { miniSidenav, sidenavColor } = controller;
  const classes = styles({ miniSidenav, sidenavColor });

  return (
    <Card className={classes.card}>
    </Card>
  );
}

export default SidenavCard;
