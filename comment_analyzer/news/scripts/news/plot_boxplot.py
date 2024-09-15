import plotly.graph_objs as go
from plotly.io import to_html
from plotly.subplots import make_subplots
from pathlib import Path

from ...models import Chen0, Chen1, Chen2


DIR = Path(__file__).resolve().parent.parent.parent


def create_boxplot():
    for i in (Chen0, Chen1, Chen2):
        if i == Chen0:
            channel_name = 'BadComedian'
            channel_name_eng = 'BadComedian'
        if i == Chen1:
            channel_name = 'вДудь'
            channel_name_eng = 'VDut'
        if i == Chen2:
            channel_name = 'ещёнепознер'
            channel_name_eng = 'pozner'

        views = [j['views'] for j in i.objects.values('views')]
        com = [j['com'] for j in i.objects.values('com')]
        user = [j['us'] for j in i.objects.values('us')]

        fig = make_subplots(rows=1, cols=3)
        fig.add_trace(go.Box(y=views, name='Views'), 1, 1)
        fig.add_trace(go.Box(y=com, name='Comments'), 1, 2)
        fig.add_trace(go.Box(y=user, name='Unique users'), 1, 3)
        fig.update_layout(showlegend=False, title=f'{channel_name}')

        html_str = to_html(fig)
        with open(f'{DIR}/templates/news/{channel_name_eng}.html', 'w') as ht:
            ht.write(html_str)


create_boxplot()
