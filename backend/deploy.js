const hre = require("hardhat");

async function main() {
  const MemeVote = await hre.ethers.getContractFactory("MemeVote");
  const memeVote = await MemeVote.deploy(); // Deploy the contract
  console.log(`MemeVote deployed to: ${memeVote.target || memeVote.address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
