import React, { useCallback, useState } from "react";
import { SSVKeys } from 'ssv-keys';
import Dropzone from "./DropZone";
import { Spin, Button } from 'antd';

// Operators and their IDs dummy data
const operatorPublicKeys = require('../constants/operators.json');
const operatorIds = require('../constants/operatorIds.json');

const STEPS = {
  START: 0,
  ENTER_PASSWORD: 1,
  DECRYPT_KEYSTORE: 2,
  ENCRYPT_SHARES: 3,
  FINISH: 4,
}

function Keyshares() {
  // Initialize SSVKeys SDK
  const ssvKeys = new SSVKeys(SSVKeys.VERSION.V3);

  // States
  const [step, setStep] = useState(STEPS.START);
  const [password, setPassword] = useState('');
  const [keyShares, setKeyShares] = useState([]);
  const [finalPayload, setFinalPayload] = useState('');
  const [keystoreFile, setKeystoreFile] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.map((file) => {
      const reader = new FileReader();
      reader.onload = function (e) {
        setKeystoreFile(e.target.result);
        setStep(STEPS.ENTER_PASSWORD);
      };
      reader.readAsText(file)
      return file;
    });
  }, []);

  const startProcess = async () => {
    setStep(STEPS.DECRYPT_KEYSTORE);
    const privateKey = await ssvKeys.getPrivateKeyFromKeystoreData(keystoreFile, password).then((result) => {
      if (result instanceof Error) {
        alert(result.message);
        setStep(STEPS.ENTER_PASSWORD);
        return;
      }
      setStep(STEPS.ENCRYPT_SHARES);
      console.log('Private key ready');
      return result;
    });
    const encryptedShares = await ssvKeys.buildShares(privateKey, operatorIds, operatorPublicKeys);

    // Build final web3 transaction payload and update keyshares file with payload data
    const payload = await ssvKeys.buildPayload(
      {
        publicKey: ssvKeys.publicKey,
        operatorIds,
        encryptedShares,
      }
    );

    setFinalPayload(JSON.stringify(payload));
    console.log('Payload ready');

    // Keyshares
    const keyShares = ssvKeys.keyShares.fromJson({
      version: 'v3',
      data: {
        operators: operatorPublicKeys.map((operator, index) => ({
          id: operatorIds[index],
          publicKey: operator,
        })),
        publicKey: ssvKeys.publicKey,
        encryptedShares,
      },
      payload,
    });
    setKeyShares(keyShares.toJson());
    console.log('KeyShares ready');
    setStep(STEPS.FINISH);
  };

  const downloadKeyShares = () => {
    const blob = new Blob([keyShares], { type: 'application/json;charset=utf-8;' });
    const filename = 'KeyShares.json';
    if (navigator.msSaveBlob) { // In case of IE 10+
      navigator.msSaveBlob(blob, filename);
    } else {
      const link = document.createElement('a');
      if (link.download !== undefined) {
        // Browsers that support HTML5 download attribute
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  };

  switch (step) {
    default:
    case STEPS.START:
      return (
        <div id={`${STEPS.START}`}>
          <h5>To generate keyshares, You can select <code>test.keystore.json</code> file in the root of this project. Password: <code>testtest</code></h5>
          <Dropzone onDrop={onDrop} accept={"application/json"} />
        </div>
      );
    case STEPS.ENTER_PASSWORD:
      return (
        <div id={`${STEPS.ENTER_PASSWORD}`}>
          <h3>Enter keystore password</h3>
          <input type="password" onChange={(event) => { setPassword(event.target.value); }} className="input" />
          <br />
          <button type="button" onClick={startProcess} className="btn">
            Decrypt Keystore File
          </button>
        </div>
      );
    case STEPS.DECRYPT_KEYSTORE:
      return (
        <div id={`${STEPS.DECRYPT_KEYSTORE}`}>
          <h3></h3>
          <Spin tip="Decrypting keystore with your password.." size="large">
            <div className="content" />
          </Spin>
        </div>
      );
    case STEPS.ENCRYPT_SHARES:
      return (
        <div id={`${STEPS.ENCRYPT_SHARES}`}>
          <h3></h3>
          <Spin tip="Encrypting Shares.." size="large">
            <div className="content" />
          </Spin>
        </div>
      );
    case STEPS.FINISH:
      return (
        <div id={`${STEPS.FINISH}`}>

          <Button type="button" onClick={downloadKeyShares} disabled={!keyShares} className="btn">
            Download Keyshares File
          </Button>
        </div>
      );
  }
}

export default Keyshares;
