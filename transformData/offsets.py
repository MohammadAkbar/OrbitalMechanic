def offsets(T):
  # import some stuff
  from tqdm.notebook import tqdm as tqdm
  from skyfield.api import EarthSatellite
  import skyfield.api
  from skyfield.api import Topos, load
  from skyfield.api import EarthSatellite
  import numpy as np
  ts = load.timescale(builtin=True)

  # input: pair of TLEs
  # output: position of second TLE
  def measured(t):
    # create satellite object from the second TLE
    satellite = EarthSatellite(t[2], t[3], '', ts)
    # get t_0 for TLE
    t_0 = satellite.epoch
    # get position of satellite at t_0
    geocentric = satellite.at(t_0)
    # return that position
    return geocentric.position.km

  # input: pair of TLEs
  # output: predicted position from first TLE at epoch t_i+1
  def predict(t):
    # create satellite objects from both TLEs
    satellite_A = EarthSatellite(t[0],t[1],'',ts)
    satellite_B = EarthSatellite(t[2],t[3],'',ts)
    # get epoch for second TLE
    t_B = satellite_B.epoch
    # predict position from first TLE at t_B
    geocentric = satellite_A.at(t_B)
    # return the position
    return geocentric.position.km

  def rotationMatrix(t):
    # create satellite object from observed TLE
    satellite = EarthSatellite(t[2],t[3],'',ts)
    # get t_0 for TLE
    t_0 = satellite.epoch
    # get position(r) and velocity(v)
    r = satellite.at(t_0).position.km
    v = satellite.at(t_0).velocity.km_per_s

    # observation r = axis origin
    O = r
    EO_norm = np.divide(r,np.linalg.norm(r))
    OE_norm = -EO_norm
    OV_norm = np.divide(v,np.linalg.norm(v))
    EOV_norm = np.cross(OE_norm,OV_norm)
    OEP_1 = np.cross(EOV_norm,OV_norm)
    OEP_2 = -OEP_1

    # might need to change
    OEP = OEP_2

    x = OV_norm
    y = EOV_norm
    y = np.divide(y,np.linalg.norm(y))
    z = OE_norm
    z = OEP
    z = np.divide(z,np.linalg.norm(z))
    #z = OE_norm
    #print(np.linalg.norm(x),np.linalg.norm(y),np.linalg.norm(z))
    R = np.zeros((4,4))
    R[0,0:3]  = x
    R[1,0:3]  = y
    R[2,0:3]  = z
    R[3,3]    = 1
    return R

  Offsets = np.empty([len(T), 3])
  #prettyPrint(T)
  for i,t in enumerate(tqdm(T.iterrows())):
    t = t[1]
    # get the measured position from the second TLE
    m = measured(t)
    # get the predicted position from the first TLE
    p = predict(t)
    # get the difference between the prediction and measurement
    diff = m - p
    # store in numpy array

    # get basis from measured
    M = rotationMatrix(t)

    M_inv = np.linalg.inv(M)
    xyz = np.array([[diff[0],diff[1],diff[2],0]])
    new_xyz = np.dot(xyz,M_inv)

    Offsets[i,:] = new_xyz[0,0:3]
  return Offsets
