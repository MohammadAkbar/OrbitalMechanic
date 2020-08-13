def plot_offsets(Offsets,thescale=100,NORAD_ID=-1):
  # import plotly graphing library
  import plotly.express as px
  import plotly.graph_objects as go


  import pandas as pd

  #print(Offsets.T)
  # make plot
  fig = go.Figure(
  )

  # put numpy matrix into pandas dataframe
  df = pd.DataFrame(Offsets, columns=["x","y","z"])
  #prettyPrint(df)

  # make plot
  fig.add_trace(

      go.Scatter3d(
        name="NORAD ID : "+str(NORAD_ID),
        x=df["x"], y=df["y"], z=df["z"],
        mode = "markers",
        marker=dict(
            #size=dfsub["s"],
            color = 'red',
            size=1.5,
            opacity=1,
            line=dict(
                width=0
            )
        )
      )
  )
  # add x axis

  fig.add_trace(
    go.Scatter3d(
      name="x-axis(parallel to velocity)",
      x=[-thescale,thescale], y=[0,0], z=[0,0],
      line=dict(
          color='red',
          width=4
      ),
      mode="lines"
    )
  )
  # add y axis
  fig.add_trace(
    go.Scatter3d(
        name="y-axis",
      x=[0,0], y=[-thescale,thescale], z=[0,0],
      line=dict(
          color='green',
          width=4
      ),
      mode="lines"
    )
  )
  # add z axis
  fig.add_trace(
    go.Scatter3d(
        name="z-axis(parallel to altitude)",
      x=[0,0], y=[0,0], z=[-thescale,thescale],
      line=dict(
          color='blue',
          width=4
      ),
      mode="lines"
    )
  )
  fig.update_layout(
      width=1200,
      height=800,
      #autosize=False,
      plot_bgcolor='rgba(0,0,0,0)',
      scene_aspectmode='cube',
      scene={
          "camera.projection.type": "orthographic",
          "camera.center":{
              "x":0,
              "y":0,
              "z":0
          },

          "xaxis":dict(nticks=4, range=[-thescale,thescale],),
          "yaxis":dict(nticks=4, range=[-thescale,thescale],),
          "zaxis":dict(nticks=4, range=[-thescale,thescale],),

      },
  )

  fig.update_layout(
      width=1200,
      height=800,
      scene = {
        "camera.projection.type": "orthographic",
        "xaxis":dict(range=[-thescale,thescale],),
        "yaxis":dict(range=[-thescale,thescale],),
        "zaxis":dict(range=[-thescale,thescale],),
      }
  )
  config = dict()
  fig.show(config=config)
