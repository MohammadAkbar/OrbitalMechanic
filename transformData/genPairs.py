def genPairs(T,stepsize=1):
  import pandas as pd
  Ts = list(
        map(
            lambda b1,b2,a1,a2:
                [a1,a2,b1,b2],
                T["TLE_LINE1"][stepsize:] , T["TLE_LINE2"][stepsize:] , T["TLE_LINE1"][:-stepsize] , T["TLE_LINE2"][:-stepsize]
        )
    )
  Ts_df = pd.DataFrame(Ts,columns=["TLE_A_LINE1","TLE_A_LINE2","TLE_B_LINE1","TLE_B_LINE2"])
  #helpers.prettyPrint(Ts_df)
  return Ts_df

def gen_all_pairs(TLE_pairs_ids):
  all_pairs = {}
  for key, satellite_object in TLE_pairs_ids.items():
    pairs = genPairs(satellite_object)
    all_pairs[key] = pairs
  return all_pairs
