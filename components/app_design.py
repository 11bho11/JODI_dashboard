import plotly.graph_objects as go

layout_simple = go.Layout(
    template="plotly",
    #plot_bgcolor="#FFFFFF",
    hovermode="x",
    hoverdistance=100,  # Distance to show hover label of data point
    spikedistance=1000,  # Distance to show spike
    xaxis=dict(
        showgrid=True,
        #linecolor="#000",
        #linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        showgrid=True,
        #linecolor="#000",
        #linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
)