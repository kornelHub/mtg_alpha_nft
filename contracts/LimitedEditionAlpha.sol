// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LimitedEditionAlpha is ERC721URIStorage, ERC721Holder, Ownable {
    uint256 public tokenCounter;

    constructor() ERC721("Limited Edition Alpha MTG set", "Alpha_MTG") ERC721Holder(){
        tokenCounter = 0;
    }

    function createCollectibleCard(string memory _tokenURI) public onlyOwner{
        _safeMint(address(this), tokenCounter);
        _setTokenURI(tokenCounter, _tokenURI);
        tokenCounter += 1;
    }

    function withdraw() external onlyOwner{
        require(address(this).balance > 0);
        payable(owner()).transfer(address(this).balance);
    }
}