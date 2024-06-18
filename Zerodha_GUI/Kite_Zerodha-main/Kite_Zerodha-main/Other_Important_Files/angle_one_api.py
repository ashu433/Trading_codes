api_key = '1JeCQX72'
username = 'A51173325'
pwd = '9979'
smartApi = SmartConnect(api_key)


try:
    token = "FGUW3TZ32RYCDFFDFMWUCPMPP4"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

data = smartApi.generateSession(username, pwd, totp)
if data['status'] == False:
    logger.error(data)
    
else:
    # login api call
    # logger.info(f"You Credentials: {data}")
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    # fetch the feedtoken
    feedToken = smartApi.getfeedToken()
    res = smartApi.getProfile(refreshToken)
    xox=smartApi.generateToken(refreshToken)
    res=res['data']['exchanges']


try:
    historicParam={
    "exchange": "NFO",
    "symboltoken": "38754",
    "interval": "FIVE_MINUTE",
    "fromdate": "2024-05-17 09:00", 
    "todate": "2024-05-17 15:30"
    }
    data_historical=smartApi.getCandleData(historicParam)
    print(data_historical)
except Exception as e:
    logger.exception(f"Historic Api failed: {e}")
