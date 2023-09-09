import { CircularProgress } from "@mui/material";

function Loading() {
    return (
        <div style={{
            display: "flex",
            position: "absolute",
            width: "100vw",
            height: "100vh",
            zIndex: 5,
            backgroundColor: "rgba(0,0,0,0.4)",
            alignItems: "center",
            justifyContent: "center"
        }}>
            <CircularProgress color="inherit" />
        </div>
    )
}

export default Loading;