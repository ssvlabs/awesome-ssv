import { useEffect, useState } from 'react';
import axios from 'axios';

const useTokenPrice = (tokenAddress) => {
  const [price, setPrice] = useState(null);

  useEffect(() => {
    axios
      .get(`https://api.coingecko.com/api/v3/coins/ethereum/contract/${tokenAddress}`)
      .then(response => {
        const id = response.data.id;
        axios
          .get(`https://api.coingecko.com/api/v3/coins/${id}`)
          .then(response => {
            setPrice(response.data.market_data.current_price.usd);
          });
      })
      .catch(error => {
        console.error(error);
      });
  }, []);
  return price;
};
export default useTokenPrice;