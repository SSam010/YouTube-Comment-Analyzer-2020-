import datetime

import plotly.graph_objs as go
from plotly.io import to_html
from pathlib import Path

from ...models import VidDate0, VidDate1, VidDate2

DIR = Path(__file__).resolve().parent.parent.parent


def create_timeline():
    for file_chen in (VidDate0, VidDate1, VidDate2):
        if file_chen == VidDate0:
            channel_name = 'BadComedian'
            channel_name_eng = 'BadComedian'
        if file_chen == VidDate1:
            channel_name = 'вДудь'
            channel_name_eng = 'VDut'
        if file_chen == VidDate2:
            channel_name = 'ещёнепознер'
            channel_name_eng = 'pozner'

        date_pub = [j['load_data'] for j in file_chen.objects.values('load_data')]


        date_pub.sort()

        date_start = datetime.datetime.strptime(date_pub[0], "%Y-%m-%d")
        date_end = datetime.datetime.strptime(date_pub[-1], "%Y-%m-%d")

        table_date = [[], []]

        while True:
            if date_start <= date_end:
                table_date[0] += [str(date_start.date())]
                table_date[1] += [date_pub.count(str(date_start.date()))]

                date_start += datetime.timedelta(days=1)
            else:
                break

        def period_plot(period):
            global table_date_with_period
            table_date_with_period = [[], []]
            days = 0
            point = 0
            while True:
                if days + period <= len(table_date[0]):
                    table_date_with_period[0] += [point]
                    point += 1
                    number_of_video = sum(table_date[1][days:days + period])
                    days += period
                    table_date_with_period[1] += [number_of_video]
                elif days <= len(table_date[0]):

                    table_date_with_period[0] += [point]
                    differ = len(table_date[0]) - period
                    number_of_video = sum(table_date[1][days:differ])
                    table_date_with_period[1] += [number_of_video]
                    break
                else:
                    break

        period_plot(1)

        trace_list = [go.Scatter(visible=True, x=table_date_with_period[0],
                                 y=table_date_with_period[1],
                                 mode='lines+markers', name='f(x)=x<sup>2</sup>')]

        num_steps = [14, 28, 50, 75, 100, 180, 365]
        for i in num_steps:
            period_plot(i)
            trace_list.append(
                go.Scatter(visible=False, x=table_date_with_period[0],
                           y=table_date_with_period[1],
                           mode='lines+markers', name='f(x)=x<sup>2</sup>'))

        fig = go.Figure(data=trace_list)

        steps = []
        for i in range(len(num_steps)):
            step = dict(
                label=str(num_steps[i]),
                method='restyle',
                args=['visible', [False] * len(fig.data)],
            )
            step['args'][1][i] = True

            steps.append(step)

        sliders = [dict(
            currentvalue={"prefix": "Days per step: ", "font": {"size": 20}},
            pad={"b": 10, "t": 50},
            steps=steps,
        )]
        fig.update_layout(showlegend=False, title=f'{channel_name}', xaxis_title="Date, step",
                          yaxis_title="Downloads, ")
        fig.layout.sliders = sliders

        html_str = to_html(fig)
        with open(f'{DIR}/templates/news/timeline_{channel_name_eng}.html', 'w') as ht:
            ht.write(html_str)


create_timeline()
