from connection.zerodha_connection import ZerodhaConnection
from data_loader.data_fetcher import DataFetcher
from datetime import datetime, timedelta

def main():
    """Main function to demonstrate data fetching."""
    # Initialize connection (authentication handled automatically)
    connection = ZerodhaConnection()
    
    # Exit if not authenticated
    if not connection.is_authenticated():
        return
    
    # Create data fetcher instance
    data_fetcher = DataFetcher(connection.kite)
    
    # Example: Get historical data for RELIANCE
    print("\n📊 Fetching data for RELIANCE...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get instrument details
    instrument = data_fetcher.get_instrument_details('RELIANCE', 'NSE')
    token = instrument.get('instrument_token')

    # Get historical data
    historical_data = data_fetcher.get_historical_data(
        instrument_token=token,
        from_date=start_date,
        to_date=end_date,
        interval='day'
    )
    print(historical_data)

if __name__ == "__main__":
    main()
