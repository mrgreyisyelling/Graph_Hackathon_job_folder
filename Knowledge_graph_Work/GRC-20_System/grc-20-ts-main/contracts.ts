/**
 * This module provides the known contract addresses for smart contracts
 * used in the knowledge graph.
 *
 * @since 0.0.6
 */

/**
 * Mainnet contract addresses
 */
export const MAINNET = {
  SPACE_PLUGIN_REPO_ADDRESS: '0xd9559df98e4103CDf0A119d4bff1537B383E462c',
  PERSONAL_SPACE_ADMIN_PLUGIN_REPO_ADDRESS: '0xa00870c6501349E126E71Dc1705fBaa2B5aeac0d',
  GOVERNANCE_PLUGIN_REPO_ADDRESS: '0x81A45db7E303eED5D8e0B84b39d96DBa23192Eab',
  DAO_FACTORY_ADDRESS: '0x9012fcc278a860B66e644cE491a1CbabFBb34a72',
  ENS_REGISTRY_ADDRESS: '0x81C575f78903F8aC1FD73dEC06d20ffdC51c9b4E',
  PLUGIN_SETUP_PROCESSOR_ADDRESS: '0xfcC0Aba63c1F1f887099EAB0d1A624A5B7A82Fc2',
} as const;

/**
 * Testnet contract addresses
 */
export const TESTNET = {
  SPACE_PLUGIN_REPO_ADDRESS: '0x0701454b0e80C53Ee8c3e0805616424758D7E7Fd',
  PERSONAL_SPACE_ADMIN_PLUGIN_REPO_ADDRESS: '0xAe8Ac47e5f3bDa62F6D1BD140AB8e1926D867355',
  GOVERNANCE_PLUGIN_REPO_ADDRESS: '0x70E786A75c7ef46C09665e25E1a683A936057087',
  DAO_FACTORY_ADDRESS: '0xb138AE700C352BB1aC75688e8ceCB98CDDaa7F09',
  ENS_REGISTRY_ADDRESS: '0xD065A680075d0e27777bAa63CFFf17e1713a19Df',
  PLUGIN_SETUP_PROCESSOR_ADDRESS: '0x3C9be4b42B313318091344A261DCDCd02DCd5736',
} as const;
