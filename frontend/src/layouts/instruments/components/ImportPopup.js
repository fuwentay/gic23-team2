import Card from "@mui/material/Card";
import SuiBox from "components/SuiBox";
import styles from "layouts/instruments/styles";
import SuiButton from "components/SuiButton";
import SuiInput from "components/SuiInput";
import React, { useRef, useState } from 'react';
import Modal from '@mui/material/Modal';
import { post, postFile } from "../../../api/api";
import Loading from "components/Loading";

function ImportPopup(props) {
    const classes = styles();
    const { open, handleClose, setInsertedRows } = props;
    const [apiUrl, setApiUrl] = useState("https://reqres.in/api/users?page=2");
    const [loading, setLoading] = useState(false);
    const hiddenFileInput = useRef(null);

    const handleChooseFile = () => {
        hiddenFileInput.current.click();
    };

    async function handleUploadFile(e) {
        const files = document.getElementById("file");
        const res = await postFile("http://localhost:5000/ingest/insertFromFile", files.files[0], setLoading);
        if (res.status === 200) {
            setInsertedRows(JSON.parse(res.data));
            handleClose();
            e.target.value = null;
        }
    };

    async function handleInsertFromApi() {
        const res = await post("http://localhost:5000/ingest/insertFromApi", { url: apiUrl }, setLoading);
        if (res.status === 200) {
            setInsertedRows(JSON.parse(res.data));
            handleClose();
        }
    }

    async function handleClear() {
        const res = await post("http://localhost:5000/ingest/deleteAll", {}, setLoading);
        if (res.status === 200) {
            setInsertedRows([]);
            handleClose();
        }
    }

    return (
        <Modal
            open={open}
            aria-labelledby="child-modal-title"
            aria-describedby="child-modal-description"
        >
            <SuiBox style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                {loading && <Loading />}
                <div
                    style={{ backgroundColor: 'black', opacity: '0', position: 'fixed', height: '100vh', width: '100vw', zIndex: '1' }}
                    onClick={handleClose} />
                <Card
                    className={classes.card}
                    style={{ padding: 20, zIndex: '2' }}>
                    <div>
                        <input
                            id="file"
                            style={{ display: "none" }}
                            type="file"
                            name="file"
                            ref={hiddenFileInput}
                            onChange={handleUploadFile} />
                        <SuiButton
                            component="a"
                            target="_blank"
                            rel="noreferrer"
                            variant="gradient"
                            buttonColor="info"
                            style={{ marginRight: '1.4rem' }}
                            onClick={handleChooseFile}>
                            Upload File
                        </SuiButton>
                    </div>
                    <div style={{ display: "flex", flexDirection: "row", marginTop: 10 }}>
                        <SuiButton
                            component="a"
                            target="_blank"
                            rel="noreferrer"
                            variant="gradient"
                            buttonColor="info"
                            style={{ marginRight: '1.4rem' }}
                            onClick={handleInsertFromApi}>
                            Insert From API
                        </SuiButton>
                        <SuiInput
                            placeholder="Type API endpoint here..."
                            customClass={classes.navbar_input}
                            value={apiUrl}
                            onChange={setApiUrl} />
                    </div>
                    <div style={{ marginTop: 10 }}>
                        <SuiButton
                            component="a"
                            target="_blank"
                            rel="noreferrer"
                            variant="gradient"
                            buttonColor="info"
                            style={{ marginRight: '1.4rem' }}
                            onClick={handleClear}>
                            Clear DB
                        </SuiButton>
                    </div>
                </Card>
            </SuiBox>
        </Modal>
    )
}

export default ImportPopup;