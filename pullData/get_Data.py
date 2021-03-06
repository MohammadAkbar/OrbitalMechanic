# generate TLE pairs for object(NORADid)
def get_TLEs(NORADid,
            spacetrack_user,
            spacetrack_pass,
            epoch="2010-01-01--2011-01-01",
            stepsize=1
            ):

    import spacetrack.operators as op
    from spacetrack import SpaceTrackClient
    import numpy as np
    import pandas as pd
    from io import StringIO

    def mycallback(until):
        duration = int(round(until - time.time()))

    st = SpaceTrackClient(spacetrack_user,spacetrack_pass)
    st.callback = mycallback

    tles = st.tle( norad_cat_id=NORADid , epoch=epoch , format='csv' )
    T=0
    if tles:
        T = pd.read_csv( StringIO(tles) )
    T.sort_values( by=['EPOCH'] )
    Ts = list(
        map(
            lambda b1,b2,a1,a2:
                [a1,a2,b1,b2],
                T["TLE_LINE1"][stepsize:] , T["TLE_LINE2"][stepsize:] , T["TLE_LINE1"][:-stepsize] , T["TLE_LINE2"][:-stepsize]
        )
    )
    return Ts

def get_batch_TLEs(NORADid,
            spacetrack_user,
            spacetrack_pass,
            epoch="2010-01-01--2011-01-01",
            stepsize=1
            ):

    import spacetrack.operators as op
    from spacetrack import SpaceTrackClient
    import numpy as np
    import pandas as pd
    from io import StringIO
    from tqdm.notebook import tqdm as tqdm

    def mycallback(until):
        duration = int(round(until - time.time()))

    st = SpaceTrackClient(spacetrack_user,spacetrack_pass)
    st.callback = mycallback

    TLE_ids = {}
    tles = st.tle( norad_cat_id=NORADid , epoch=epoch , format='csv' )
    if tles:
      t = pd.read_csv(StringIO(tles))
      for id in tqdm(NORADid):
        ids = t[(t['NORAD_CAT_ID'] == id)]
        TLE_ids[id] = ids[['NORAD_CAT_ID','TLE_LINE1','TLE_LINE2']]
    return TLE_ids


#Get Current MEO objects
def get_MEO_ids():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('OrbitalMechanic/Data/inOrbit.csv')
    #df = df[df['OBJECT_NAME'].str.contains("DEB")]
    df = df[(df['APOGEE'] > 2000)&(df['APOGEE']<36000)]
    return list(np.unique(df["NORAD_CAT_ID"]))

#Get Current LEO objects
def get_LEO_ids():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('OrbitalMechanic/Data/inOrbit.csv')
    #df = df[df['OBJECT_NAME'].str.contains("DEB")]
    df = df[(df['APOGEE'] > 125)&(df['APOGEE']<2000)]
    return list(np.unique(df["NORAD_CAT_ID"]))

#Get Current GEO objects
def get_GEO_ids():
    import pandas as pd
    import numpy as np
    df = pd.read_csv('OrbitalMechanic/Data/inOrbit.csv')
    #df = df[df['OBJECT_NAME'].str.contains("DEB")]
    df = df[(df['APOGEE'] > 36000)]
    return list(np.unique(df["NORAD_CAT_ID"]))
