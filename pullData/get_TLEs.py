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

    def mycallback(until):
        duration = int(round(until - time.time()))

    st = SpaceTrackClient(spacetrack_user,spacetrack_pass)
    st.callback = mycallback

    tles = st.tle( norad_cat_id=NORADid , epoch=epoch , format='csv' )
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
