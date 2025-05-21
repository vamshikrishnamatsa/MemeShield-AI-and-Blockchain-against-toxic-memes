import React, { useState } from 'react';
import { ethers } from 'ethers';
import MemeVoteABI from '../contract/MemeVoteABI.json';
import { uploadToIPFS } from '../utils/pinata';

const CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

const MemeUploader = () => {
  const [file, setFile] = useState(null);
  const [memeId, setMemeId] = useState('');
  const [ipfsUrl, setIpfsUrl] = useState('');
  const [voteStatus, setVoteStatus] = useState('');

  const uploadMeme = async () => {
    const ipfsHash = await uploadToIPFS(file);
    setIpfsUrl(ipfsHash);

    const provider = new ethers.BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    const contract = new ethers.Contract(CONTRACT_ADDRESS, MemeVoteABI.abi, signer);


    const tx = await contract.uploadMeme(ipfsHash);
    await tx.wait();
    alert('Meme uploaded!');
  };

  const voteOnMeme = async (isOffensive) => {
    const provider = new ethers.BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    const contract = new ethers.Contract(CONTRACT_ADDRESS, MemeVoteABI.abi, signer);

    const tx = await contract.vote(memeId, isOffensive);
    await tx.wait();
    setVoteStatus(isOffensive ? "Voted: Offensive" : "Voted: Not Offensive");
  };

  return (
    <div>
      <h2>Upload Meme</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadMeme}>Upload</button>

      {ipfsUrl && (
        <div>
          <p>IPFS URL: <a href={ipfsUrl} target="_blank" rel="noreferrer">{ipfsUrl}</a></p>
        </div>
      )}

      
    </div>
  );
};

export default MemeUploader;