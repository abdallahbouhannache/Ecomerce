# Python
from decouple import config

USERNAME = config('SATIM_USERNAME')
PASSWORD = config('SATIM_PASSWORD')
LANGUAGE = "AR"
ORDER_ID = 0
AMOUNT   = 0

url = f"https://test.satim.dz/payment/rest/refund.do?amount={AMOUNT}&language={LANGUAGE}&orderId={ORDER_ID}&password={PASSWORD}&userName={USERNAME}"

print(url)