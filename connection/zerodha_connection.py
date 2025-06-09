from kiteconnect import KiteConnect
import logging
import os

class ZerodhaConnection:
    """
    A class to handle Zerodha API connection and authentication.
    
    This class provides functionality to:
    - Initialize connection with Zerodha API
    - Handle authentication
    - Manage access tokens
    
    Attributes:
        api_key (str): Zerodha API key
        api_secret (str): Zerodha API secret
        kite (KiteConnect): Instance of KiteConnect for API interactions
    """
    
    def __init__(self):
        """
        Initialize ZerodhaConnection with API credentials.
        
        The initialization:
        1. Sets up API credentials
        2. Creates KiteConnect instance
        3. Configures logging
        4. Attempts to authenticate using saved access token
        """
        # Zerodha API credentials
        API_KEY = "5eluftddht8pwa7o"
        API_SECRET = "wcpxfs5j94z66e6r1zymeme63qxm7yno"
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        
        # Initialize KiteConnect with API key
        self.kite = KiteConnect(api_key=self.api_key)
        
        # Configure logging for debugging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Attempt to authenticate
        self._authenticate()
    
    def _authenticate(self):
        """
        Attempt to authenticate using saved access token.
        """
        print(f"1. Visit: {self.get_login_url()}")
        try:
            if os.path.exists("access_token.txt"):
                with open("access_token.txt", "r") as f:
                    access_token = f.read().strip()
                if access_token:
                    data = self.kite.generate_session(access_token, api_secret=self.api_secret)
                    self.kite.set_access_token(data["access_token"])
                    # Test the token
                    profile = self.kite.profile()
                    self.logger.info(f"Authentication successful! User: {profile.get('user_name', 'Unknown')}")
                    print(f"✓ Authenticated as: {profile.get('user_name', 'Unknown')}")
                    return True
            
            print("❌ Authentication required!")
            print(f"1. Visit: {self.get_login_url()}") 
            print("2. Complete login and copy the access token")
            print("3. Save the access token to 'access_token.txt'")
            return False
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            print("❌ Authentication failed!")
            print(f"1. Visit: {self.get_login_url()}")
            print("2. Get a fresh access token and save to 'access_token.txt'")
            return False
    
    def set_access_token(self, access_token: str):
        """
        Set the access token for API authentication.
        
        Args:
            access_token (str): The access token from Zerodha
        """
        self.kite.set_access_token(access_token)
        # Save to file for future use
        with open("access_token.txt", "w") as f:
            f.write(access_token)
    
    def get_login_url(self) -> str:
        """
        Get the login URL for Zerodha authentication.
        
        Returns:
            str: The login URL
        """
        return self.kite.login_url()
    
    def is_authenticated(self) -> bool:
        """
        Check if the connection is authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        try:
            self.kite.profile()
            return True
        except:
            return False