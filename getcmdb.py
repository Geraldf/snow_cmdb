import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def impcsv(cookies, url, sysid, reccount):
    """read the CMDB from Servicenow and returns an Panda Dataframe, as well as the last read sys_id

    Args:
        cookies (Object): Cookie  from a browser sessiom to avoid login
        url (String): URL to your ServiceNow Instance
        sysid (String): First sys_id to be fetched
        reccount (Int): Number of recrods to be fetched. max: 100000

    Returns:
        dataframe: CMDB as a Pandas Dataframe
        String: Last sys_id fetched. If empty dataframe this will be none
    """

    u = f"{url}&sysparm_record_count={reccount}&sysparm_query=sys_id%3E{sysid}"
    r = requests.get(u, allow_redirects=True, cookies=cookies)
    open(f'cmdb{sysid}.csv', 'w', encoding="utf-8").write(r.text)
    csv_df = pd.read_csv(f'cmdb{sysid}.csv', encoding="utf-8")
    os.remove(f'cmdb{sysid}.csv')
    if (len(csv_df.index) > 0):
        last_sys_ID = csv_df['sys_id'].iloc[-1]
    else:
        last_sys_ID = None
    return csv_df, last_sys_ID


cookies = os.getenv('COOKIES')
url = os.getenv('URL')


cmdb_df, sys_id = impcsv(
    cookies, url, "0", 100)


while sys_id:
    imp_df, sys_id = impcsv(cookies, url, sys_id, 100)
    cmdb_df = pd.concat([cmdb_df, imp_df])

impcsv()
cmdb_df.to_excel("output.xlsx")
