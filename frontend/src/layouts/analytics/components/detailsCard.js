// @mui material components
import Card from "@mui/material/Card";

// Soft UI Dashboard React components
import SuiBox from "components/SuiBox";
import SuiTypography from "components/SuiTypography";

function DetailsCard() {
    return (
        <div>
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
        </div>
    );
}

export default DetailsCard;