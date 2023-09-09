/* eslint-disable react/prop-types */
// @mui material components
import Icon from "@mui/material/Icon";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";
import SuiProgress from "components/SuiProgress";

// Images
import logoSpotify from "assets/images/small-logos/logo-spotify.svg";
import logoInvesion from "assets/images/small-logos/logo-invision.svg";
import logoJira from "assets/images/small-logos/logo-jira.svg";
import logoSlack from "assets/images/small-logos/logo-slack.svg";
import logoWebDev from "assets/images/small-logos/logo-webdev.svg";
import logoXD from "assets/images/small-logos/logo-xd.svg";
import coin from "assets/images/small-logos/coin.svg";

function Completion({ value, color }) {
  return (
    <SuiBox display="flex" alignItems="center">
      <SuiTypography variant="caption" textColor="text" fontWeight="medium">
        {value}%&nbsp;
      </SuiTypography>
      <SuiBox width="8rem">
        <SuiProgress value={value} color={color} gradient noLabel />
      </SuiBox>
    </SuiBox>
  );
}

const action = (
  <Icon className="font-bold text-secondary cursor-pointer" fontSize="small">
    more_vert
  </Icon>
);

//TODO: add risk, security, or other metrics
export default {
  columns: [
    { name: "instrument", align: "left" },
    { name: "budget", align: "left" },
    { name: "status", align: "left" },
    { name: "completion", align: "center" },
    { name: "action", align: "center" },
  ],

  rows: [
    {
      instrument: [coin, "Equities"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $2,500
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          working
        </SuiTypography>
      ),
      completion: <Completion value={60} color="info" />,
      action,
    },
    {
      instrument: [logoInvesion, "Fixed Income Securities"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $5,000
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          done
        </SuiTypography>
      ),
      completion: <Completion value={100} color="success" />,
      action,
    },
    {
      instrument: [logoJira, "Commodities"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $3,400
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          canceled
        </SuiTypography>
      ),
      completion: <Completion value={30} color="error" />,
      action,
    },
    {
      instrument: [logoSlack, "Hedge Funds"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $1,400
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          canceled
        </SuiTypography>
      ),
      completion: <Completion value={0} color="error" />,
      action,
    },
    {
      instrument: [logoWebDev, "Mutual Funds"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $14,000
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          working
        </SuiTypography>
      ),
      completion: <Completion value={80} color="info" />,
      action,
    },
    {
      instrument: [logoXD, "Infrastructure"],
      budget: (
        <SuiTypography variant="button" textColor="text" fontWeight="medium">
          $2,300
        </SuiTypography>
      ),
      status: (
        <SuiTypography variant="caption" textColor="text" fontWeight="medium">
          done
        </SuiTypography>
      ),
      completion: <Completion value={100} color="success" />,
      action,
    },
  ],
};
