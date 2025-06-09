from typing import Dict, List
import logging
from datetime import datetime, timedelta

class DataFetcher:
    """
    A class to fetch market data from Zerodha.
    
    This class provides functionality to:
    - Fetch historical data
    - Get instrument details
    - Fetch market quotes
    """
    
    def __init__(self, kite_connection):
        """
        Initialize DataFetcher with a KiteConnect instance.
        
        Args:
            kite_connection: An instance of KiteConnect with valid authentication
        """
        self.kite = kite_connection
        self.logger = logging.getLogger(__name__)
    
    def get_historical_data(self, instrument_token: int, from_date: datetime, 
                          to_date: datetime, interval: str = 'day') -> List[Dict]:
        """
        Fetch historical data for a given instrument.
        
        Args:
            instrument_token (int): The instrument token
            from_date (datetime): Start date
            to_date (datetime): End date
            interval (str): Data interval ('minute', '5minute', '15minute', '30minute', '60minute', 'day')
            
        Returns:
            List[Dict]: List of historical data points
        """
        try:
            data = self.kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
            self.logger.info(f"Successfully fetched historical data for token {instrument_token}")
            return data
        except Exception as e:
            self.logger.error(f"Error fetching historical data: {str(e)}")
            return []
    
    def get_instrument_details(self, trading_symbol: str, exchange: str) -> Dict:
        """
        Get instrument details for a specific symbol.
        
        Args:
            trading_symbol (str): The trading symbol (e.g., 'RELIANCE')
            exchange (str): Exchange name (e.g., 'NSE')
            
        Returns:
            Dict: Instrument details
        """
        try:
            instruments = self.kite.instruments(exchange)
            instrument = next(
                (i for i in instruments if i['tradingsymbol'] == trading_symbol),
                None
            )
            return instrument if instrument else {}
        except Exception as e:
            self.logger.error(f"Error fetching instrument details: {str(e)}")
            return {}
    
    def get_quote(self, trading_symbol: str, exchange: str) -> Dict:
        """
        Get current market quote for a symbol.
        
        Args:
            trading_symbol (str): The trading symbol (e.g., 'RELIANCE')
            exchange (str): Exchange name (e.g., 'NSE')
            
        Returns:
            Dict: Current market quote
        """
        try:
            instrument_token = self.get_instrument_details(trading_symbol, exchange).get('instrument_token')
            if instrument_token:
                quote = self.kite.quote(instrument_token)
                return quote
            return {}
        except Exception as e:
            self.logger.error(f"Error fetching quote: {str(e)}")
            return {} 